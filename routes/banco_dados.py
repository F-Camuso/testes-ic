from flask import Blueprint, jsonify
from services.banco_dados import processamento_operadoras
from utils.logger import setup_logger

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
        - 500 Erro Interno: Se ocorrer algum erro no processamento.
        
    """
    logger = setup_logger("execucao_processamento")
    try:
        linhas_inseridas_demo, linhas_inseridas_operadoras = processamento_operadoras()

        return jsonify({
            'linhas_inseridas_demo': linhas_inseridas_demo,
            'linhas_inseridas_operadoras': linhas_inseridas_operadoras
        }), 200

    except Exception as e:
        logger.error(f"Erro no processamento: {e}")
        return jsonify({'error': 'Erro interno no servidor'}), 500