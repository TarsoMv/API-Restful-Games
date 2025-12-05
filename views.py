from app import app
from flask import jsonify, request
from db import criar_conexao

@app.route('/games', methods = ['GET'])
def get_games():
    con = criar_conexao()
    cursor = con.cursor(dictionary=True)

    cursor.execute("SELECT * FROM games")
    games = cursor.fetchall()

    cursor.close()
    con.close()
    print(games)
    return jsonify(games), 200

@app.route('/games/<int:id>', methods = ['GET'])
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

@app.route('/games', methods=['POST'])
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

@app.route('/games/<int:id>', methods=['PUT'])
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

@app.route('/games/<int:id>', methods=['DELETE'])
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