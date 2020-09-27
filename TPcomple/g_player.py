from player import Player

import pygame

from util import *


class DrawablePlayer(Player):
    def __init__(self, n_player, board, color):
        Player.__init__(self, n_player, board)
        self.n_player = n_player
        self.c = color

    def draw(self, board, surface):
        square_w, square_h = board.square_dimension()
        x, y = get_position_from_player_number(self, board)
        x, y = board.get_position_on_board(x, y, square_w, square_h)
        pygame.draw.ellipse(surface, self.c, (x, y, square_w, square_h))
