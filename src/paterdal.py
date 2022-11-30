import pygame
import numpy
import matplotlib


class Paterdal:
    """
    An implementation of WORDLE(tm) designed with the visually impaired
    in mind.
    """

    def __init__(
            self,
            col_offset=10,
            row_offset=10,
            h_tile_size=80,
            v_tile_size=80,
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
        self.cols = 5
        self.rows = 6

        self.col_offset = col_offset
        self.row_offset = row_offset
        self.h_tile_size = h_tile_size
        self.v_tile_size = v_tile_size
        self.line_width = line_width
        self.line_color = line_color
        self.back_color = background_color

        # Set up the PyGame window:
        self.width = round(2 * self.col_offset + self.cols * self.h_tile_size)
        self.height = round(2 * self.row_offset + self.rows * self.v_tile_size)
        self.screen = pygame.display.set_mode((self.width, self.height))

        # Set window title:
        pygame.display.set_caption("Paterdal")

        # Manage how frequently the screen updates
        self.clock = pygame.time.Clock()

        # Draw the board
        self.draw_board()

    def draw_board(self):
        """Displays the grid"""

        # Fill the PyGame window with white color:
        color = self.back_color  # white
        self.screen.fill(color)

        # Set common square attributes
        color = self.line_color  # black
        lw = self.line_width  # line width
        col_offset = round(self.col_offset)
        row_offset = round(self.row_offset)

        for r in range(self.rows):
            for c in range(self.cols):
                x_start = col_offset + self.h_tile_size * c
                y_start = row_offset + self.v_tile_size * r
                x_end = x_start + self.h_tile_size
                y_end = y_start + self.v_tile_size
                points = [
                    (x_start, y_start),
                    (x_end, y_start),
                    (x_end, y_end),
                    (x_start, y_end),
                ]
                pygame.draw.lines(self.screen, color, True, points, lw)

    def get_size(self,
                 col_offset=-1,
                 row_offset=-1,
                 cols=-1,
                 rows=-1,
                 h_tile_size=-1,
                 v_tile_size=-1
                 ):
        """
        Returns either the calculated size of the board based on the
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
        cols = self.cols if cols < 0 else self.cols
        rows = self.rows if rows < 0 else self.rows
        h_tile_size = self.h_tile_size if h_tile_size < 0 else self.h_tile_size
        v_tile_size = self.v_tile_size if v_tile_size < 0 else self.v_tile_size

        c = round(col_offset + cols * h_tile_size)
        r = round(row_offset + rows * v_tile_size)

        return c, r

    def resize(self, new_width, new_height):
        new_size = min(new_width, new_height)
        new_size = 200 if new_size < 200 else new_size

        c, r = self.get_size()
        delta_c = new_size / c
        delta_r = new_size / r

        self.col_offset *= delta_c
        self.row_offset *= delta_r
        self.h_tile_size *= delta_c
        self.v_tile_size *= delta_r

        # recalculate the new size with the new
        # offset and tile_size
        c, r = self.get_size()

        self.screen = pygame.display.set_mode((c, r),
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

            # Limit refresh rate to 20 frames per second:
            self.clock.tick(20)

            # Refresh the screen:
            pygame.display.update()

        # Terminate PyGame:
        pygame.quit()


P = Paterdal()
P.start()
