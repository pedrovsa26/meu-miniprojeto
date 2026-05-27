import csv
# Importa as funções criadas no arquivo funcoes.py
from funcoes import limpar_categoria, tratar_dimensoes_fisicas, formatar_data_br, validar_hipotese_cancelado

def processar_produtos(caminho_input, caminho_output):
    total_linhas = 0
    nulos_corrigidos = 0
    linhas_descartadas = 0
    
    with open(caminho_input, mode='r', encoding='utf-8-sig') as arquivo_in, \
         open(caminho_output, mode='w', encoding='utf-8', newline='') as arquivo_out:
        
        leitor = csv.DictReader(
            arquivo_in, 
            delimiter=',', 
            quotechar='"', 
            skipinitialspace=True
        )
        
        # CORRIGIDO: Agora 'campos' está 100% em minúsculo
        campos = leitor.fieldnames
        if campos and len(campos) == 1 and 'product_category_name' in campos[0]:
            texto_cabecalho = campos[0].replace('"', '')
            campos = texto_cabecalho.split(',')
            
            arquivo_in.seek(0)
            next(arquivo_in) 
            leitor = csv.DictReader(arquivo_in, fieldnames=campos, delimiter=',')

        escritor = csv.DictWriter(arquivo_out, fieldnames=campos)
        escritor.writeheader()
        
        for linha in leitor:
            total_linhas += 1
            
            if 'product_category_name' not in linha:
                valores = list(linha.values())
                if len(valores) >= 2:
                    categoria_original = valores[1]
                else:
                    categoria_original = ""
            else:
                categoria_original = linha['product_category_name']
            
            if not categoria_original or categoria_original.strip() == "" or categoria_original == '""':
                nulos_corrigidos += 1
                categoria_original = "Sem Categoria"
                
            linha['product_category_name'] = limpar_categoria(categoria_original)
            
            linha_tratada = tratar_dimensoes_fisicas(linha)
            if linha_tratada is None:
                linhas_descartadas += 1
                continue 
                
            escritor.writerow(linha_tratada)
            
    return total_linhas, nulos_corrigidos, linhas_descartadas

def processar_pedidos(caminho_input, caminho_output):
    total_linhas = 0
    pedidos_cancelados = 0
    hipotese_confirmada = True
    
    with open(caminho_input, mode='r', encoding='utf-8') as arquivo_in, \
         open(caminho_output, mode='w', encoding='utf-8', newline='') as arquivo_out:
         
        leitor = csv.DictReader(arquivo_in)
        campos = leitor.fieldnames
        escritor = csv.DictWriter(arquivo_out, fieldnames=campos)
        escritor.writeheader()
        
        for linha in leitor:
            total_linhas += 1
            
            # Contagem de cancelados
            if linha['order_status'] == 'canceled':
                pedidos_cancelados += 1
                
            # 3. Validação da regra de negócio (Hipótese de cancelamento)
            valido = validar_hipotese_cancelado(linha['order_status'], linha['order_delivered_customer_date'])
            if not valido:
                hipotese_confirmada = False # Encontrou um pedido não-cancelado sem data de entrega
                
            # 4. Formatação Temporal
            linha['order_approved_at'] = formatar_data_br(linha['order_approved_at'])
            
            escritor.writerow(linha)
            
    return total_linhas, pedidos_cancelados, hipotese_confirmada

if __name__ == "__main__":
    print("Iniciando Pipeline de Sanitização de Dados... 🚀\n")
    
    # Processando base de produtos
    tot_prod, nulos_prod, descartes = processar_produtos('olist_products_dataset.csv', 'produtos_sanitizados.csv')
    
    # Processando base de pedidos
    tot_ped, cancelados, hipotese = processar_pedidos('olist_orders_dataset.csv', 'pedidos_sanitizados.csv')
    
    # --- RELATÓRIO DE STATUS MANUAL ---
    print("="*40)
    print("      RELATÓRIO DE SANITIZAÇÃO      ")
    print("="*40)
    print(f"Total de produtos processados: {tot_prod}")
    print(f"Total de categorias nulas/corrigidas: {nulos_prod}")
    print(f"Total de produtos descartados (dimensões ausentes): {descartes}")
    print("-"*40)
    print(f"Total de pedidos processados: {tot_ped}")
    print(f"Total de pedidos cancelados identificados: {cancelados}")
    print("-"*40)
    print(f"A hipótese de que datas de entrega nulas são APENAS de pedidos cancelados é:")
    print(f"👉 {'VERDADEIRA' if hipotese else 'FALSA (Existem pedidos com outros status sem data de entrega)'}")
    print("="*40)