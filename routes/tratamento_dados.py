from flask import Blueprint, request, jsonify
from services.tratamento_dados import processar_pdf
from utils.compactar_arquivos import compactar_arquivos

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
    """
    name = request.args.get('name')

    if not name:
        return jsonify(message="Nome não fornecido."), 400

    lista_csv = processar_pdf()

    if lista_csv:
        compactar_arquivos(f'./data/teste2/Teste_{name}.zip', lista_csv)
        return jsonify(message="Processamento concluído com sucesso.")
    else:
        return jsonify(message="Falha ao processar o csv."), 500