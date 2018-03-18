"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""


class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass


def custom_score(game, player):
    def weight_fn(i):
        return 1 / (i + 1)

    return moves_forward_difference(game, player, 3, weight_fn)


def custom_score_2(game, player):
    return open_path_score(game, player, max_path=6, dfs=True)


def custom_score_3(game, player):
    return open_path_score(game, player, max_path=6,dfs=False)


def get_moves(game, loc):
    directions = [(-2, -1), (-2, 1), (-1, -2), (-1, 2),
                  (1, -2), (1, 2), (2, -1), (2, 1)]
    return [(r + dr, c + dc) for r, c in loc for dr, dc in directions
            if game.move_is_legal((r + dr, c + dc))]


def moves_forward_difference(game, player, moves, weight_fn):
    own = [set([game.get_player_location(player)])]
    opp = [set([game.get_player_location(game.get_opponent(player))])]
    score = 0.0

    for i in range(moves):
        own.append(set(get_moves(game, own[-1])))
        opp.append(set(get_moves(game, opp[-1])))
        p = len(own[-1])
        o = len(opp[-1])
        if own[-1].intersection(opp[-1]):
            # accounting for the possibility of being blocked by opponent
            p -= 1
        if i > 0:
            if opp[-2].intersection(opp[-1]):
                # accounting for the possibility of blocking opponent
                o -= 1
            # taking into account that one of the moves is the origin square not marked as illegal
            p = max(0, p - 1)
            o = max(0, o - 1)
        score += weight_fn(i) * (p - o)
    return score

def get_adjacent(r, c, game):
    directions = [(-2, -1), (-2, 1), (-1, -2), (-1, 2),
                  (1, -2), (1, 2), (2, -1), (2, 1)]
    return [get_idx((r + dr, c + dc), game.height) for dr, dc in directions
            if game.move_is_legal((r + dr, c + dc))]


def get_idx(move, height):
    return move[0] + move[1] * height


def create_game_graph(game):
    graph = {}
    for y in range(game.height):
        for x in range(game.width):
            graph[get_idx((y, x), game.height)] = set(get_adjacent(y, x, game))
    return graph


def open_path_score(game, player, max_path, dfs):
    graph = create_game_graph(game)
    frontier = [get_idx(game.get_player_location(player), game.height)]
    explored = set()

    def get_neighbors(vertex, turn):
        neighbors = []
        for i in graph[vertex]:
            l = len(graph[i])
            if l > 1:
                neighbors.append((i, l))
            elif l == 1:
                #if first turn don't add single move that can be blocked by opponent
                if turn == 1:
                    opponent_vertex = get_idx(game.get_player_location(game.get_opponent(player)), game.height)
                    if not i in graph[opponent_vertex]:
                        neighbors.append((i, 1))
                else:
                    neighbors.append((i, 1))
        # exploration order from the square with fewest onward moves, following Warnsdorf's rule for knight tour
        return [v[0] for v in sorted(neighbors, key=lambda c: c[1])]

    path_len = 0
    if dfs:
        pop_index = -1
    else:
        pop_index = 0
    while frontier and path_len < max_path:
        vertex = frontier.pop(pop_index)
        if vertex in explored:
            continue
        explored.add(vertex)
        path_len += 1
        graph[vertex] -= explored
        for neighbor in get_neighbors(vertex, path_len):
            frontier.append(neighbor)
    return float(path_len)


class IsolationPlayer:
    """Base class for minimax and alphabeta agents -- this class is never
    constructed or tested directly.

    ********************  DO NOT MODIFY THIS CLASS  ********************

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """

    def __init__(self, search_depth=3, score_fn=custom_score, timeout=10.):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout

    def get_candidate_moves(self, game):
        return game.get_legal_moves()


class MinimaxPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using depth-limited minimax
    search. You must finish and test this player to make sure it properly uses
    minimax to return a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        **************  YOU DO NOT NEED TO MODIFY THIS FUNCTION  *************

        For fixed-depth search, this function simply wraps the call to the
        minimax method, but this method provides a common interface for all
        Isolation agents, and you will replace it in the AlphaBetaPlayer with
        iterative deepening search.

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        moves = self.get_candidate_moves(game)
        best_move = (-1, -1)
        if not moves:
            # print('minimax player no moves, forfeiting...')
            return best_move  # forfeit
        else:
            best_move = moves[0]
        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            return self.minimax(game, self.search_depth)

        except SearchTimeout:
            return best_move  # Handle any actions required after timeout as needed
        except Exception as e:
            print(e)
        # Return the best move from the last completed search iteration
        return best_move

    def minimax(self, game, max_depth):
        """Implement depth-limited minimax search algorithm as described in
        the lectures.

        This should be a modified version of MINIMAX-DECISION in the AIMA text.
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Minimax-Decision.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        max_depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        moves = self.get_candidate_moves(game)
        return self.minimax_decision(game, max_depth, moves)

    def minimax_decision(self, game, depth, legal_moves):
        best_score = float("-inf")
        best_move = legal_moves[0]
        for m in legal_moves:
            v = self.min_value(game.forecast_move(m), depth - 1)
            if v > best_score:
                best_score = v
                best_move = m
            if self.time_left() < self.TIMER_THRESHOLD:
                raise SearchTimeout()
        return best_move

    def min_value(self, game, max_depth):
        if game.is_winner(game.inactive_player):
            return float("inf")
        elif self.time_left() < self.TIMER_THRESHOLD:  # time limit cutoff return v
            raise SearchTimeout()
        elif max_depth <= 0:
            return self.score(game, game.inactive_player)
        else:
            moves = self.get_candidate_moves(game)
            best_score = float("inf")
            for m in moves:
                s = self.max_value(game.forecast_move(m), max_depth - 1)
                if s < best_score:
                    best_score = s
                if self.time_left() < self.TIMER_THRESHOLD:
                    raise SearchTimeout()
            return best_score

    def max_value(self, game, max_depth):
        if game.is_loser(game.active_player):
            return float("-inf")
        elif self.time_left() < self.TIMER_THRESHOLD:  # time limit cutoff return v
            raise SearchTimeout()
        elif max_depth <= 0:
            return self.score(game, game.active_player)
        else:
            moves = self.get_candidate_moves(game)
            best_score = float("-inf")
            for m in moves:
                s = self.min_value(game.forecast_move(m), max_depth - 1)
                if s > best_score:
                    best_score = s
                if self.time_left() < self.TIMER_THRESHOLD:
                    raise SearchTimeout()
            return best_score


class AlphaBetaPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using iterative deepening minimax
    search with alpha-beta pruning. You must finish and test this player to
    make sure it returns a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        Modify the get_move() method from the MinimaxPlayer class to implement
        iterative deepening search instead of fixed-depth search.

        **********************************************************************
        NOTE: If time_left() < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        moves = self.get_candidate_moves(game)
        if not moves:
            # print('alphabeta player no moves, forfeiting...')
            return (-1, -1)  # forfeit
        else:
            default_move = moves[0]
            try:
                m = self.alphabeta_iterative_deepening(game)
                if m:
                    return m
                else:
                    return default_move
            except SearchTimeout:
                return default_move
            except Exception as e:
                print(e)
                # print(str(e))
                return default_move

    def alphabeta_iterative_deepening(self, game):
        best_move = None
        try:
            depth = 1
            while True:
                best_move = self.alphabeta(game, depth)
                depth += 1
                if self.time_left() < self.TIMER_THRESHOLD:
                    return best_move
        except SearchTimeout:
            pass
        # print('alphabeta_iterative_deepening move {} candidate first moves {}, max_depth {}, best move {}'.format(game.move_count, len(moves),max_depth,best_move))
        return best_move

    def alphabeta(self, game, max_depth, alpha=float("-inf"), beta=float("inf")):
        """Implement depth-limited minimax search with alpha-beta pruning as
        described in the lectures.

        This should be a modified version of ALPHA-BETA-SEARCH in the AIMA text
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Alpha-Beta-Search.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        actions = self.get_candidate_moves(game)
        best_score = float("-inf")
        best_move = None
        for m in actions:
            v = self.min_alphabeta_value(game.forecast_move(m), max_depth - 1, alpha, beta)
            if v > best_score:
                best_score = v
                best_move = m
            if best_score >= beta:
                return best_move
            alpha = max(alpha, best_score)
            if self.time_left() < self.TIMER_THRESHOLD:
                raise SearchTimeout()

        return best_move

    def max_alphabeta_value(self, game, max_depth, alpha, beta):
        """ Return the value for a loss (-inf) if the game is over,
        otherwise return the maximum value over all legal child
        nodes.
        """
        if game.is_loser(game.active_player):
            return float("-inf")
        elif self.time_left() < self.TIMER_THRESHOLD:  # time limit cutoff return v
            raise SearchTimeout()
        elif max_depth <= 0:
            return self.score(game, game.active_player)
        else:
            moves = self.get_candidate_moves(game)
            best_score = float("-inf")
            for m in moves:
                best_score = max(best_score,
                                 self.min_alphabeta_value(game.forecast_move(m), max_depth - 1, alpha, beta))
                if best_score >= beta:
                    return best_score
                alpha = max(alpha, best_score)
                if self.time_left() < self.TIMER_THRESHOLD:
                    raise SearchTimeout()
            return best_score

    def min_alphabeta_value(self, game, max_depth, alpha, beta):
        """ Return the value for a win (+inf) if the game is over,
        otherwise return the minimum value over all legal child
        nodes.
        """
        if game.is_winner(game.inactive_player):
            return float("inf")
        elif self.time_left() < self.TIMER_THRESHOLD:  # time limit cutoff return v
            raise SearchTimeout()
        elif max_depth <= 0:
            return self.score(game, game.inactive_player)
        else:
            moves = self.get_candidate_moves(game)
            best_score = float("inf")
            for m in moves:
                best_score = min(best_score,
                                 self.max_alphabeta_value(game.forecast_move(m), max_depth - 1, alpha, beta))
                if best_score <= alpha:
                    return best_score
                beta = min(beta, best_score)
                if self.time_left() < self.TIMER_THRESHOLD:
                    raise SearchTimeout()
            return best_score
