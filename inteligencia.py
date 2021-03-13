import chess
import numpy as np

class Ia:
    MAX_VAL = 1000000
    MIN_VAL = -1000000
    def __init__(self, board):
        self.board = board
        self.value_pieces = {
            chess.PAWN: 100,
            chess.KNIGHT: 320,
            chess.BISHOP: 330,
            chess.ROOK: 500,
            chess.QUEEN: 900,
            chess.KING: 20000
        }
        self.movility_bonus = {#para negras hay que hacer movility_bonus[piece][63-casilla]
            chess.PAWN: np.array( (0,  0,  0,  0,  0,  0,  0,  0,
                          5, 10, 10,-20,-20, 10, 10,  5,
                          5, -5,-10,  0,  0,-10, -5,  5,
                          0,  0,  0, 20, 20,  0,  0,  0,
                          5,  5, 10, 25, 25, 10,  5,  5,
                          10, 10, 20, 30, 30, 20, 10, 10,
                          50, 50, 50, 50, 50, 50, 50, 50,
                          0,  0,  0,  0,  0,  0,  0,  0)
            ),
            chess.KNIGHT: np.array((-50,-40,-30,-30,-30,-30,-40,-50,
                            -40,-20,  0,  5,  5,  0,-20,-40,
                            -30,  5, 10, 15, 15, 10,  5,-30,
                            -30,  0, 15, 20, 20, 15,  0,-30,
                            -30,  5, 15, 20, 20, 15,  5,-30,
                            -30,  0, 10, 15, 15, 10,  0,-30,
                            -40,-20,  0,  0,  0,  0,-20,-40,
                            -50,-40,-30,-30,-30,-30,-40,-50)
            ),
            chess.BISHOP: np.array((-20,-10,-10,-10,-10,-10,-10,-20,
                            -10,  5,  0,  0,  0,  0,  5,-10,
                            -10, 10, 10, 10, 10, 10, 10,-10,
                            -10,  0, 10, 10, 10, 10,  0,-10,
                            -10,  5,  5, 10, 10,  5,  5,-10,
                            -10,  0,  5, 10, 10,  5,  0,-10,
                            -10,  0,  0,  0,  0,  0,  0,-10,
                            -20,-10,-10,-10,-10,-10,-10,-20)
            ),
            chess.ROOK: np.array((0,  0,  0,  5,  5,  0,  0,  0,
                        -5,  0,  0,  0,  0,  0,  0, -5,
                        -5,  0,  0,  0,  0,  0,  0, -5,
                        -5,  0,  0,  0,  0,  0,  0, -5,
                        -5,  0,  0,  0,  0,  0,  0, -5,
                        -5,  0,  0,  0,  0,  0,  0, -5,
                        5, 10, 10, 10, 10, 10, 10,  5,
                        0,  0,  0,  0,  0,  0,  0,  0)
            ),
            chess.QUEEN: np.array((-20,-10,-10, -5, -5,-10,-10,-20,
                        -10,  0,  5,  0,  0,  0,  0,-10,
                        -10,  5,  5,  5,  5,  5,  0,-10,
                          0,  0,  5,  5,  5,  5,  0, -5,
                          -5,  0,  5,  5,  5,  5,  0, -5,
                          -10,  0,  5,  5,  5,  5,  0,-10,
                          -10,  0,  0,  0,  0,  0,  0,-10,
                          -20,-10,-10, -5, -5,-10,-10,-20
            )),
            chess.KING: np.array((20, 30, 10,  0,  0, 10, 30, 20,
                        20, 20,  0,  0,  0,  0, 20, 20,
                        -10,-20,-20,-20,-20,-20,-20,-10,
                        -20,-30,-30,-40,-40,-30,-30,-20,
                        -30,-40,-40,-50,-50,-40,-40,-30,
                        -30,-40,-40,-50,-50,-40,-40,-30,
                        -30,-40,-40,-50,-50,-40,-40,-30,
                        -30,-40,-40,-50,-50,-40,-40,-30)
            )
            
        }
        self.transp_table = {}
        

    def evaluate_pos(self):
        value = 0
        for square,piece in self.board.piece_map().items():
            if piece.color == chess.WHITE: #si chess.WHITE: chess.Color= True; chess.BLACK: chess.Color= False
                value -= self.value_pieces[piece.piece_type] - self.movility_bonus[piece.piece_type][square]
            else:
                value += self.value_pieces[piece.piece_type] + self.movility_bonus[piece.piece_type][63-square]
        return value

    def best_move(self,profundidad,player,a,b):
        
        # la ia es negras, se escoge el mejor movimiento para negras
        if profundidad ==0 :
            evaluation = self.evaluate_pos()
            self.transp_table[self.board.fen()] = evaluation
            return evaluation,None

        elif self.board.is_game_over():
            result = self.board.result()
            if result == '1-0':
                self.transp_table[self.board.fen()] = self.MIN_VAL
                return self.MIN_VAL,None
            elif result == '0-1':
                self.transp_table[self.board.fen()] = self.MAX_VAL
                return self.MAX_VAL,None
            elif result == '1/2-1/2':
                self.transp_table[self.board.fen()] = 0
                return 0,None
        else:       
            if player == chess.BLACK:
                best_move_white = None
                best_board = self.MIN_VAL-1
                board_eval = self.MIN_VAL
                for move in self.board.legal_moves:
                    self.board.push(move)
                    #check if the state is on the table
                    if self.board.fen() in self.transp_table:
                        board_eval = self.transp_table[self.board.fen()]
                    else:
                        board_eval = max(board_eval,self.best_move(profundidad-1,chess.WHITE,a,b)[0])
                        #self.transp_table[self.board.fen()] = board_eval
                    self.board.pop()
                    a = max(a,board_eval)
                    if board_eval > best_board :
                        best_board = board_eval
                        best_move_white = move
                    if a>=b:
                        break
                return best_board,best_move_white
            else:
                best_move_black = None
                # best_board = self.MAX_VAL
                board_eval2 = self.MAX_VAL
                for move in self.board.legal_moves:
                    self.board.push(move)
                    if self.board.fen() in self.transp_table:
                        board_eval2 = self.transp_table[self.board.fen()]
                    else:
                        board_eval2 = min(board_eval2,self.best_move(profundidad-1,chess.BLACK,a,b)[0])
                        #self.transp_table[self.board.fen()] = board_eval2
                    self.board.pop()
                    b = min(b,board_eval2)
                    if a>=b:
                        break
                return board_eval2,best_move_black
    
    def best_move_negascout(self,profundidad,player,alpha,beta):
        if profundidad ==0 :
            evaluation = self.evaluate_pos()
            # self.transp_table[self.board.fen()] = evaluation
            return evaluation,None
        # elif self.board.is_game_over():
        #     result = self.board.result()
        #     if result == '1-0':
        #         self.transp_table[self.board.fen()] = self.MIN_VAL
        #         return self.MIN_VAL,None
        #     elif result == '0-1':
        #         self.transp_table[self.board.fen()] = self.MAX_VAL
        #         return self.MAX_VAL,None
        #     elif result == '1/2-1/2':
        #         self.transp_table[self.board.fen()] = 0
        #         return 0,None
        else:
            b = beta
            best_move = None
            for move in self.board.legal_moves:
                try:
                    self.board.push(move)
                except:
                    continue
                a = - self.best_move_negascout(profundidad-1,not player,-b,-alpha)[0]
                
                if a>alpha: 
                    alpha = a
                    best_move = move
                if alpha>= beta :
                    self.board.pop()
                    return a,best_move
                if alpha>=b:
                    alpha = - self.best_move_negascout(profundidad-1,not player,-beta,-alpha)[0]
                    self.board.pop()
                    if alpha>=beta:
                        return alpha, move
                else:
                    self.board.pop()
                b = alpha + 1
            return alpha,best_move
                

# board = chess.Board()
# board.set_fen('1rbqkr2/ppppppbp/8/3B4/4P3/8/PPPP1P1P/RNBQK1NR')
# ia= Ia(board)
# print(ia.evaluate_pos())