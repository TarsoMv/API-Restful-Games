from flask import Blueprint
from flask import jsonify, request
from db import db_decorator
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

views_bp = Blueprint("views", __name__, url_prefix="/games")

@views_bp.route('', methods = ['GET'])
@jwt_required()
@db_decorator
def get_games(cursor):
    cursor.execute("SELECT * FROM games")
    games = cursor.fetchall()
 

    print(games)
    return jsonify(games), 200

@views_bp.route('/<int:id>', methods = ['GET'])
@jwt_required()
@db_decorator
def get_game(cursor, id):
    cursor.execute("SELECT * FROM games WHERE game_id = %s ", (id,))
    game = cursor.fetchone()
    
    if not game:
        return jsonify({"msg":"Game not found"}), 404
    return jsonify(game), 200

@views_bp.route('', methods=['POST'])
@jwt_required()
@db_decorator
def add_games(cursor):
    dados = request.json

    if not dados.get("game_name") or not dados.get("game_slug"):
        return jsonify({"msg":"Dados faltando"}), 400

    game_name = dados.get("game_name")
    game_slug = dados.get("game_slug")  
    launch_date = dados.get("launch_date")

    
    sql = "INSERT INTO games (game_name, game_slug, launch_date) VALUES (%s, %s, %s)"
    cursor.execute(sql, (game_name, game_slug, launch_date))
    

    new_id = cursor.lastrowid


    return jsonify({"game_id" : new_id,"game_name": game_name, "game_slug": game_slug, "launch_date": launch_date}), 201

@views_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
@db_decorator
def update_game(cursor, id):
    dados = request.get_json(silent=True)
    if not dados:
        return jsonify({"msg": "JSON inválido ou ausente"}), 400

    cursor.execute("SELECT * FROM games WHERE game_id = %s", (id,))
    if not cursor.fetchone():
        return jsonify({"msg": "Game not found"}), 404

    campos = []
    valores = []

    if "game_name" in dados:
        campos.append("game_name = %s")
        valores.append(dados["game_name"])

    if "game_slug" in dados:
        campos.append("game_slug = %s")
        valores.append(dados["game_slug"])

    if "launch_date" in dados:
        campos.append("launch_date = %s")
        valores.append(dados["launch_date"])

    if not campos:
        return jsonify({"msg": "Nenhum campo para atualizar"}), 400

    sql = f"""
        UPDATE games
        SET {', '.join(campos)}
        WHERE game_id = %s
    """
    valores.append(id)
    cursor.execute(sql, tuple(valores))

    return jsonify({"msg": "Game atualizado com sucesso"}), 200


@views_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
@db_decorator
def delete_game(cursor, id): 
    user = get_jwt_identity()
    claims = get_jwt()
    role = claims["role"]

    if role != 'ADMIN': 
        return {"message": "Forbidden"}, 401
 


    cursor.execute("SELECT * FROM games WHERE game_id = %s ", (id,))
    game = cursor.fetchall()

    if len(game) == 0:
        return jsonify({"msg":"Game not found"}), 404

    sql = "DELETE FROM games WHERE game_id=%s"
    cursor.execute(sql, (id,))
    
    return '', 204