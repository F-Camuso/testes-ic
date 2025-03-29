import requests
from bs4 import BeautifulSoup
import re
import os
import zipfile
import pandas as pd
from utils.conexao import setup_database

def processamento_operadoras():
    """
    Função para coletar os arquivos do FTP/PDA, fazer o download da lista de operadoras e as despesas dos 2 ultimos anos
    Depois é criado um banco de dados para armazenar as informações baixadas e tratadas das duas tabelas

    Retorno:
        linhas_inseridas_demo (int): Quantidade de linhas adicionadas na tabela das despesas 
        linhas_inseridas_operadoras (int): Quantidade de linhas adicionadas na tabela das operadoras
    """
    connection = setup_database()
    if connection is None:
        print("Falha na conexão com o banco de dados.")
        return
    
    # Tabela das contas
    cursor = connection.cursor()
    url_base = 'https://dadosabertos.ans.gov.br/FTP/PDA/demonstracoes_contabeis/'
    lista_anos = lista_diretorios(url_base, 'ano')
    ultimos_anos = lista_anos[-2:]
    caminho_zip = "./data/demo_contabeis_zip"
    caminho_csv = "./data/demo_contabeis_descompactado"
    
    for ano in ultimos_anos:
        url_ano = url_base + ano
        arquivos_zip = lista_diretorios(url_ano, 'zip')
        for zip in arquivos_zip:
            url_zip = url_ano + zip
            caminho_arquivo_baixado = download_arquivos(url_zip, caminho_zip)
            descompacta_arquivos(caminho_arquivo_baixado, caminho_csv)
    
    df_demo_contabeis = adiciona_csv_df(caminho_csv)

    with open('./utils/scriptsSQL/insercao_demonstracoes_contabeis.sql', 'r') as file:
        query_demo_contabeis = file.read()
    
    dados_demo_contabeis = []
    for row in df_demo_contabeis.itertuples(index=False, name=None):
        dados_demo_contabeis.append(tuple(row))
    insere_lotes(connection, cursor, query_demo_contabeis, dados_demo_contabeis) # inserção em lotes pra evitar timeout no execute
    linhas_inseridas_demo = cursor.rowcount()
    cursor.close()
    connection.close()

    # Tabela das operadoras
    cursor = connection.cursor()
    url_segunda_tabela = 'https://dadosabertos.ans.gov.br/FTP/PDA/operadoras_de_plano_de_saude_ativas/'
    pagina = requests.get(url_segunda_tabela)
    soup = BeautifulSoup(pagina.text,'html.parser')
    for a in soup.find_all('a', href=True):
        href = a['href']
        if '.csv' in href:
            url_csv = url_segunda_tabela + href
            csv_baixado = download_arquivos(url_csv, './data/operadoras_ativas')
    
    df = pd.read_csv(csv_baixado, delimiter=';', encoding='utf-8', dtype=object)
    df['Numero'] = df['Numero'].str.replace(r'\.0$', '', regex=True)
    df['Numero'] = df['Numero'].str.replace('.', '', regex=False)
    df = df.fillna('')
    
    with open('./utils/scriptsSQL/insercao_relatorio_cadop.sql', 'r') as file:
        query = file.read()

    dados = []
    for row in df.itertuples(index=False, name=None):
        dados.append(tuple(row))
    cursor.executemany(query, dados)
    connection.commit()
    linhas_inseridas_operadoras = cursor.rowcount
    cursor.close()

    return linhas_inseridas_demo, linhas_inseridas_operadoras
    
def insere_lotes(connection, cursor, query, data, tamanho_lote=1000):
    """
        Função que insere dados em lotes no banco de dados, utilizando um tamanho de lote configurável.

        Parâmetros:
            connection (objeto): Conexão ativa com o banco de dados.
            cursor (objeto): Cursor associado à conexão para executar as operações no banco.
            query (str): Comando SQL para inserir os dados.
            data (list): Lista contendo os dados a serem inseridos no banco.
            tamanho_lote (int): Tamanho do lote de dados a ser inserido de cada vez. O padrão é 1000.

        Retorno:
            None: A função realiza a inserção dos dados diretamente no banco de dados.
    """
    for i in range(0, len(data), tamanho_lote):
        batch = data[i:i+tamanho_lote]
        cursor.executemany(query, batch)
        connection.commit()

