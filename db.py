import mysql.connector
from mysql.connector import Error

def criar_conexao():
    try: 
        con=mysql.connector.connect(
            host='localhost',
            user='root',
            password='2080',
            database='games'
        )
        return con
    except Error as e: 
        print("Erro ao conectar ao SGBD:", e)
        return None
