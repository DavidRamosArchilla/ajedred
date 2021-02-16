from flask import Flask,request,Response
import chess
from inteligencia import Ia
app = Flask(__name__)
board = chess.Board()

@app.route('/')
def play():
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
    casilla_inicio = request.args.get('from')
    casilla_destino = request.args.get('to')
    promotion = request.args.get('promotion') == 'true'
    movimiento_str = f'{casilla_inicio}{casilla_destino}'
    # movimiento = chess.Move(casilla_inicio,casilla_destino,promotion= chess.QUEEN if promotion else None)
    movimiento = chess.Move.from_uci(movimiento_str)
    movimiento.promotion = chess.QUEEN if promotion else None
    print(movimiento)
    # print( chess.Move.from_uci(movimiento) in board.legal_moves)
    if movimiento in (board.legal_moves):
        board.push(movimiento)
        ia = Ia(board)
        ia_move = ia.best_move(3,chess.BLACK)[1]
        print(ia_move)
        board.push(ia_move)
        if board.is_game_over():
            print('game over')
            return app.response_class(response = "game over",status=200) #app.response_class( response = "game over",status = 201)
        else:
            return app.response_class(response = board.fen(),status=200)
    else:
        print(board)
        return app.response_class(response = board.fen(),status=200)

@app.route('/newgame')
def new_game():
    board.reset()
    return app.response_class(response = chess.STARTING_BOARD_FEN)