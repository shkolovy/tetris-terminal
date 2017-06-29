"""
   #####   ####  #####   ###    #   ####
     #     #       #     #  #      #
 *   #     ###     #     # #    #   ###   *
     #     #       #     #  #   #      #
     #     ####    #     #   #  #  ####

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

import curses
import random


GAME_WINDOW_WIDTH = 25
GAME_WINDOW_HEIGHT = 19

HELP_WINDOW_WIDTH = 18
HELP_WINDOW_HEIGHT = 8

STATUS_WINDOW_WIDTH = 18
STATUS_WINDOW_HEIGHT = 10

TITLE_HEIGHT = 6


def init_screen():
    screen = curses.initscr()
    curses.beep()
    curses.noecho()
    curses.cbreak()
    curses.start_color()
    curses.curs_set(0)

    init_colors()

    return screen


def init_colors():
    # grey for dots
    curses.init_pair(99, 8, curses.COLOR_BLACK)
    curses.init_pair(98, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(97, curses.COLOR_RED, curses.COLOR_BLACK)

    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_BLUE)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_RED)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_YELLOW)
    curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_GREEN)


def init_game_window():
    window = curses.newwin(GAME_WINDOW_HEIGHT, GAME_WINDOW_WIDTH, TITLE_HEIGHT, 3)
    # window.nodelay(True)
    window.keypad(1)

    return window


def init_help_window():
    window = curses.newwin(HELP_WINDOW_HEIGHT, HELP_WINDOW_WIDTH, TITLE_HEIGHT + STATUS_WINDOW_HEIGHT + 1, GAME_WINDOW_WIDTH + 5)
    return window


def init_status_window():
    window = curses.newwin(STATUS_WINDOW_HEIGHT, STATUS_WINDOW_WIDTH, TITLE_HEIGHT, GAME_WINDOW_WIDTH + 5)
    return window


def draw_game_window(window):
    window.clear()
    window.border()

    # draw dots
    for row in range(1, GAME_WINDOW_HEIGHT - 1, 2):
        for col in range(1, GAME_WINDOW_WIDTH - 2, 2):
            window.addstr(row, col, " . ", curses.color_pair(99))

    window.addstr(4 + 4, 1, f"  ", curses.color_pair(3))
    window.addstr(5 + 4, 1, f"  ", curses.color_pair(3))
    window.addstr(6 + 4, 1, f"  ", curses.color_pair(3))
    window.addstr(7 + 4, 1, f"  ", curses.color_pair(3))

    window.addstr(y+3+4, x + 3, f"  ", curses.color_pair(1))
    window.addstr(y+4+4, x + 3, f"  ", curses.color_pair(1))
    window.addstr(y+5+4, x + 3, f"    ", curses.color_pair(1))

    window.addstr(3 + 4, 7, f"  ", curses.color_pair(2))
    window.addstr(4 + 4, 5, f"      ", curses.color_pair(2))

    window.refresh()


def draw_status_window(window):
    window.border()

    score = 200

    window.addstr(1, 2, f"Score: {score}")
    window.addstr(2, 2, "Next block:")

    window.addstr(4, 4, f"  ", curses.color_pair(1))
    window.addstr(5, 4, f"  ", curses.color_pair(1))
    window.addstr(6, 4, f"    ", curses.color_pair(1))

    window.refresh()


def draw_help_window(window):
    window.border()
    title = "Controls"
    window.addstr(0, int(HELP_WINDOW_WIDTH / 2 - len(title) / 2), title)

    window.addstr(2, 2, "Move   - ← ↓ →")
    window.addstr(3, 2, "Drop   - space")
    window.addstr(4, 2, "Rotate - ↑")
    window.addstr(5, 2, "Pause  - p")
    window.addstr(6, 2, "Quit   - q")

    window.refresh()


def draw_title():
    window = curses.newwin(TITLE_HEIGHT, 50, 1, 3)
    window.addstr(0, 4, "#####  ####  #####  ###    #   ####", curses.color_pair(98))
    window.addstr(1, 4, "  #    #       #    #  #      #", curses.color_pair(98))
    window.addstr(2, 4, "  #    ###     #    # #    #   ###", curses.color_pair(98))
    window.addstr(3, 4, "  #    #       #    #  #   #      #", curses.color_pair(98))
    window.addstr(4, 4, "  #    ####    #    #   #  #  ####", curses.color_pair(98))

    window.addstr(2, 0, " *", curses.color_pair(97))
    window.addstr(2, 41, " *", curses.color_pair(97))

    window.refresh()


def draw_footer():
    window = curses.newwin(1, 50, TITLE_HEIGHT + GAME_WINDOW_HEIGHT + 1, 10)
    window.addstr(0, 9, "Made with", curses.color_pair(98))
    window.addstr(0, 19, "❤", curses.color_pair(97))

    window.refresh()


block_types = {
    1: [[0, 1, 0],
        [1, 1, 1]],
    2: [[1, 0],
        [1, 0],
        [1, 1]],
    3: [[0, 1, 1],
        [1, 1, 0]],
    4: [[1, 1],
        [1, 1]],
    5: [[1, 1, 1, 1]]
}


class Board:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.board = [[0 for _ in range(col)] for _ in range(row)]

        self.current_block = None

    def print_current_block(self):
        self.current_block.print()

    def get_start_position(self):
        return int(self.col / 2 - self.current_block.size()[1] / 2)

    def put_current_block(self):
        start_row = 0
        start_col = self.get_start_position()
        block_size = self.board.current_block.size()

        for r in range(block_size[0]):
            for c in range(block_size[1]):
                self.board[start_row + r][start_col + c] = self.current_block.block()[r][c]

    def land_block(self):
        pass

    def move_block(self):
        pass

    def generate_block(self):
        self.current_block = Block(random.randint(1, len(block_types)))

    def rotate_block(self):
        self.current_block.rotate()


class Block:
    def __init__(self, block_type):
        self.shape = block_types[block_type]

    def size(self):
        return len(self.shape()), len(self.shape()[0])

    def block(self):
        """Link to current block shape (can be rotated)"""
        return self.shape

    def rotate(self):
        """Every time rotate clockwise 90"""
        self.shape = list(map(list, zip(*self.shape[::-1])))


# class BlockT(Block):
#     def __init__(self):
#         super().__init__([[0, 1, 0],
#                           [1, 1, 1]])
#
#
# class BlockL(Block):
#     def __init__(self):
#         super().__init__([[1, 0],
#                           [1, 0],
#                           [1, 1]])
#
#
# class BlockS(Block):
#     def __init__(self):
#         super().__init__([[0, 1, 1],
#                           [1, 1, 0]])
#
#
# class BlockI(Block):
#     def __init__(self):
#         super().__init__([[1, 1, 1, 1]])
#
#
# class BlockO(Block):
#     def __init__(self):
#         super().__init__([[1, 1],
#                           [1, 1]])

x = 0
y = 0

if __name__ == "__main__":
    try:
        screen = init_screen()

        draw_title()
        draw_footer()

        game_window = init_game_window()
        help_window = init_help_window()
        status_window = init_status_window()

        draw_game_window(game_window)
        draw_help_window(help_window)
        draw_status_window(status_window)

        # screen.clear()
        # screen.refresh()

        quit_game = False

        while not quit_game:
            key_event = game_window.getch()

            if key_event == curses.KEY_UP:
                y -= 2
                pass
            elif key_event == curses.KEY_DOWN:
                y += 2
                pass
            elif key_event == curses.KEY_LEFT:
                x -= 2
                pass
            elif key_event == curses.KEY_RIGHT:
                x += 2
                pass
            elif key_event == ord(" "):
                y = 8
                pass
            elif key_event == ord("q"):
                quit_game = True
            elif key_event == ord("p"):
                pass

            draw_game_window(game_window)
    finally:
        curses.endwin()
