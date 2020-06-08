from data import *
import pygame
vec = pygame.math.Vector2


class Enemy:
    def __init__(self, ene, pos, number):
        self.ene = ene
        self.starting_pos = [pos.x, pos.y]
        self.grid_pos = pos
        self.pix_pos = self.get_pix_pos()
        self.radius = int(self.ene.cell_width//2)
        self.number = number
        self.colour = self.set_colour()
        self.direction = vec(0, 0)
        self.enemy_nature = self.set_enemy_nature()

    def update(self):

        self.grid_pos[0] = (self.pix_pos[0]-top_bottom_space +
                            self.ene.cell_width//2)//self.ene.cell_width+1
        self.grid_pos[1] = (self.pix_pos[1]-top_bottom_space +
                            self.ene.cell_height//2)//self.ene.cell_height+1

    def draw(self):
        pygame.draw.circle(self.ene.screen, self.colour,
                           (int(self.pix_pos.x), int(self.pix_pos.y)), self.radius)

    def time_to_move(self):
        if int(self.pix_pos.x+top_bottom_space//2) % self.ene.cell_width == 0:
            if self.direction == vec(1, 0) or self.direction == vec(-1, 0) or self.direction == vec(0, 0):
                return True
        if int(self.pix_pos.y+top_bottom_space//2) % self.ene.cell_height == 0:
            if self.direction == vec(0, 1) or self.direction == vec(0, -1) or self.direction == vec(0, 0):
                return True
        return False


    def get_pix_pos(self):
        return vec((self.grid_pos.x*self.ene.cell_width)+top_bottom_space//2+self.ene.cell_width//2,
                   (self.grid_pos.y*self.ene.cell_height)+top_bottom_space//2 +
                   self.ene.cell_height//2)

    def set_colour(self):
        if self.number == 0:
            return (255, 000, 000)
        if self.number == 1:
            return (000, 51, 255)
        if self.number == 2:
            return (102, 000, 255)
        if self.number == 3:
            return (000, 204, 000)

    def set_enemy_nature(self):
        if self.number == 0:
            return "red"
        elif self.number == 1:
            return "blue"
        elif self.number == 2:
            return "purple"
        else:
            return "green"