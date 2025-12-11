from flask import Blueprint
from flask import jsonify, request
from db import criar_conexao
from flask_jwt_extended import jwt_required, get_jwt_identity

views_bp = Blueprint("views", __name__, url_prefix="/games")

@views_bp.route('', methods = ['GET'])
@jwt_required()
def get_games():
    current_user = get_jwt_identity()
    con = criar_conexao()
    cursor = con.cursor(dictionary=True)

    cursor.execute("SELECT * FROM games")
    games = cursor.fetchall()

    cursor.close()
    con.close()
    print(games)
    return jsonify(games), 200

@views_bp.route('/<int:id>', methods = ['GET'])
def get_game(id):


    con = criar_conexao()
    cursor = con.cursor(dictionary=True)

    cursor.execute("SELECT * FROM games WHERE game_id = %s ", (id,))
    game = cursor.fetchall()

    cursor.close()
    con.close()
    
    if len(game) == 0:
        return jsonify({"msg":"Game not found"}), 404
    return jsonify(game[0]), 200

@views_bp.route('', methods=['POST'])
def add_games():
    dados = request.json

    if not dados.get("game_name") or not dados.get("game_slug"):
        return jsonify({"msg":"Dados faltando"}), 400

    game_name = dados.get("game_name")
    game_slug = dados.get("game_slug")
    launch_date = dados.get("launch_date")

    con = criar_conexao()
    cursor = con.cursor()

    sql = "INSERT INTO games (game_name, game_slug, launch_date) VALUES (%s, %s, %s)"
    cursor.execute(sql, (game_name, game_slug, launch_date))
    con.commit()

    new_id = cursor.lastrowid

    cursor.close()
    con.close()

    return jsonify({"game_id" : new_id,"game_name": game_name, "game_slug": game_slug, "launch_date": launch_date}), 201

@views_bp.route('/<int:id>', methods=['PUT'])
def update_game(id): 


    dados = request.json
    game_name = dados.get("game_name")
    game_slug = dados.get("game_slug")
    launch_date = dados.get("launch_date")
    
    con = criar_conexao()
    cursor = con.cursor()

    cursor.execute("SELECT * FROM games WHERE game_id = %s ", (id,))
    game = cursor.fetchall()

    if len(game) == 0:
        return jsonify({"msg":"Game not found"}), 404

    sql = "UPDATE games SET game_name = %s, game_slug = %s, launch_date = %s WHERE game_id = %s"
    cursor.execute(sql, (game_name, game_slug, launch_date, id))
    con.commit()

    cursor.close()
    con.close()

    return jsonify({"game_id": id, "game_name": game_name, "game_slug": game_slug, "launch_date": launch_date}), 200

@views_bp.route('/<int:id>', methods=['DELETE'])
def delete_game(id): 
    
 

    con = criar_conexao()
    cursor = con.cursor()

    cursor.execute("SELECT * FROM games WHERE game_id = %s ", (id,))
    game = cursor.fetchall()

    if len(game) == 0:
        return jsonify({"msg":"Game not found"}), 404

    sql = "DELETE FROM games WHERE game_id=%s"
    cursor.execute(sql, (id,))
    con.commit()

    cursor.close()
    con.close()

    return '', 204