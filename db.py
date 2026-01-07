import os
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error
from functools import wraps

load_dotenv()


def criar_conexao():
    try: 
        con=mysql.connector.connect(
            host = os.environ["host"],
            user = os.environ["user"],
            password = os.environ["password"],
            database= os.environ["database"]
        )
        return con
    except Error as e: 
        print("Erro ao conectar ao SGBD:", e)
        return None
    
def db_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        con = criar_conexao()
        if not con:
            raise RuntimeError("Falha ao realizar conexão com o banco de dados")
        

        cursor = con.cursor(dictionary=True)
        try:
            result = func(cursor, *args, **kwargs)
            con.commit() 
            return result
        except Exception as e:
            con.rollback()
            raise e
        
        finally:
            cursor.close()
            con.close()

    return wrapper 
        
