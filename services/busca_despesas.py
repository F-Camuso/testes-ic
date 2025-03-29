from utils.conexao import get_connection

def buscar_despesas(meses):
    """
    Função para buscar as 10 operadoras com maiores despesas em X meses.

    Parâmetros:
        meses (str): Quantidade de meses para serem analisados (3 = trimestre, 12 = anual).

    Retorno:
        list[dict]: Lista com as operadoras e suas despesas em X meses.
    """
    connection = get_connection("ftp_pda")
    cursor = connection.cursor()

    sql_path = './utils/scriptsSQL/analise_despesas.sql'
    with open(sql_path, 'r', encoding='utf-8') as file:
        query = file.read()
    
    cursor.execute(query, (meses,))
    resultados = cursor.fetchall()
    cursor.close()
    connection.close()

    return resultados