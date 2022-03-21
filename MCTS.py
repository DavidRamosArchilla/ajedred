import chess
import numpy as np


class MCTS:
    C = 1 # hiperparameter to manage expliotation vs exploration
    def __init__(self):
        self.explored = set() # fen: value // eliminar??
        self.nodes_parameters = {} # fen: (N, V) N--> times visited, V-->value
        self.UCT = {} # fen: UPC (upper confidence tree)

    def get_value(self, result: str, player):
        if result == '1-0':
            return 1 if player == chess.WHITE else -1

        elif result == '0-1':
            return -1 if player == chess.WHITE else 1 
        else:
            return 0



    """
    s --> state
    v --> value of s
    """
    # TODO: tener en cuenta el numero de movimientos sin avances para que si este es elevado se considere un empate
    def search(self, s: chess.Board):
        if s.is_game_over():
            s_fen = s.fen()
            v = self.get_value(s.result(), s.turn) 
            if s_fen not in self.nodes_parameters:
                # self.visited.add(s_fen)
                self.nodes_parameters[s_fen] = np.array((1, v))
            else:
                self.nodes_parameters[s_fen][0] += 1
            return -v, 1

        s_fen = s.fen()
        # if s_fen not in self.visited:
        #   self.visited.append(s_fen)
        #   v = self.simulate(s)
        #   self.node_parameters[s_fen] = (1,v)
        #   return -v
        
        childs = s.legal_moves

        if s_fen in self.explored:
        # choose which node is going to be expanded
            best_uct = float('-inf')
            best_child = None
            # best_w = 0
            n_p = self.nodes_parameters[s_fen][0] # parent's n
            for a in childs:
                s.push(a)
                w, n = self.nodes_parameters[s.fen()]
                child_uct = self.get_UCT(n, w, n_p)
                if child_uct > best_uct:
                    best_uct = child_uct
                    best_child = a
                    # best_w = w
                s.pop()
            s.push(best_child)
            sum_v, sum_n = self.search(s) # cambiar signo??
            # propagate the results
            self.nodes_parameters[s_fen][0] += sum_n
            self.nodes_parameters[s_fen][1] += sum_v

        
        else:
            self.explored.add(s_fen)
            sum_v = 0
            sum_n = 0
            for a in childs:
                s.push(a)
                a_fen = s.fen()
                if a_fen not in self.nodes_parameters:
                    v = self.simulate(a_fen, s.turn) 
                    self.nodes_parameters[a_fen] = np.array((1, v))
                    sum_v += v
                    sum_n += 1
                s.pop()
            self.nodes_parameters[s_fen][0] += sum_n
            self.nodes_parameters[s_fen][1] += sum_v

        # v = -self.search(new_s)

        return -sum_v, sum_n

        # hay que crear una copia del objeto antes de llamar esta funcion. Tambien considerar pasar simplemente el fen y hacer la copia dentro de la funcion
    
    def search_iter(self, s):
        path = self.select(s)
        print(path)
        leaf = path[-1]
        self.explored.add(leaf)
        # print(self.explored)
        sum_v = 0
        sum_n = 0
        board = chess.Board(leaf)
        for a in board.legal_moves:
            board.push(a)
            a_fen = board.fen()
            if a_fen not in self.nodes_parameters:
                v = self.simulate(a_fen, board.turn) 
                self.nodes_parameters[a_fen] = np.array((1, v))
                sum_v += v
                sum_n += 1
            board.pop()
        
        for i in path:
            self.nodes_parameters[i][0] += sum_n
            self.nodes_parameters[i][1] += sum_v
    
    def _select(self, current_s, parent_s, best_path: dict, current_path: list, best_uct: list):
        if current_s not in self.explored: # TODO: check if is game over
            if parent_s is not None:
                n_p = self.nodes_parameters[parent_s][0]
                n, w = self.nodes_parameters[current_s]
                uct = self.get_UCT(n, w, n_p)
                if uct > best_uct[0]:
                    best_uct[0] = uct
                    best_path[0] = current_path[:] # current_path[:] es mas rapido

        else:
            board = chess.Board(current_s)
            for child in board.legal_moves:
                board.push(child)
                child_fen = board.fen()
                current_path.append(child_fen)
                self._select(child_fen, current_s, best_path, current_path, best_uct)
                current_path.pop()
                board.pop()

    def select(self, s):
        best_path = {0: [s]} # it acts as a wrapper in order to pass the varable by reference
        current_path = [s]
        best_uct = [float('-inf')] # pass this parameter by reference
        self._select(s, None, best_path, current_path, best_uct)
        print(best_uct)
        return best_path[0]

    def simulate(self, s_fen, turn):
        
        s = chess.Board(s_fen)
        while not s.is_game_over():
            move = np.random.choice(list(s.legal_moves))
            s.push(move)
        return self.get_value(s.result(), turn)

    def get_UCT(self, n, w, n_p, c=C):
        # if n_p == 0 or n == 0: return 0
        return w/n + c * np.sqrt(n_p) / (1 + n)
        # return w/n + c * np.sqrt(np.log(n_p) / n)

    def iterate(self, n_iters, s: chess.Board):
        s_fen = s.fen()
        self.nodes_parameters[s_fen] = np.array((1, 0))
        for i in range(n_iters):
            # v, n = self.search(s)
            # self.nodes_parameters[s_fen][0] += n
            # self.nodes_parameters[s_fen][1] += v
            self.search_iter(s_fen)
            if True or i % 5 == 0:
                print(f'Iteration {i+1} [{"=" * (i//5)}>{" " * ((n_iters-i-1)//5)}]')

mcts = MCTS()
fen_prueba = '5rk1/pb4pq/4p1Q1/1pn1P3/3p2P1/P2P4/1P1K4/5R2 w - - 3 14'# 'rn1B1br1/pp3ppp/2p3k1/5p2/2BP4/5N2/PPP2P1P/R2QK2R w KQ - 1 14' # 'rnb1kbnr/pppp1ppp/4p3/6q1/8/2NP4/PPP1PPPP/R1BQKBNR w - - 0 1' # rn1B1b1r/pp3ppp/2p3k1/5p2/2BP4/5N2/PPP2P1P/R2QK2R b KQ - 0 13
mcts.iterate(50, chess.Board(fen_prueba))
c = chess.Board(fen_prueba)
i = 0
# mcts.simulate(fen_prueba, chess.WHITE)
print(mcts.nodes_parameters[c.fen()])
for a in c.legal_moves:
    c.push(a)
    print(f'N: {mcts.nodes_parameters[c.fen()][0]} , V: {mcts.nodes_parameters[c.fen()][1]}')
    print(c.fen())
    c.pop()
    i+=1
print(len(mcts.nodes_parameters), len(mcts.explored))