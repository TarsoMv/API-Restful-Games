from flask import jsonify, request, Blueprint
from flask_jwt_extended import create_access_token
import bcrypt
from db import db_decorator

login_bp = Blueprint("login", __name__, url_prefix="/auth")

#Colocar verificação com banco de dados MYSQL

@login_bp.route("/login", methods=["POST"])
@db_decorator
def login(cursor):
    username = request.json.get("username", None)
    password = request.json.get("password", None)

    if not username or not password: 
        return jsonify({"msg": "Username and Password are required"}), 400
   
    cursor.execute("SELECT userid, username, password, role FROM users WHERE username = %s ", (username,))
    user = cursor.fetchone()


    if not user:
        return jsonify({"msg": "Bad username or password"}), 401


    stored_username = user["username"]
    stored_hash = user["password"]
    role = user["role"]
    userid = user["userid"]

    if username == stored_username and bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8')): 
        access_token = create_access_token(
            identity=str(userid),
            additional_claims={"role":str(role)}
            )
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"msg": "Bad username or password"}), 401

    