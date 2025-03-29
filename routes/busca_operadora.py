from flask import Blueprint, request, jsonify
from services.busca_operadora import buscar_nome
from utils.logger import setup_logger

busca_operadora_bp = Blueprint('buscar_operadora', __name__)

@busca_operadora_bp.route('/buscar_operadora', methods=['GET'])
def buscar_operadora():
    """
        Busca uma operadora pelo nome no banco de dados.

        Parâmetros:
            - nome (query string): Nome da operadora a ser buscada.

        Retorno:
            - 200 OK: JSON com os resultados encontrados.
            - 400 Bad Request: Se o parâmetro 'nome' não for fornecido.
            - 500 Erro Interno: Se ocorrer um erro no processamento.
    """
    logger = setup_logger("buscar_operadora")

    try:
        nome = request.args.get('nome')
        if not nome:
            return jsonify({"erro": "O parâmetro 'nome' é obrigatório."}), 400

        resultados = buscar_nome(nome)
        return jsonify(resultados), 200

    except Exception as e:
        logger.error(f"Erro ao buscar operadora: {e}")
        return jsonify({"erro": "Erro interno no servidor"}), 500