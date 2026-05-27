import csv
import re
from datetime import datetime

def limpar_categoria(nome_categoria):
    """
    Padroniza strings: minúsculas, remove espaços extras e limpa caracteres especiais.
    """
    if not nome_categoria:
        return "Sem Categoria"
    
    # Converte para minúsculas e remove espaços no início/fim
    nome_limpo = nome_categoria.lower().strip()
    
    # Mantém apenas letras, números e underlines (substitui o resto por nada)
    nome_limpo = re.sub(r'[^a-z0-9_\s]', '', nome_limpo)
    
    return nome_limpo

def tratar_dimensoes_fisicas(registro):
    """
    Trata valores nulos para dimensões físicas.
    Estratégia adotada: Descarte do registro caso peso ou dimensões estejam vazios.
    Justificativa: Para logística e cálculo de frete (Black Friday), dados zerados 
    ou fictícios (médias) gerariam prejuízo real no cálculo do frete.
    """
    chaves_dimensoes = [
        'product_weight_g', 'product_lenght_cm', 
        'product_height_cm', 'product_width_cm'
    ]
    
    for chave in chaves_dimensoes:
        if not registro.get(chave) or registro[chave].strip() == "":
            return None # Sinaliza que o registro deve ser descartado
            
    return registro

def formatar_data_br(string_data):
    """
    Converte a data de "YYYY-MM-DD HH:MM:SS" para "DD/MM/YYYY".
    """
    if not string_data or string_data.strip() == "":
        return "Data não disponível"
    try:
        # Converte a string original para objeto datetime
        data_obj = datetime.strptime(string_data, "%Y-%m-%d %H:%M:%S")
        # Retorna formatado no padrão brasileiro
        return data_obj.strftime("%d/%m/%Y")
    except ValueError:
        return string_data

def validar_hipotese_cancelado(status_pedido, data_entrega):
    """
    Verifica se a ausência de data de entrega se deve estritamente ao cancelamento.
    """
    # Se a data está vazia e o status NÃO é cancelado
    if (not data_entrega or data_entrega.strip() == "") and status_pedido != "canceled":
        return False # Hipótese refutada para este registro específico
    return True