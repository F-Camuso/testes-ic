from flask import Blueprint, request, jsonify
from services.busca_despesas import buscar_despesas
from utils.logger import setup_logger

busca_despesas_bp = Blueprint('busca_despesas', __name__)

@busca_despesas_bp.route('/buscar_despesas', methods=['GET'])
def buscar_despesas_route():
    """
        Busca as despesas das operadoras com base no número de meses informado.

        Parâmetros:
            - meses (query string): Número de meses para calcular as despesas.

        Retorno:
            - 200 OK: JSON com os resultados encontrados.
            - 400 Bad Request: Se o parâmetro 'meses' não for informado.
            - 500 Erro Interno: Se ocorrer um erro no processamento.
    """
    logger = setup_logger("buscar_despesas")
    try:
        meses = request.args.get('meses')
        if not meses:
            return jsonify({'error': "O parâmetro 'meses' é obrigatório"}), 400

        resultados = buscar_despesas(meses)
        return jsonify(resultados), 200

    except Exception as e:
        logger.error(f"Erro ao buscar despesas: {e}")
        return jsonify({'error': 'Erro interno no servidor'}), 500