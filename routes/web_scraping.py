from flask import Blueprint, request, jsonify
from services.web_scraping import realizar_scraping
from utils.arquivos import compactar_arquivos
from utils.logger import setup_logger

web_scraping_bp = Blueprint('web_scraping', __name__)

@web_scraping_bp.route('/web_scraping', methods=['POST'])
def web_scraping():
    """
    Endpoint para realizar web scraping e compactar os arquivos baixados.

    Requisição:
        - Método: POST
        - Body (JSON): {"url": "URL do site"}

    Retornos:
        - 200 OK: Se o scraping for bem-sucedido e os arquivos forem compactados.
        - 400 Bad Request: Se a URL não for fornecida.
        - 500 Erro Interno: Se ocorrer um erro durante o processamento.
    """
    logger = setup_logger("web_scraping")
    try:
        data = request.get_json()
        url = data.get('url') if data else None

        if not url:
            return jsonify({"erro": "URL não fornecida."}), 400

        arquivos_baixados = realizar_scraping(url)

        if arquivos_baixados:
            compactar_arquivos('./data/teste1/anexos_gov.zip', arquivos_baixados)
            logger.info(f"Arquivos compactados com sucesso")
            return jsonify({"mensagem": "Web scraping realizado com sucesso. Arquivos compactados."}), 200
        else:
            return jsonify({"mensagem": "Nenhum arquivo encontrado para download."}), 404

    except Exception as e:
        logger.error(f"Erro ao buscar despesas: {e}")
        return jsonify({'error': 'Erro interno no servidor'}), 500