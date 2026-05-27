# Pipeline de Sanitização de Dados - E-commerce Olist

Este projeto foi desenvolvido como o Mini-Projeto Avaliativo do Módulo 1 (Semana 07) do curso de Machine Learning e Visão Computacional. O objetivo principal é construir um pipeline de extração, tratamento e carregamento de dados (ETL) utilizando estritamente recursos nativos da linguagem Python, sem o auxílio de bibliotecas externas como o Pandas.

## Descrição do Projeto
No cenário atual, empresas líderes em e-commerce, como a Olist, lidam diariamente com milhões de transações estruturadas. Contudo, dados do mundo real são notoriamente conhecidos por serem ruidosos, incompletos ou mal formatados. 

Este script foi desenvolvido para atuar como um Analista de Dados Júnior, resolvendo inconsistências em lotes extraídos do banco de dados oficial (`olist_products_dataset.csv` e `olist_orders_dataset.csv`) que estavam travando os relatórios automatizados da empresa.

### Tarefas Técnicas Implementadas:
1. **Validação e Tratamento de Dados Ausentes:** Identificação de valores nulos na coluna de categorias de produtos e preenchimento com o termo padrão "Sem Categoria".
2. **Regra de Corte Logística:** Eliminação de registros com dimensões físicas ausentes, visando a proteção de cálculos de frete.
3. **Padronização de Strings com Regex:** Conversão de textos para letras minúsculas, remoção de espaçamentos excedentes (`.strip()`) e limpeza de caracteres especiais por meio de expressões regulares (módulo `re`).
4. **Validação de Regra de Negócio:** Análise condicional das datas de entrega vazias para validar a hipótese comercial sobre pedidos cancelados.
5. **Formatação Temporal:** Conversão de strings de data para o formato simplificado brasileiro (`DD/MM/YYYY`) via módulo `datetime`.
6. **Sumário Estatístico:** Exibição em tela de uma contagem manual detalhada das linhas processadas, nulos corrigidos e status mapeados.

---

## Guia de Execução

### Pré-requisitos
* Ter o Python 3.x instalado em sua máquina.
* Garantir que os arquivos de dados brutas (`olist_products_dataset.csv` e `olist_orders_dataset.csv`) estejam localizados na mesma pasta dos scripts Python.

### Como Rodar o Projeto no VS Code
1. Abra a pasta do projeto no VS Code (**File > Open Folder...**).
2. Abra o terminal integrado do sistema.
3. Certifique-se de que o terminal está apontando para o diretório correto dos arquivos.
4. Execute o pipeline com o comando abaixo:
   ```bash
   python main.py

---

# Reflexão Teórica sobre Machine Learning
A higienização e o tratamento prévio de dados brutos são etapas indispensáveis para o sucesso de modelos preditivos, evitando o famoso problema do Garbage In, Garbage Out (Lixo Entra, Lixo Sai). Quando algoritmos de Machine Learning são alimentados com dados ruidosos, incompletos ou mal formatados, eles tendem a aprender correlações falsas. Isso resulta diretamente em problemas críticos como o Overfitting — onde o modelo decora os erros da base de treino e perde a capacidade de generalizar para o mundo real — ou o Underfitting, que ocorre quando a IA é incapaz de aprender até mesmo as regras básicas devido à inconsistência dos dados.  

A aplicação de regras de negócio sólidas e padronizações técnicas (como o uso de Expressões Regulares e tratamento de datas) blinda a infraestrutura lógica de dados da empresa. No caso de grandes eventos de varejo como a Black Friday, decisões operacionais cruciais — tais como o descarte de registros sem dimensões físicas para proteger o cálculo real de frete — garantem previsões consistentes e evitam vieses estatísticos indesejados. Dessa forma, um pipeline automatizado de sanitização é o que assegura tomadas de decisão automatizadas precisas, seguras e financeiramente viáveis. 