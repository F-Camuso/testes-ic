from flask import Blueprint, request, jsonify
from services.busca_operadora import buscar_nome

busca_operadora_bp = Blueprint('buscar_operadora', __name__)

@busca_operadora_bp.route('/buscar_operadora', methods=['GET'])
def buscar_operadora():
    """
        Busca uma operadora pelo nome no banco de dados.

        Parâmetros:
            - nome (query string): Nome da operadora a ser buscada.

        Retorno:
            - JSON com os resultados encontrados ou erro se o parâmetro 'nome' não for fornecido.
    """
    nome = request.args.get('nome')
    
    if not nome:
        return jsonify({"erro": "O parâmetro 'nome' é obrigatório."}), 400

    resultados = buscar_nome(nome)
    return jsonify(resultados), 200