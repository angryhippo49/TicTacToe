from flask import Flask, request, jsonify, send_file
from backend import create_board, update_board, is_game_over, computer_move
from typing import List
import os

app = Flask(__name__)
board = create_board()  # global board lives here

@app.route('/create_new_board', methods=['POST'])
def create_new_board():
    global board
    board = create_board()
    return jsonify(board)


@app.route('/')
def serve_frontend():
    return send_file(os.path.abspath("frontend/frontend.html"))


@app.route('/make_move', methods=['POST'])
def make_move():
    global board
    data = request.get_json()
    row = data['row']
    col = data['col']
    player = data['player']
    print(data)
    
    update_board(board, (row, col), player)

    # Only let computer move if game isn't over
    if not is_game_over(board):
        computer_move(board, 'X', 'O', 'Yes')
    else:
        # somehow render "game over" messag
        return jsonify({"message": "Game Over", "board": board})

    return jsonify(board)


if __name__ == '__main__':
    app.run(debug=True)