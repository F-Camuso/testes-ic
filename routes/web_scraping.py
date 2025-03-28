from flask import Blueprint, request, jsonify
from services.web_scraping import realizar_scraping
from utils.compactar_arquivos import compactar_arquivos


web_scraping_bp = Blueprint('web_scraping', __name__)

@web_scraping_bp.route('/web_scraping', methods=['POST'])
def web_scraping():
    """
    Endpoint para realizar web scraping e compactar os arquivos baixados.

    Requisição:
        - Método: POST
        - Body (JSON): {"url": "URL do site"}

    Retornos:
        - 200 OK: Web scraping realizado com sucesso.
        - 400 Bad Request: Se a URL não for fornecida.
    """

    url = request.json.get('url')
    
    if not url:
        return jsonify(message="URL não fornecida."), 400
    
    arquivos_baixados = realizar_scraping(url)
    
    if arquivos_baixados:
        compactar_arquivos('./data/teste1/anexos_gov.zip', arquivos_baixados)
        return jsonify(message="Web scraping realizado com sucesso. Arquivos compactados.")
    else:
        return jsonify(message="Nenhum arquivo encontrado para download.")
