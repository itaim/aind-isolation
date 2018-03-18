"""This file is provided as a starting template for writing your own unit
tests to run and debug your minimax and alphabeta agents locally.  The test
cases used by the project assistant are not public.
"""

import time
import unittest
from importlib import reload

import game_agent
import isolation


class IsolationTest(unittest.TestCase):
    """Unit tests for isolation agents"""

    def setUp(self):
        reload(game_agent)
        self.player1 = "Player1"
        self.player2 = "Player2"
        self.game = isolation.Board(self.player1, self.player2)

    def test_example(self):
        # TODO: All methods must start with "test_"
        self.fail("Hello, World!")

if __name__ == '__main__':
    unittest.main()



class HeuristicsTest(unittest.TestCase):
    def test_potential_score_func(self):
        for gen in range(11):
            for moves in range(9):
                s = game_agent.potential_score_func(moves,gen)
                print('Generation: {}, Moves: {}, Score: {}'.format(gen,moves,s))

    def test_open_path_score(self):
        d = 7
        self.player1 = game_agent.AlphaBetaPlayer(search_depth=2,score_fn=game_agent.custom_score_3)
        self.player2 = game_agent.MinimaxPlayer(search_depth=2)

        self.game = isolation.Board(self.player1, self.player2, width=d, height=d)

        self.game._board_state = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 1,
                                  0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1,
                                  1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 51, 42]
        self.game.move_count = len([x for x in self.game._board_state[0:-4] if x == 1])
        print(self.game.to_string())

        res = game_agent.open_path_score(self.game,self.player1,100)
        print('open_path_score = {}'.format(res))
        # res = self.game.play(10000)
        # print(res)


    def test_get_long_path_potential_score(self):
        d = 9
        self.player1 = game_agent.MinimaxPlayer(search_depth=2)
        self.player2 = game_agent.MinimaxPlayer(search_depth=2)

        self.game = isolation.Board(self.player1, self.player2, width=d, height=d)

        self.game._board_state = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 1,
                                  0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1,
                                  1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 51, 42]
        self.game.move_count = len([x for x in self.game._board_state[0:-4] if x == 1])
        print(self.game.to_string())

        start = time.time()
        score = game_agent.custom_score_2(self.game, self.player1)
        elapsed = time.time() - start
        print('generations_weighted_difference {}'.format(score))
        print('elapsed {}'.format(elapsed))

        start = time.time()
        score = game_agent.custom_score_3(self.game,self.player1)
        elapsed = time.time()-start
        print('get_long_path_potential_score {}'.format(score))
        print('elapsed {}'.format(elapsed))

        moves = game_agent.get_moves(self.game, [self.game.get_player_location(self.player1)])
        start = time.time()
        max,avg = game_agent.max_avg_path(self.game, moves)
        elapsed = time.time() - start
        print('max_avg_path {} {}'.format(max,avg))
        print('elapsed {}'.format(elapsed))

        start = time.time()
        max_pos = 100
        max = game_agent.dfs(self.game,self.game.get_player_location(self.player1),max_pos)
        elapsed = time.time() - start
        print('dfs {} max positions {}'.format(max, max_pos))
        print('elapsed {}'.format(elapsed))

    def test_move_weights(self):

        m = MoveWeights(49)
        print(sum(m.weights.values()))
        for k,v in m.weights.items():
            print('move {} weight {}'.format(k,v))
        # for i in range(30):
        #     v1 = math.log(i+1)
        #     v2 = math.log(math.sqrt(i+1))
        #     # print('{} log() {}'.format(i,v1))
        #     print('{} - log(sqrt()) {}'.format(i,v2))


    def test_center_score(self):
        t = 0
        c = 0
        for x in range(7):
            for y in range(7):
                w, h = 7 // 2, 7 // 2
                score = float((h - y) ** 2 + (w - x) ** 2)
                print('x {} y {} w {} h {} center distance score {}'.format(x,y,w,h,score))
                t += score
                c += 1
        print('average center score {}'.format(t/c))