def adiciona_csv_df(diretorio):
    """
    Função que percorre arquivos CSV em um diretório, realiza o processamento dos dados e retorna um DataFrame consolidado.

    Parâmetros:
        diretorio (str): Caminho do diretório onde os arquivos CSV estão localizados.

    Retorno:
        pd.DataFrame: DataFrame consolidado contendo os dados processados de todos os arquivos CSV no diretório.
    """ 
    df_completo = pd.DataFrame()
    for arquivo in os.listdir(diretorio):
        if arquivo.endswith('.csv'):
            caminho_arquivo = os.path.join(diretorio, arquivo)
            df = pd.read_csv(caminho_arquivo, delimiter=';', encoding='utf-8', dtype=object)
            df['VL_SALDO_INICIAL'] = df['VL_SALDO_INICIAL'].str.replace(',', '.').astype(float)
            df['VL_SALDO_FINAL'] = df['VL_SALDO_FINAL'].str.replace(',', '.').astype(float)
            df['REG_ANS'] = df['REG_ANS'].astype(str).str.zfill(6)
            if df['DATA'].str.contains(r'\d{2}/\d{2}/\d{4}', na=False).any():
                df['DATA'] = pd.to_datetime(df['DATA'], format='%d/%m/%Y').dt.strftime('%Y-%m-%d')
            df_completo = pd.concat([df_completo, df], ignore_index=True)

    return df_completo

def lista_diretorios(url, tipo):
    """
    Função que realiza o scraping de uma página para listar diretórios ou arquivos com base no tipo solicitado.
    
    Parâmetros: 
        url (str): URL da página a ser processada para buscar os links.
        tipo (str): Tipo de filtro a ser aplicado. Pode ser:
            - 'ano': Filtra e retorna apenas diretórios de ano (ex: '2022/').
            - 'zip': Filtra e retorna apenas arquivos com a extensão '.zip'.

    Retorno:
        list: Uma lista com os diretórios ou arquivos encontrados, conforme o tipo solicitado.
    """
    diretorios = []
    ano_regex = re.compile(r'^\d{4}/$')
    pagina = requests.get(url)    
    soup = BeautifulSoup(pagina.text, 'html.parser')
    for a in soup.find_all('a', href=True):
        href = a['href']
        if tipo == 'ano':
            if ano_regex.match(href):
                diretorios.append(href)
        if tipo == 'zip':
            if href.endswith('.zip'):
                diretorios.append(href)

    return diretorios

def download_arquivos(url, caminho_pasta):
    """
    Função que realiza o download de um arquivo a partir de uma URL e o salva em um diretório local.

    Parâmetros:
        url (str): URL do arquivo a ser baixado.
        caminho_pasta (str): Caminho do diretório onde o arquivo será salvo.

    Retorno:
        str: Caminho completo do arquivo baixado.
    """

    caminho_arquivo = os.path.join(caminho_pasta, os.path.basename(url))
    response = requests.get(url)

    os.makedirs(caminho_pasta, exist_ok=True)
    with open(caminho_arquivo, 'wb') as file:
        file.write(response.content)
    return caminho_arquivo

def descompacta_arquivos(caminho_arquivos, caminho_extracao):
    """
    Função que descompacta um arquivo ZIP em um diretório específico.

    Parâmetros:
        caminho_arquivos (str): Caminho do arquivo ZIP a ser extraído.
        caminho_extracao (str): Diretório onde os arquivos serão extraídos.

    Retorno:
        None
    """
    os.makedirs(caminho_extracao, exist_ok=True)
    with zipfile.ZipFile(caminho_arquivos, 'r') as zip_ref:
        zip_ref.extractall(caminho_extracao)