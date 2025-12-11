import bcrypt
from db import criar_conexao

con = criar_conexao()
cursor = con.cursor()

password = b"ADMIN"
hashed = bcrypt.hashpw(password, bcrypt.gensalt())

userAdmin = {
    "username" : "AdminAPI",
    "role" : "ADMIN",
    "passwordHashed" : hashed
} 

print(userAdmin["passwordHashed"])

sql = "INSERT INTO users (username, role, password) VALUES (%s, %s, %s)"

cursor.execute(sql, (userAdmin["username"], userAdmin["role"], userAdmin["passwordHashed"]))
con.commit()

cursor.close()
con.close()

#INSERT INTO games (game_name, game_slug, launch_date) VALUES (%s, %s, %s)