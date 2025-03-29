from utils.conexao import get_connection
from utils.logger import setup_logger
def buscar_nome(nome):
    """
        Busca uma operadora pelo nome no banco de dados.

        Parâmetros:
            - nome (query string): Nome da operadora a ser buscada.

        Retorno:
            - JSON com os resultados encontrados ou erro se o parâmetro 'nome' não for fornecido.
    """
    
    logger = setup_logger("busca_operadora")

    connection = get_connection("ftp_pda")
    cursor = connection.cursor(dictionary=True)
    query = "SELECT cnpj, razao_social as Operadora FROM relatorio_cadop WHERE razao_social LIKE %s"
    cursor.execute(query, (f"%{nome.upper()}%",))
    resultados = cursor.fetchall()
    
    logger.info(f"Resultados da busca por {nome}:\n{resultados}")
    cursor.close()
    connection.close()
    return resultados