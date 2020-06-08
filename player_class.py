from data import *
import pygame
vec = pygame.math.Vector2

class Player:
    def __init__(self, pro, pos):
        self.pro = pro
        self.starting_pos = [pos.x, pos.y]
        self.grid_pos = pos
        self.pix_pos = self.get_pix_pos()
        self.direction = vec(1, 0)
        self.stored_direction = None
        self.movable = True
        self.current_score = 0
        self.speed = 1.04
        self.lives = 1

    def update(self):
        if self.movable:
            self.pix_pos += self.direction*self.speed
        if self.time_of_moving():
            if self.stored_direction != None:
                self.direction = self.stored_direction
            self.movable= self.can_move()

        self.grid_pos[0] = (self.pix_pos[0]-top_bottom_space +
                            self.pro.cell_width//2)//self.pro.cell_width+1
        self.grid_pos[1] = (self.pix_pos[1]-top_bottom_space+
                            self.pro.cell_height//2)//self.pro.cell_height+1
        if self.on_food():
            self.eat_food()

    def draw(self):
        pygame.draw.circle(self.pro.screen,(255,255,000), (int(self.pix_pos.x),
                                                            int(self.pix_pos.y)), self.pro.cell_width//2)


        for x in range(self.lives):
            pygame.draw.circle(self.pro.screen, (255,255,000), (30 + 20*x, height - 15), 7)

    def on_food(self):
        if self.grid_pos in self.pro.foods:
            if int(self.pix_pos.x+top_bottom_space//2) % self.pro.cell_width == 0:
                if self.direction == vec(1, 0) or self.direction == vec(-1, 0):
                    return True
            if int(self.pix_pos.y+top_bottom_space//2) % self.pro.cell_height == 0:
                if self.direction == vec(0, 1) or self.direction == vec(0, -1):
                    return True
        return False

    def eat_food(self):
        self.pro.foods.remove(self.grid_pos)
        self.current_score += 1

    def move(self, direction):
        self.stored_direction = direction

    def get_pix_pos(self):
        return vec((self.grid_pos[0]*self.pro.cell_width)+top_bottom_space//2+self.pro.cell_width//2,
                   (self.grid_pos[1]*self.pro.cell_height) +
                   top_bottom_space//2+self.pro.cell_height//2)

    def time_of_moving(self):
        if int(self.pix_pos.x+top_bottom_space//2) % self.pro.cell_width == 0:
            if self.direction == vec(1, 0) or self.direction == vec(-1, 0) or self.direction == vec(0, 0):
                return True
        if int(self.pix_pos.y+top_bottom_space//2) % self.pro.cell_height == 0:
            if self.direction == vec(0, 1) or self.direction == vec(0, -1) or self.direction == vec(0, 0):
                return True

    def can_move(self):
        for block in self.pro.blocks:
            if vec(self.grid_pos+self.direction) == block:
                return False
        return True