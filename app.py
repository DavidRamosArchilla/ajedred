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
    is_first_move = (request.args.get('isFirst')) == 'True'
    color = request.args.get('color') # color: 1--> mueven blancas, 0--> mueven negras
    movimiento_str = f'{casilla_inicio}{casilla_destino}'
    # movimiento = chess.Move(casilla_inicio,casilla_destino,promotion= chess.QUEEN if promotion else None)
    if not is_first_move:
        movimiento = chess.Move.from_uci(movimiento_str)
        movimiento.promotion = chess.QUEEN if promotion else None
        print('mov ', movimiento)
    # print( chess.Move.from_uci(movimiento) in board.legal_moves)
    
    if is_first_move or movimiento in (board.legal_moves):
        if not is_first_move:
            board.push(movimiento)
        ia_move = mueve_ia(color)
        if ia_move is None:
            return app.response_class(response = "game over",status=200,headers = {'game_over':True})
        else:
            board.push(ia_move)
        if board.is_game_over():
            print('game over')
            return app.response_class(response = "game over",status=200,headers = {'game_over':True}) #app.response_class( response = "game over",status = 201)
        else:
            return app.response_class(response = board.fen(),status=200,headers={'game_over':False})
    else:
        return app.response_class(response = board.fen(),status=200)

def mueve_ia(color):
    aux  = chess.Board(board.fen())
    ia = Ia(aux) 
    player = chess.WHITE if color else chess.BLACK
    val,ia_move = ia.best_move_negascout(4,player,alpha=ia.MIN_VAL,beta=ia.MAX_VAL)
    # val,ia_move = ia.best_move(4,player,a=ia.MIN_VAL, b=ia.MAX_VAL)
    # ia_move = ia.best_move_mlp(2,player)[1]
    print('ia: ', ia_move)
    print(val)
    
    return ia_move

@app.route('/newgame')
def new_game():
    board.reset()
    return app.response_class(response = chess.STARTING_BOARD_FEN)

if __name__ == '__main__':
    app.run(debug=True)