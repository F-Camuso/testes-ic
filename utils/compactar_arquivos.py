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
