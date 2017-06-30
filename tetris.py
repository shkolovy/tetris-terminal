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
import math

BOARD_WIDTH = 10
BOARD_HEIGHT = 17

GAME_WINDOW_WIDTH = 2 * BOARD_WIDTH + 2
GAME_WINDOW_HEIGHT = BOARD_HEIGHT + 2

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
    """Init colors"""

    curses.init_pair(99, 8, curses.COLOR_BLACK)
    curses.init_pair(98, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(97, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(96, curses.COLOR_BLACK, curses.COLOR_CYAN)

    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_BLUE)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_RED)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_YELLOW)
    curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_GREEN)
    curses.init_pair(5, curses.COLOR_BLACK, curses.COLOR_MAGENTA)


def init_game_window():
    """Create and return game window"""

    window = curses.newwin(GAME_WINDOW_HEIGHT, GAME_WINDOW_WIDTH, TITLE_HEIGHT, 3)
    # window.nodelay(True)
    window.keypad(1)

    return window


def init_help_window():
    """Create and return help window"""

    window = curses.newwin(HELP_WINDOW_HEIGHT, HELP_WINDOW_WIDTH, TITLE_HEIGHT + STATUS_WINDOW_HEIGHT + 1,
                           GAME_WINDOW_WIDTH + 5)
    return window


def init_status_window():
    """Create and return status window"""

    window = curses.newwin(STATUS_WINDOW_HEIGHT, STATUS_WINDOW_WIDTH, TITLE_HEIGHT, GAME_WINDOW_WIDTH + 5)
    return window


def draw_game_window(window):
    """Draw game widnow"""

    window.border()

    # draw dots
    for row in range(1, GAME_WINDOW_HEIGHT - 1, 2):
        for col in range(1, GAME_WINDOW_WIDTH - 2, 2):
            window.addstr(row, col, ".", curses.color_pair(99))

    # draw board
    for a in range(BOARD_HEIGHT):
        for b in range(BOARD_WIDTH):
            if board.board[a][b] == 1:
                window.addstr(a + 1, 2 * b + 1, "  ", curses.color_pair(96))
            else:
                # hack: to avoid clearing
                window.addstr(a + 1, 2 * b + 1, "  ")

    # draw current block
    for a in range(board.current_block.size[0]):
        for b in range(board.current_block.size[1]):
            if board.current_block.shape[a][b] == 1:
                x = 2 * board.current_block_pos[1] + 2 * b + 1
                y = board.current_block_pos[0] + a + 1
                window.addstr(y, x, "  ", curses.color_pair(board.current_block.color))

    window.refresh()


def draw_status_window(window):
    """Draw status window"""

    # hack: avoid clearing (blinking)
    for row in range(1, STATUS_WINDOW_HEIGHT - 1):
        window.addstr(row, 2, "".rjust(STATUS_WINDOW_WIDTH - 3, " "))

    window.border()

    score = random.randint(1, 3000)

    window.addstr(1, 2, f"Score: {score}")
    window.addstr(2, 2, "Next block:")

    start_col = int(STATUS_WINDOW_WIDTH / 2 - board.next_block.size[1])

    for row in range(board.next_block.size[0]):
        for col in range(board.next_block.size[1]):
            if board.next_block.shape[row][col] == 1:
                window.addstr(4 + row, start_col + 2 * col, "  ", curses.color_pair(board.next_block.color))

    window.refresh()


def draw_help_window(window):
    """Draw help window"""

    window.border()
    title = "Controls"
    window.addstr(0, int(HELP_WINDOW_WIDTH / 2 - len(title) / 2), title)

    window.addstr(1, 2, "Move   - ← ↓ →")
    window.addstr(2, 2, "Drop   - space")
    window.addstr(3, 2, "Rotate - ↑")
    window.addstr(4, 2, "Pause  - p")
    window.addstr(5, 2, "Quit   - q")

    window.refresh()


def draw_title():
    """Draw title"""

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


block_shapes = [
    # t block
    [[0, 1, 0],
     [1, 1, 1]],
    # l block
    [[1, 0],
     [1, 0],
     [1, 1]],
    # s block
    [[0, 1, 1],
     [1, 1, 0]],
    # o block
    [[1, 1],
     [1, 1]],
    # i block
    [[1, 1, 1, 1]]
]


class Board:
    """Board representation"""

    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.board = [[0 for _ in range(width)] for _ in range(height)]

        self.current_block_pos = None
        self.current_block = None
        self.next_block = None

    def start(self):
        """Start game"""

        self.place_new_block()

    def place_new_block(self):
        """Place new block and generate the next one"""

        if self.next_block is None:
            self.current_block = self._generate_block()
            self.next_block = self._generate_block()
        else:
            self.current_block = self.next_block
            self.next_block = self._generate_block()

        col_pos = math.ceil((self.width - self.current_block.size[1]) / 2)
        self.current_block_pos = [0, col_pos]

    def _land_block(self):
        """Put block to the board and generate a new one"""

        for row in range(self.current_block.size[0]):
            for col in range(self.current_block.size[1]):
                if self.current_block.shape[row][col] == 1:
                    self.board[self.current_block_pos[0] + row][self.current_block_pos[1] + col] = 1

        self.place_new_block()

    def check_game_over(self):
        pass

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

    def drop(self):
        """Move to very very bottom"""

        i = 1
        while self._can_move((self.current_block_pos[0]+1, self.current_block_pos[1])):
            i += 1
            self.move_block("down")

        self._land_block()
        self._burn()

    def _burn(self):
        """Remove matched lines"""

        for row in range(BOARD_HEIGHT):
            if sum(self.board[row]) == BOARD_WIDTH:
                for r in range(row, 0, -1):
                    self.board[r] = self.board[r-1]

    def _can_move(self, to_pos):
        """Check if move is possible"""

        if to_pos[1] < 0 or to_pos[1] + self.current_block.size[1] > BOARD_WIDTH \
                or to_pos[0] + self.current_block.size[0] > BOARD_HEIGHT:
            return False

        for row in range(self.current_block.size[0]):
            for col in range(self.current_block.size[1]):
                if self.current_block.shape[row][col] == 1:
                    if self.board[to_pos[0] + row][to_pos[1] + col] == 1:
                        return False
        return True

    @staticmethod
    def _generate_block():
        """Get random block"""

        block_type = random.randint(0, len(block_shapes) - 1)
        return Block(block_type)

    def rotate_block(self):
        """Rotate block"""

        self.current_block.rotate()


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


board = Board(BOARD_HEIGHT, BOARD_WIDTH, )
board.start()

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

        # screen.clear()
        # screen.refresh()

        quit_game = False

        while not quit_game:
            draw_status_window(status_window)

            key_event = game_window.getch()

            if key_event == curses.KEY_UP:
                board.current_block.rotate()
            elif key_event == curses.KEY_DOWN:
                board.move_block("down")
            elif key_event == curses.KEY_LEFT:
                board.move_block("left")
            elif key_event == curses.KEY_RIGHT:
                board.move_block("right")
            elif key_event == ord(" "):
                board.drop()
            elif key_event == ord("q"):
                quit_game = True
            elif key_event == ord("p"):
                pass

            draw_game_window(game_window)

    finally:
        curses.endwin()
