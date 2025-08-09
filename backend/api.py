from flask import Flask, request, jsonify, send_file
from backend import create_board, update_board, is_game_over, computer_move_frontend
from typing import List
import os

app = Flask(__name__)
board = create_board()  # global board lives here
ctn = 1


@app.route('/create_new_board', methods=['POST'])
def create_new_board():
    global board
    global ctn
    board = create_board()
    ctn = 1  # Reset move counter for new game
    return jsonify(board)


@app.route('/')
def serve_frontend():
    return send_file(os.path.abspath("frontend/frontend.html"))


@app.route('/make_move', methods=['POST'])
def make_move():
    global board
    global ctn
    data = request.get_json()
    turn = data.get('turn', 'Yes')

    if is_game_over(board):
        return jsonify(board)

    # Handle player move and computer response
    if 'row' in data and 'col' in data and 'player' in data:
        # Player made a move
        row = data['row']
        col = data['col']
        player = data['player']
        update_board(board, (row, col), player)
        
        # Check if game is over after player move
        if is_game_over(board):
            return jsonify({"message": "Game Over", "board": board})
        
        # Make computer move if game isn't over
        computer_move_frontend(board, 'X', 'O', turn, ctn)
        ctn += 1
        
        # Check if game is over after computer move
        if is_game_over(board):
            return jsonify({"message": "Game Over", "board": board})
        
        return jsonify(board)
    elif turn == 'No':
        # Computer goes first (initial computer move)
        computer_move_frontend(board, 'X', 'O', turn, ctn)
        ctn += 1
        
        # Check if game is over after computer move
        if is_game_over(board):
            return jsonify({"message": "Game Over", "board": board})
        
        return jsonify(board)
    else:
        # Just a board update call, return current board
        return jsonify(board)


if __name__ == '__main__':
    app.run(debug=True)