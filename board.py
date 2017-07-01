"""
====T Block====

     #
    ###

    0 1 0
    1 1 1

    1 0
    1 1
    1 0

    1 1 1
    0 1 0

    0 1
    1 1
    0 1

====I Block====

    ####

    1 1 1 1

    1
    1
    1
    1

====O Block====

    ##
    ##

    1 1
    1 1

====S Block=====

     ##
    ##

    0 1 1
    1 1 0

    1 0
    1 1
    0 1

====L Block=====

    #
    #
    ##

    1 0
    1 0
    1 1
"""

import math
import random
import os

BEST_SCORE_FILE_NAME = "best_score"

block_shapes = [
    # T Block
    [[0, 1, 0],
     [1, 1, 1]],
    # L Block
    [[1, 0],
     [1, 0],
     [1, 1]],
    # S Block
    [[0, 1, 1],
     [1, 1, 0]],
    # O Block
    [[1, 1],
     [1, 1]],
    # I Block
    [[1], [1], [1], [1]]
]


class Board:
    """Board representation"""

    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.board = self._get_new_board()

        self.current_block_pos = None
        self.current_block = None
        self.next_block = None

        self.game_over = False
        self.score = None
        self.lines = None
        self.best_score = None
        self.level = None

    def start(self):
        """Start game"""

        self.board = self._get_new_board()

        self.current_block_pos = None
        self.current_block = None
        self.next_block = None

        self.game_over = False
        self.score = 0
        self.lines = 0
        self.level = 1
        self.best_score = self._read_best_score()

        self._place_new_block()

    def is_game_over(self):
        """Is game over"""

        return self.game_over

    def move_block(self, direction):
        """Try to move block"""

        pos = self.current_block_pos
        if direction == "left":
            new_pos = [pos[0], pos[1] - 1]
        elif direction == "right":
            new_pos = [pos[0], pos[1] + 1]
        elif direction == "down":
            new_pos = [pos[0] + 1, pos[1]]
        else:
            raise ValueError("wrong directions")

        if self._can_move(new_pos):
            self.current_block_pos = new_pos
        elif direction == "down":
            self._land_block()
            self._burn()
            self._place_new_block()

    def drop(self):
        """Move to very very bottom"""

        i = 1
        while self._can_move((self.current_block_pos[0] + 1, self.current_block_pos[1])):
            i += 1
            self.move_block("down")

        self._land_block()
        self._burn()
        self._place_new_block()

    def _get_new_board(self):
        return [[0 for _ in range(self.width)] for _ in range(self.height)]

    def _place_new_block(self):
        """Place new block and generate the next one"""

        if self.next_block is None:
            self.current_block = self._get_new_block()
            self.next_block = self._get_new_block()
        else:
            self.current_block = self.next_block
            self.next_block = self._get_new_block()

        col_pos = math.floor((self.width - self.current_block.size[1]) / 2)
        self.current_block_pos = [0, col_pos]

        if self._check_overlapping(self.current_block_pos):
            self.game_over = True
            self._save_best_score()
        else:
            self.score += 5

    def _land_block(self):
        """Put block to the board and generate a new one"""

        for row in range(self.current_block.size[0]):
            for col in range(self.current_block.size[1]):
                if self.current_block.shape[row][col] == 1:
                    self.board[self.current_block_pos[0] + row][self.current_block_pos[1] + col] = 1

    def _burn(self):
        """Remove matched lines"""

        for row in range(self.height):
            if all(col != 0 for col in self.board[row]):
                for r in range(row, 0, -1):
                    self.board[r] = self.board[r - 1]
                self.board[0] = [0 for _ in range(self.width)]
                self.score += 100
                self.lines += 1
                if self.lines % 10 == 0:
                    self.level += 1

    def _check_overlapping(self, pos):
        """If current block overlaps any other on the board"""

        for row in range(self.current_block.size[0]):
            for col in range(self.current_block.size[1]):
                if self.current_block.shape[row][col] == 1:
                    if self.board[pos[0] + row][pos[1] + col] == 1:
                        return True
        return False

    def _can_move(self, pos):
        """Check if move is possible"""

        if pos[1] < 0 or pos[1] + self.current_block.size[1] > self.width \
                or pos[0] + self.current_block.size[0] > self.height:
            return False

        return not self._check_overlapping(pos)

    def _save_best_score(self):
        """Save best score to file"""

        if self.best_score < self.score:
            with open(BEST_SCORE_FILE_NAME, "w") as file:
                file.write(str(self.score))

    @staticmethod
    def _read_best_score():
        """Read best score from file"""

        if os.path.exists(f"./{BEST_SCORE_FILE_NAME}"):
            with open(BEST_SCORE_FILE_NAME) as file:
                return int(file.read())
        return 0

    @staticmethod
    def _get_new_block():
        """Get random block"""

        return Block(random.randint(0, len(block_shapes) - 1))


class Block:
    """Block representation"""

    def __init__(self, block_type):
        self.shape = block_shapes[block_type]
        self.color = block_type + 1
        self.size = self._get_size()

    def rotate(self):
        """Every time rotate clockwise 90"""

        self.shape = list(map(list, zip(*self.shape[::-1])))
        self.size = self._get_size()

    def _get_size(self):
        return [len(self.shape), len(self.shape[0])]
