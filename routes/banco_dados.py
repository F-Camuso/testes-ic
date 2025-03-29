from flask import Blueprint, request, jsonify
from services.banco_dados import processamento_operadoras

execucao_processamento_bp = Blueprint('execucao_processamento', __name__)

@execucao_processamento_bp.route('/execucao_processamento', methods=['GET'])
def execucao_processamento():
    """
    Endpoint para processar configurar um banco, extrair dados de CSVs baixados dos sites 
    e inserir esses valores em duas tabelas.

    Requisição:
        - Método: GET

    Retornos:
        - 200 OK: Se o processamento for bem-sucedido e os arquivos forem compactados.
        
    """
    linhas_inseridas_demo, linhas_inseridas_operadoras = processamento_operadoras()

    # Retorna as quantidades de linhas inseridas no formato JSON
    return jsonify({
        'linhas_inseridas_demo': linhas_inseridas_demo,
        'linhas_inseridas_operadoras': linhas_inseridas_operadoras
    }), 200