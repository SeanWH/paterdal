"""
   An implementation of WORDLE(tm) designed with the visually impaired
   in mind.
"""
import sqlite3
import random
import datetime

import pygame

from more_itertools import collapse


# pylint: disable=no-member

class Paterdal:
    """
    The implementation
    """
    def __init__(
            self,
            col_offset=10,
            row_offset=10,
            h_tile_size=80,
            v_tile_size=80,
            cols=5,
            rows=6,
            line_width=4,
            line_color=(0, 0, 0),
            background_color=(255, 255, 255),
    ):
        """Initializes the game
        :param col_offset:
        :param row_offset:
        :param h_tile_size:
        :param v_tile_size:
        :param line_width:
        :param line_color:
        :param background_color:
        """

        # Initialize pygame
        pygame.init()

        # 8x8 square board
        self.cols = cols
        self.rows = rows

        self.board = {
            1: ["", "", "", "", ""],
            2: ["", "", "", "", ""],
            3: ["", "", "", "", ""],
            4: ["", "", "", "", ""],
            5: ["", "", "", "", ""],
            6: ["", "", "", "", ""]
        }

        self.col_offset = col_offset
        self.row_offset = row_offset
        self.h_tile_size = h_tile_size
        self.v_tile_size = v_tile_size
        self.line_width = line_width
        self.line_color = line_color
        self.back_color = background_color

        self.current_try = 1
        self.current_cell = 0

        # Set up the PyGame window:
        self.width = round(2 * self.col_offset + self.cols * self.h_tile_size)
        self.height = round(2 * self.row_offset + self.rows * self.v_tile_size)
        self.screen = pygame.display.set_mode((self.width, self.height),
                                              pygame.RESIZABLE
                                              )

        # Set window title:
        pygame.display.set_caption("Paterdal")

        # Manage how frequently the screen updates
        self.clock = pygame.time.Clock()

        self.word = self.get_word_from_db()
        self.letters = self.split_word(self.word)

        # Draw the board
        self.draw_board()

    def split_word(self, word):
        """
        Splits word into its individual letters and
        returns that as a list.
        :param word:
        :return:
        """
        letters = []
        for letter in word:
            letters.append(letter)

        return letters

    def get_word_from_db(self):
        """
        Gets the word used from the database
        :return:
        """
        database = sqlite3.connect("wordlist.db")
        db_cursor = database.cursor()
        alpha_indices = db_cursor.execute(
            "SELECT DISTINCT alpha_idx FROM words"
            )
        index_list = list(collapse(alpha_indices.fetchall()))

        use_date = "2022-01-01"

        while use_date != "":
            index = random.choice(index_list)
            word_data = db_cursor.execute(
                "SELECT word, used_date FROM words WHERE alpha_idx = :index",
                index
            )
            word_list = word_data.fetchall()
            word, use_date = random.choice(word_list)

        # mark the word as used
        use_date = datetime.date.today()
        db_cursor.execute(
            "UPDATE words SET used_date = :use_date WHERE word = :word",
            [use_date, word]
            )
        database.commit()
        database.close()
        return word

    def is_alpha_key(self, event_key):
        """
        Is the key pressed a letter key?
        :param event_key:
        :return:
        """
        return event_key in [
            pygame.K_a, pygame.K_b, pygame.K_c, pygame.K_d, pygame.K_e,
            pygame.K_f, pygame.K_g, pygame.K_h, pygame.K_i, pygame.K_j,
            pygame.K_k, pygame.K_l, pygame.K_m, pygame.K_n, pygame.K_o,
            pygame.K_p, pygame.K_q, pygame.K_r, pygame.K_s, pygame.K_t,
            pygame.K_u, pygame.K_v, pygame.K_w, pygame.K_x, pygame.K_y,
            pygame.K_z
        ]

    def get_letter(self, attempt, col):
        """
        Returns a specific letter from a specific guess
        :param attempt:
        :param col:
        :return:
        """
        row = self.board[attempt]
        return row[col]

    def get_guess(self, attempt):
        """
        Returns the entire list of letters from the guess
        :param attempt:
        :return:
        """
        return self.board[attempt]

    def calculate_points(self, col, row):
        """
        Calculates the points of a given cell on the board, based
        on the cell's col, row, and offsets.
        :param col:
        :param row:
        :return:
        """
        col_offset = round(self.col_offset)
        row_offset = round(self.row_offset)

        x_start = col_offset + self.h_tile_size * col
        y_start = row_offset + self.v_tile_size * row
        x_end = x_start + self.h_tile_size
        y_end = y_start + self.v_tile_size
        points = [
            (x_start, y_start),
            (x_end, y_start),
            (x_end, y_end),
            (x_start, y_end),
        ]

        return points

    def draw_board(self):
        """Displays the grid"""

        self.screen.fill(self.back_color)

        for row in range(self.rows):
            for col in range(self.cols):
                points = self.calculate_points(col, row)
                pygame.draw.lines(self.screen, self.line_color, True, points,
                                  self.line_width
                                  )

    def get_size(self,
                 col_offset=-1,
                 row_offset=-1,
                 cols=-1,
                 rows=-1,
                 h_tile_size=-1,
                 v_tile_size=-1
                 ):
        """
        Returns the calculated size of the board based on the
        above parameters.
        :param col_offset:
        :param row_offset
        :param cols:
        :param rows:
        :param h_tile_size:
        :param v_tile_size:
        :return:
        """

        col_offset = self.col_offset if col_offset < 0 else col_offset
        row_offset = self.row_offset if row_offset < 0 else row_offset
        cols = self.cols if cols < 0 else cols
        rows = self.rows if rows < 0 else rows
        h_tile_size = self.h_tile_size if h_tile_size < 0 else h_tile_size
        v_tile_size = self.v_tile_size if v_tile_size < 0 else v_tile_size

        # Squares...
        tile_size = max(h_tile_size, v_tile_size)
        self.h_tile_size = tile_size
        self.v_tile_size = tile_size

        width = round((2 * col_offset) + cols * tile_size)
        height = round((2 * row_offset) + rows * tile_size)

        return width, height

    def calculate_new_size(self, width, height):
        """
        Determines the new size of the resized screen
        :param width:
        :param height:
        :return:
        """

        current_width, current_height = self.get_size()

        width_ratio = width / current_width
        height_ratio = height / current_height

        self.col_offset *= width_ratio
        self.row_offset *= height_ratio
        self.v_tile_size *= width_ratio
        self.h_tile_size *= height_ratio

        return self.get_size()

    def resize(self, new_width, new_height):
        """
        Resizes the board.
        :param new_width:
        :param new_height:
        :return:
        """
        width = 200 if new_width < 200 else new_width
        height = 300 if new_height < 300 else new_height

        new_width, new_height = self.calculate_new_size(width, height)

        self.screen = pygame.display.set_mode((new_width, new_height),
                                              pygame.RESIZABLE
                                              )

        self.draw_board()

    def start(self):
        """PyGame event loop"""

        # Event loop:
        finished = False
        while not finished:

            # Process any new PyGame events:
            for event in pygame.event.get():

                # Mouse moved over the PyGame window:
                if event.type == pygame.MOUSEMOTION:
                    pass

                # Mouse button was released over the PyGame window:
                if event.type == pygame.MOUSEBUTTONUP:
                    pass

                # Implement scrollable screen
                # scrolls by ROWS, not incrementally
                if event.type == pygame.MOUSEWHEEL:
                    pass

                # PyGame window was resized:
                if event.type == pygame.VIDEORESIZE:
                    self.resize(event.w, event.h)

                # User closed the window:
                if event.type == pygame.QUIT:
                    finished = True

                # Some key was pressed:
                if event.type == pygame.KEYDOWN:
                    # If the pressed key was ESC, exit:
                    if event.key == pygame.K_ESCAPE:
                        finished = True
                    # If the pressed key was DOWN ARROW, scroll screen
                    # one row down
                    if event.key == pygame.K_DOWN:
                        pass
                    # If the pressed key was UP ARROW, scroll screen
                    # one row up
                    if event.key == pygame.K_UP:
                        pass
                    # Handle alpha keys here
                    if self.is_alpha_key(event.key):
                        pass

            # Limit refresh rate to 20 frames per second:
            self.clock.tick(20)

            # Refresh the screen:
            pygame.display.update()

        # Terminate PyGame:
        pygame.quit()


P = Paterdal()
P.start()
