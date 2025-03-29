import requests
import os
import zipfile

def compactar_arquivos(nome_zip, arquivos):
    """
    Função que realiza o scraping da página e faz o download dos arquivos PDF solicitados.
    
    Retorno:
        list: Uma lista com o caminho dos arquivos baixados.
    """
    with zipfile.ZipFile(nome_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for arquivo in arquivos:
            zipf.write(arquivo, arcname=arquivo.split('/')[-1])

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