import mysql.connector
import os

def get_connection(database=None):
    """
    Função para estabelecer a conexão com o banco de dados.

    Retorno:
        connection (mysql.connector.connection.MySQLConnection): Conexão ativa com o banco de dados.
    """
    connection = mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=database if database else None
    )
    
    if connection.is_connected():
        print("MySQL conectado")
    
    return connection


def setup_database():
    """
    Função que configura o banco de dados executando um script SQL.

    Retorno:
        connection (mysql.connector.connection.MySQLConnection): Conexão ativa com o banco de dados.
    """
    connection = get_connection()  # Obtém a conexão ativa
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