class GetMovesTest(unittest.TestCase):

    def test_get_moves1(self):
        d = 9
        self.player1 = game_agent.MinimaxPlayer(search_depth=2)
        self.player2 = game_agent.MinimaxPlayer(search_depth=2)

        self.game = isolation.Board(self.player1, self.player2, width=d, height=d)

        self.game._board_state = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 1,
                                  0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1,
                                  1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 51, 42]
        self.game.move_count = len([x for x in self.game._board_state[0:-4] if x == 1])
        print(self.game.to_string())

        moves = game_agent.get_moves(self.game, [(6,5)])
        print(len(moves))
        print(moves)
        self.assertEqual(len(moves), 6)

        moves = game_agent.get_moves(self.game, moves)
        print(len(moves))
        print(moves)
        self.assertEqual(len(moves), 13)

class MinimaxPlayerTest(unittest.TestCase):

    def test_minimax(self):
        self.player1 = game_agent.MinimaxPlayer(search_depth=1)
        self.player2 = game_agent.MinimaxPlayer(search_depth=1)
        self.game = isolation.Board(self.player1, self.player2)
        res = self.game.play(5000)
        print(res)

    def test_minimax_functionality3(self):
        d = 9
        self.player1 = game_agent.MinimaxPlayer(search_depth=1)
        self.player2 = game_agent.MinimaxPlayer(search_depth=1)

        self.game = isolation.Board(self.player1, self.player2, width=d, height=d)

        self.game._board_state = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 32, 22]
        self.game.move_count = len([x for x in self.game._board_state[0:-4] if x == 1])
        res = self.game.play(10000)
        print(res)
        v = self.player1.visited_nodes
        print('Player 1 visited {}'.format(len(v)))
        print(set(v))

    def test_minimax_open_move_score_depth2(self):
        d = 9
        self.player1 = game_agent.MinimaxPlayer(search_depth=2)
        self.player2 = game_agent.MinimaxPlayer(search_depth=2)

        self.game = isolation.Board(self.player1, self.player2, width=d, height=d)

        self.game._board_state = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 51, 42]
        self.game.move_count = len([x for x in self.game._board_state[0:-4] if x == 1])
        print(self.game.to_string())
        res = self.game.play(10000)
        print(res)

        expected = {((7, 6), (8, 4)), ((7, 6), (4, 4)), ((8, 5), (5, 7)), ((8, 3), (8, 4)), ((7, 2), (5, 7)),
                    ((8, 3), (7, 7)), ((8, 5), (7, 3)), ((4, 3), (4, 4)), ((4, 3), (8, 4)), ((7, 2), (7, 7)),
                    ((4, 3), (8, 6)), ((8, 3), (5, 7)), ((7, 2), (8, 4)), ((8, 5), (7, 7)), ((7, 2), (8, 6)),
                    ((7, 2), (7, 3)), ((7, 6), (5, 7)), ((8, 5), (4, 4)), ((7, 2), (4, 4)), ((4, 3), (5, 7)),
                    ((4, 3), (7, 3)), ((8, 5), (8, 6)), ((8, 5), (8, 4)), ((4, 3), (7, 7)), ((7, 6), (7, 7)),
                    ((8, 3), (4, 4)), ((7, 6), (8, 6)), ((8, 3), (7, 3)), ((7, 6), (7, 3)), ((8, 3), (8, 6))}

        print('Expected leaf nodes: {}'.format(len(expected)))
        print(expected)

        actual = set(self.player1.visited_nodes)
        print('Leaf nodes your agent evaluated: {}'.format(len(actual)))
        print(actual)

        print('Skipped nodes:')
        print(expected.difference(actual))
        extra = actual.difference(expected)
        print('Extra nodes: {}'.format(len(extra)))
        print(extra)

        #         print('Extra {}'.format(actual.difference(expected_eval)))
        #         print('Missing {}'.format(expected_eval.difference(actual)))


