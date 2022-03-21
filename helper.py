from tensorflow.keras.models import load_model 
import tfdeploy as td
import pickle
import numpy as np

def load():
    model = load_model('modelo_overfitted2.h5')
    return model

def load_from_pikle():
    # model = pickle.load(open('model.pkl', 'rb'))
    model = td.Model('model.pkl')
    return model

def get_bitboard(board):
    '''
    params
    ------
    board : chess.pgn board object
        board to get state from
    returns
    -------
    bitboard representation of the state of the game
    64 * 6 + 5 dim binary numpy vector
    64 squares, 6 pieces, '1' indicates the piece is at a square
    5 extra dimensions for castling rights queenside/kingside and whose turn
    '''

    bitboard = np.zeros(64*6*2+5)

    piece_idx = {'p': 0, 'n': 1, 'b': 2, 'r': 3, 'q': 4, 'k': 5}

    for i in range(64):
        if board.piece_at(i):
            color = int(board.piece_at(i).color) + 1
            bitboard[(piece_idx[board.piece_at(i).symbol().lower()] + i * 6) * color] = 1

    bitboard[-1] = int(board.turn)
    bitboard[-2] = int(board.has_kingside_castling_rights(True))
    bitboard[-3] = int(board.has_kingside_castling_rights(False))
    bitboard[-4] = int(board.has_queenside_castling_rights(True))
    bitboard[-5] = int(board.has_queenside_castling_rights(False))

    return np.reshape(bitboard, (1, bitboard.shape[0]))
    # return str(bitboard)[1:-1].replace('\n', '').replace(' ', ',')