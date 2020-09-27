from board import Board

import pygame


class DrawableBoard(Board):
    def __init__(self, m, n, x, y, width, height, separation, color):
        Board.__init__(self, m, n)
        self.x, self.y = x, y
        self.w, self.h = width, height
        self.c = color
        self.s = separation

    def square_dimension(self):
        square_w = self.w // self.n - self.s
        square_h = self.h // self.m - self.s
        return square_w, square_h

    def get_position_on_board(self, x, y, square_w, square_h):
        x = self.x + x * square_w + x * self.s
        y = self.y + y * square_h + y * self.s
        return x, y

    def draw(self, surface):
        square_w, square_h = self.square_dimension()
        for y in range(self.m):
            for x in range(self.n):
                square_x, square_y = self.get_position_on_board(x, y, square_w, square_h)
                pygame.draw.rect(surface, self.c, (square_x, square_y, square_w, square_h), 1)
