from os import stat_result
from flask import Flask,request,Response
import chess

app = Flask(__name__)
board = chess.Board()

@app.route('/')
def play():
    
    board_to_html = board_html(board)
    return open("home.html").read()

#no lo uso
def board_to_string(board):
    fen_encoded = board.board_fen()
    parsed=""
    for letter in fen_encoded:
        if letter.isdigit():
            parsed += '_'*int(letter)
        elif letter=='/':
            parsed+='<br>'
        else:
            parsed+=letter
    return parsed

def board_html(board):
    fen_encoded = board.board_fen()
    parsed="<tr>"
    for letter in fen_encoded:
        if letter.isdigit():
            parsed += '<td> <img src="./static/piezas/casilla_blanca.png"/></td>'*int(letter)
        elif letter=='/':
            parsed+='</tr><tr>'
        else:
            parsed+='<td> <img src="./static/piezas/peon_negro.png"/></td>'
    parsed+='</tr>'
    return parsed

@app.route('/move_coordinates')
def move():
    casilla_inicio = int(request.args.get('from'))
    casilla_destino = int(request.args.get('to'))
    promotion = request.args.get('promotion') == 'true'
   
    movimiento = chess.Move(casilla_inicio,casilla_destino,promotion= chess.QUEEN if promotion else None)
    if movimiento in board.legal_moves:
        board.push(movimiento)
        print(board)
        if board.is_game_over():
            print('game over')
            return app.response_class(response = "game over",status=200) #app.response_class( response = "game over",status = 201)
        else:
            return app.response_class(response = board.fen(),status=200)
    else:
        return app.response_class(response = board.fen(),status=200)