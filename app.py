from flask import Flask,request,Response
import chess

app = Flask(__name__)

@app.route('/')
def play():
    board = chess.Board()
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

    chess.Move(casilla_inicio,casilla_destino,promotion= chess.QUEEN if promotion else None)