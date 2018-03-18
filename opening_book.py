import random


class OpeningBook(object):

    def __init__(self,width,height):
        self.height = height
        self.width = width
        self.dict = {
            self.get_board_key(),[(width//2,height//2)]
        }
        # non_center_first_moves = [(row, col) for row in range(width) for col in range(height) if row != width//2 or col != height // 2]
        # for m in non_center_first_moves:
        #     key = self.get_board_key(moves = [m])
        #     self.dict[key] = [(width//2,height // 2)]
        # for row in range(width):
        #     for col in range(height):
        #         if row == width//2 and col == height // 2:
        #             continue
        #         self.get_board_key(])
        #         self.dict[]

    def get_opening_book_moves(self):
        if not self._board_state[-1]:
            # Player 1 to occupy center on 1st move
            return [(self.width//2,self.height//2)]
        elif not self._board_state[-2] and not self._board_state[self.width//2+self.height//2*self.height]:
            # Player 2 to occupy center if free
            return [(self.width // 2, self.height // 2)]
        else:
            return None

    def get_board(self, moves=[]):
        board_state = [0] * (self.width * self.height + 3)
        board_state[-1] = None
        board_state[-2] = None
        count = 0
        for row,col in moves:
            idx = row + col * self.height
            board_state[idx] = 1
            last_move_idx = count%2 + 1
            board_state[-last_move_idx] = idx
            board_state[-3] ^= 1
        return board_state

    def get_board_key(self,moves=[]):
        board_state = self.get_board(moves)
        return str(board_state).__hash__()