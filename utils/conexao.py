import mysql.connector
import os

def setup_database():
    """
    Função que configura o banco de dados executando um script SQL.

    Parâmetros:
        Nenhum.

    Retorno:
        connection (mysql.connector.connection.MySQLConnection): Conexão ativa com o banco de dados.

    Processamento:
        - Conecta ao banco de dados utilizando variáveis de ambiente para as credenciais.
        - Lê o arquivo de configuração SQL e executa os comandos no banco de dados.
        - Retorna a conexão para ser utilizada posteriormente.
    """
    connection = mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD')
    )
    if connection.is_connected():
        print("Mysql conectado")

    cursor = connection.cursor()

    sql_path = './utils/scriptsSQL/configuracao_db.sql'
    with open(sql_path, 'r') as file:
        configuracao_script = file.read()

    comandos = configuracao_script.split(';')
    for comando in comandos:
        comando = comando.strip()
        if comando:
            cursor.execute(comando)

    connection.commit()
    cursor.close()
    
    return connection