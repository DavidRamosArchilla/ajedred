import chess

class Ia:
    MAX_VAL = 1000000
    MIN_VAL = -1000000
    def __init__(self, board):
        self.board = board
        self.value_pieces = {
            chess.PAWN: 1,
            chess.KNIGHT: 3,
            chess.BISHOP: 3,
            chess.ROOK: 5,
            chess.QUEEN: 9,
            chess.KING: 0
        }

    def evaluate_pos(self):
        value = 0
        for k,piece in self.board.piece_map().items():
            if piece.color == chess.WHITE: #si chess.WHITE: chess.Color= True; chess.BLACK: chess.Color= False
                value -= self.value_pieces[piece.piece_type]
            else:
                value += self.value_pieces[piece.piece_type]
        return value

    def best_move(self,profundidad,player,a,b):# TODO implementar poda alfa beta
        # la ia es negras, se escoge el mejor movimiento para negras
        if self.board.is_game_over():
            result = self.board.result()
            if result == '1-0':
                return self.MIN_VAL,None
            elif result == '0-1':
                return self.MAX_VAL,None
            elif result == '1/2-1/2':
                return 0,None
        elif profundidad ==0 :
            return self.evaluate_pos(),None
        else:
            moves = list(self.board.legal_moves)
            if player == chess.BLACK:
                best_move_white = None
                best_board = self.MIN_VAL
                board_eval = self.MIN_VAL
                for move in moves:
                    self.board.push(move)
                    board_eval = max(board_eval,self.best_move(profundidad-1,chess.WHITE,a,b)[0])
                    self.board.pop()
                    a = max(a,board_eval)
                    if board_eval >best_board :
                        best_board = board_eval
                        best_move_white = move
                    if a>=b:
                        break
                return best_board,best_move_white
            else:
                best_move_black = None
                # best_board = self.MAX_VAL
                board_eval2 = self.MAX_VAL
                for move in moves:
                    self.board.push(move)
                    board_eval2 = min(board_eval2,self.best_move(profundidad-1,chess.BLACK,a,b)[0])
                    self.board.pop()
                    b = min(b,board_eval2)
                    if a>=b:
                        break
                return board_eval2,best_move_black
# board = chess.Board()
# board.set_fen('1rbqkr2/ppppppbp/8/3B4/4P3/8/PPPP1P1P/RNBQK1NR')
# ia= Ia(board)
# print(ia.evaluate_pos())