#     def test_minimax_functionality1(self):
#         d = 9
#         self.player1 = game_agent.MinimaxPlayer(search_depth=1)
#         self.player2 = game_agent.MinimaxPlayer(search_depth=1)
#
#         self.game = isolation.Board(self.player1, self.player2, width=d, height=d)
#
#         self.game._board_state = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0,
#          0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0,
#          0, 0, 0, 0, 0, 0, 0, 0, 51, 57]
#         self.game.move_count = len([x for x in self.game._board_state[0:-4] if x == 1])
#         # print('move count {}'.format(self.game.move_count))
#         res = self.game.play(10000)
#         print(res)
#
#         actual = set({x for v in game_agent.player_1_evaluated.values() for x in v})
#         print('evaluated {}'.format(len(actual)))
#         print(actual)
#
#         expected_eval = set({((1, 7), (8, 4)), ((2, 8), (7, 3)), ((2, 4), (5, 7)), ((2, 8), (5, 7)), ((5, 7),
#          (7,3)), ((5, 7), (7, 7)),((1, 7), (5, 7)), ((5, 7), (8, 4)), ((1, 5), (5, 7)), ((1, 7), (7, 3)), ((2, 8),
#          (8, 4)), ((4, 8), (5, 7)),
#          ((5, 7), (8, 6)), ((2, 8), (8, 6)), ((4, 4), (5, 7)), ((5, 7), (4, 4)), ((4, 8), (7, 3)), ((1, 5), (8, 4)),
#          ((2, 4), (4, 4)), ((2, 4), (7, 3)), ((2, 8), (4, 4)), ((4, 4), (7, 3)), ((1, 5), (8, 6)), ((2, 4), (8, 6)),
#          ((1, 7), (7, 7)), ((4, 4), (7, 7)), ((2, 8), (7, 7)), ((1, 7), (4, 4)), ((4, 4), (8, 4)), ((1, 5), (4, 4)),
#          ((2, 4), (8, 4)), ((1, 5), (7, 3)), ((4, 8), (4, 4)), ((4, 8), (7, 7)), ((4, 8), (8, 6)), ((2, 4), (7, 7)),
#          ((4, 8), (8, 4)), ((1, 5), (7, 7)), ((4, 4), (8, 6)), ((1, 7), (8, 6))})
#
#         print('expected evaluated {}'.format(len(expected_eval)))
#         print(expected_eval)
#         print('Extra {}'.format(actual.difference(expected_eval)))
#         print('Missing {}'.format(expected_eval.difference(actual)))
#
#
#
#
#     def test_minimax_functionality2(self):
#         d = 9
#         self.player1 = game_agent.MinimaxPlayer(search_depth=1)
#         self.player2 = game_agent.MinimaxPlayer(search_depth=1)
#
#         self.game = isolation.Board(self.player1, self.player2,width=d,height=d)
#         #    0 1 2 3 4 5 6 7 8
#         # 0 | | | | | | | | | |
#         # 1 | | | | | | | | | |
#         # 2 | | | | | |-| | | |
#         # 3 | | | |1|-|-|2| | |
#         # 4 | |-|-|-|-|-| | | |
#         # 5 | | | |-| |-|-| | |
#         # 6 | | |-|-| | |-| | |
#         # 7 | | | | | | | | | |
#         # 8 | | | | | | | | | |
#
#         self.game._board_state[2 + 5 * d] = 1
#         self.game._board_state[3 + 3 * d] = 1
#         self.game._board_state[3 + 4 * d] = 1
#         self.game._board_state[3 + 5 * d] = 1
#         self.game._board_state[3 + 6 * d] = 1
#         self.game._board_state[4 + 1 * d] = 1
#         self.game._board_state[4 + 2 * d] = 1
#         self.game._board_state[4 + 3 * d] = 1
#         self.game._board_state[4 + 4 * d] = 1
#         self.game._board_state[4 + 5 * d] = 1
#         self.game._board_state[5 + 3 * d] = 1
#         self.game._board_state[5 + 5 * d] = 1
#         self.game._board_state[5 + 6 * d] = 1
#         self.game._board_state[6 + 2 * d] = 1
#         self.game._board_state[6 + 3 * d] = 1
#         self.game._board_state[6 + 6 * d] = 1
#          h + w * d
#         self.game._board_state[-3] = 0
#         self.game._board_state[-2] = 3 + 6 * d
#         self.game._board_state[-1] = 3 + 3 * d
#
#         print(self.game.to_string())
#         print('evaluated')
#         print(set(game_agent.player_1_evaluated))
#
#         res = self.game.play(5000)
#         print(res)
#         print('evaluated {}'.format(len(set(game_agent.player_1_evaluated))))
#         s1 = sorted(set(game_agent.player_1_evaluated))
#         print(s1)
#
#         expected_eval = sorted(set([((1, 2), (3, 6)), ((2, 1), (3, 6)), ((5, 4), (3, 6)), ((5, 2), (3, 6)), ((1, 4), (3, 6))]))
#         print('expected evaluated {}'.format(len(expected_eval)))
#         print(expected_eval)
#
#
# class AlphaBetaPlayerTest(unittest.TestCase):
#
#     def test_alphabeta(self):
#         self.player1 = game_agent.AlphaBetaPlayer(search_depth=1)
#         self.player2 = game_agent.AlphaBetaPlayer(search_depth=1)
#         self.game = isolation.Board(self.player1, self.player2)
#         res = self.game.play(5000)
#         print(res)
#
#     def test_alphabets_functionality(self):
#         d = 9
#         self.player1 = game_agent.AlphaBetaPlayer(search_depth=1)
#         self.player2 = game_agent.AlphaBetaPlayer(search_depth=1)
#
#         self.game = isolation.Board(self.player1, self.player2,width=d,height=d)
#         #    0 1 2 3 4 5 6 7 8
#         # 0 | | | | | | | | | |
#         # 1 | | | |2|-| | | | |
#         # 2 | | |-| | | |-| | |
#         # 3 | | |-| |-|-|-| | |
#         # 4 | | | |-|-|-|-| | |
#         # 5 | | |1|-|-|-|-| | |
#         # 6 | | | | | | |-| | |
#         # 7 | | | | | | | | | |
#         # 8 | | | | | | | | | |
#
#         self.game._board_state[1 + 3 * d] = 1
#         self.game._board_state[1 + 4 * d] = 1
#         self.game._board_state[2 + 2 * d] = 1
#         self.game._board_state[2 + 6 * d] = 1
#         self.game._board_state[3 + 2 * d] = 1
#         self.game._board_state[3 + 4 * d] = 1
#         self.game._board_state[3 + 5 * d] = 1
#         self.game._board_state[3 + 6 * d] = 1
#         self.game._board_state[4 + 3 * d] = 1
#         self.game._board_state[4 + 4 * d] = 1
#         self.game._board_state[4 + 5 * d] = 1
#         self.game._board_state[4 + 6 * d] = 1
#         self.game._board_state[5 + 2 * d] = 1
#         self.game._board_state[5 + 3 * d] = 1
#         self.game._board_state[5 + 4 * d] = 1
#         self.game._board_state[5 + 5 * d] = 1
#         self.game._board_state[5 + 6 * d] = 1
#         self.game._board_state[6 + 6 * d] = 1
#
#         self.game._board_state[-3] = 0
#         self.game._board_state[-2] = 1 + 3 * d
#         self.game._board_state[-1] = 5 + 2 * d
#
#         print(self.game.to_string())
#         print('evaluated')
#         print(set(game_agent.player_1_evaluated))
#
#         res = self.game.play(5000)
#         print(res)
#         print('evaluated {}'.format(len(set(game_agent.player_1_evaluated))))
#         print(set(game_agent.player_1_evaluated))
#
#         expected_eval = sorted(set([((7, 1), (1, 3)), ((6, 4), (1, 3)), ((7, 3), (1, 3)), ((6, 0), (1, 3)), ((3, 1), (1, 3)), ((4, 0), (1, 3)), ((3, 3), (1, 3))]))
#
#         print('expected evaluated {}'.format(len(expected_eval)))
#         print(expected_eval)
#
#
#
#