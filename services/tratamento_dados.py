import pdfplumber
import csv
import re
import os

def processar_pdf():
    """
    Processa o PDF Anexo I, extraindo as tabelas e gerando um CSV.

    Retorno:
        - str: Caminho do csv para ser compactado.
    """
    pdf_path = './data/teste1/Anexo I.pdf'
    csv_path = './data/teste2/tabela_rol_procedimentos_saude.csv'
    
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)
    
    dicionario = coleta_legenda(pdf_path) # Criação do dicionario utilizado para troca de siglas

    with pdfplumber.open(pdf_path) as pdf: # Coleta do PDF com o pdfplumber
        with open(csv_path, mode='w', newline='', encoding='utf-8') as file:  
            writer = csv.writer(file)
            cabecalho_preenchido = False # Flag para indicar que o header já foi preenchido
            for page in pdf.pages:
                tables = page.extract_tables() # Coleta da tabela na página
                for table in tables:
                    if not cabecalho_preenchido: # Prenchimento do header
                        writer.writerow(table[0])
                        cabecalho_preenchido = True
                    for row in table[1:]:  # Coleta das linhas da tabela a partir da segunda celula, ignorando o header
                        row_substituida = troca_siglas(dicionario, row, table[0])
                        writer.writerow(row_substituida) # Escrita da row depois de fazer a troca da sigla onde existir OD ou AMB

    return [csv_path]

def troca_siglas(dicionario, linha, cabecalho):
    """
    Substitui siglas encontradas na tabela pelos seus significados.

    Parâmetros:
        - dicionario (dict): Dicionário de siglas e seus significados.
        - linha (list): Linha da tabela a ser processada.
        - cabecalho (list): Cabeçalho da tabela para encontrar as colunas certas.

    Retorno:
        - list: Linha com as siglas substituídas.
    """
    # Coleta o número da coluna onde está OD e em sequencia AMB 
    od_index = cabecalho.index("OD") if "OD" in cabecalho else -1 
    amb_index = cabecalho.index("AMB") if "AMB" in cabecalho else -1
    
    # Substituição das siglas pelo seus valores correspondentes de acordo com o dicionario
    if od_index != -1:
        linha[od_index] = dicionario.get(linha[od_index])  
    if amb_index != -1:
        linha[amb_index] = dicionario.get(linha[amb_index])
    
    return linha

def dicionario_legenda(texto):
    """
    Constrói um dicionário de siglas e significados extraídos da legenda do PDF.

    Parâmetros:
        - texto (str): Texto contendo as siglas e seus significados.

    Retorno:
        - dict: Dicionário de siglas e seus significados.
    """
    # Os grupos coletados são: as siglas e tudo que está entre 2 siglas (significado)
    # sigla -> ([A-Z]{2,3}):
    # significado -> (.*?)
    regex = r"([A-Z]{2,3}):\s(.*?)(?=\s[A-Z]{2,3}:|$)"
    matches = re.findall(regex, texto)
    
    dicionario = {}
    for sigla, significado in matches: # Para cada grupo, coleta a sigla e o significado, além de remover os espaços em branco do significado. 
        dicionario[sigla] = significado.strip()
    
    return dicionario

def coleta_legenda(pdf_path):
    """
    Extrai a legenda do PDF e retorna um dicionário de siglas.

    Parâmetros:
        - pdf_path (str): Caminho do arquivo PDF.

    Retorno:
        - dict: Dicionário de siglas e significados.
    """
    with pdfplumber.open(pdf_path) as pdf:
        for pagina in pdf.pages:
            texto = pagina.extract_text() # Extrai o texto do pdf até encontrar "Legenda:"
            if texto and 'Legenda:' in texto:
                index_legenda = texto.find('Legenda: ') # O texto_legendas vai ser preenchido com tudo que começa após a Legenda:
                texto_legendas = texto[index_legenda + len('Legenda:'): -2].strip() #     e termina no penultimo index da página 
                dicionario = dicionario_legenda(texto_legendas)
                return dicionario
    return {}