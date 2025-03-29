import requests
from bs4 import BeautifulSoup
from utils.logger import setup_logger
import os

def baixar_arquivos(url, name): 
    """
    Baixa um arquivo da URL fornecida e o salva no diretório informado.

    Parâmetros:
        url (str): URL do arquivo que será baixado.
        name (str): Nome do arquivo a ser salvo no diretório.

    Retorno:
        str: Caminho do arquivo salvo no sistema.
    """
    logger = setup_logger("web_scraping")

    response = requests.get(url)
    file_path = f'./data/teste1/{name}'
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'wb') as file:
        file.write(response.content)
    logger.info(f"Download do arquivo '{name}' feito com sucesso.")

    return file_path


def realizar_scraping(url):
    """
    Função que realiza o scraping da página e faz o download dos arquivos PDF solicitados.
    
    Parâmetros: 
        url (str): URL do site para fazer o scraping.

    Retorno:
        list: Uma lista com o caminho dos arquivos baixados.
    """
    logger = setup_logger("web_scraping")
    pagina = requests.get(url)
    soup = BeautifulSoup(pagina.text, 'html.parser')
    links = soup.find_all('a', href=True) # Busca todos os links do site
    
    arquivos_baixados = []
    for link in links: # Para cada link, verificar se existe a palavra Anexo e se é um pdf
        href = link['href']
        text = link.get_text().replace('.', '') # Limpeza do nome
        if 'Anexo' in text and href.endswith('.pdf'): 
            logger.info(f"Arquivo {text} encontrado na página")
            caminho = baixar_arquivos(href, f'{text}.pdf')
            arquivos_baixados.append(caminho)
    
    return arquivos_baixados
