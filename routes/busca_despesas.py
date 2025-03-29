from flask import Blueprint, request, jsonify
from services.busca_despesas import buscar_despesas

busca_despesas_bp = Blueprint('busca_despesas', __name__)

@busca_despesas_bp.route('/buscar_despesas', methods=['GET'])
def buscar_despesas_route():
    """
        Busca as despesas das operadoras com base no número de meses informado.

        Parâmetros:
            - meses (query string): Número de meses para calcular as despesas.

        Retorno:
            - JSON com os resultados encontrados.
    """
    meses = request.args.get('meses')

    resultados = buscar_despesas(meses)
    return jsonify(resultados), 200