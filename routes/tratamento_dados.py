from flask import Blueprint, request, jsonify
from services.tratamento_dados import processar_pdf
from utils.arquivos import compactar_arquivos
from utils.logger import setup_logger
tratamento_dados_bp = Blueprint('tratamento_dados', __name__)

@tratamento_dados_bp.route('/tratamento_dados', methods=['GET'])
def tratamento_dados():
    """
    Endpoint para processar um arquivo PDF, extraindo tabelas e gerando um CSV.

    Requisição:
        - Método: GET
        - queryParam:
            - name (str): Nome a ser colocado no zip Teste_{seu_nome}.

    Retornos:
        - 200 OK: Se o processamento for bem-sucedido e os arquivos forem compactados.
        - 400 Bad Request: Se o nome não for fornecido.
        - 500 Erro Interno: Se ocorrer um erro durante o processamento.
    """

    logger = setup_logger("tratamento_dados")
    try:
        name = request.args.get('name')

        if not name:
            return jsonify({"erro": "Nome não fornecido."}), 400

        lista_csv = processar_pdf()

        if lista_csv:
            compactar_arquivos(f'./data/teste2/Teste_{name}.zip', lista_csv)
            return jsonify({"mensagem": "Processamento concluído com sucesso."}), 200
        else:
            return jsonify({"erro": "Falha ao processar o CSV."}), 500

    except Exception as e:
        logger.error(f"Erro ao buscar despesas: {e}")
        return jsonify({'error': 'Erro interno no servidor'}), 500