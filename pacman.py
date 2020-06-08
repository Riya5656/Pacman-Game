from enemy_class import *
from player_class import *
from data import *
import pygame,sys
pygame.init()
vec = pygame.math.Vector2
pygame.display.set_caption("Pacman")

class pman:
    def __init__(self):
        self.screen=pygame.display.set_mode((height,width))
        self.clock = pygame.time.Clock()
        self.run = True
        self.state = 'initial'
        self.cell_width=back_width// columns
        self.cell_height = back_height // rows
        self.blocks=[]
        self.foods=[]
        self.enemies=[]
        self.e_pos=[]
        self.p_pos=None
        self.load()
        self.img()
        self.player = Player(self, vec(self.p_pos))
        self.make_enemies()

    def play(self):
        while self.run:
            if self.state =='initial':
                self.initial_events()
                self.initial_update()
                self.initial_draw()

            elif self.state== 'playing':
                self.playing_events()
                self.playing_update()
                self.playing_draw()

            elif self.state=='game over':
                self.game_over_events()
                self.game_over_update()
                self.game_over_draw()

            else:
                self.running = False

            self.clock.tick(60)

        pygame.quit()
        sys.exit()

    #################### HELPFUL METHODS ########################

    def draw_text(self, words, screen, pos, size, colour, font_name, centered=False):
        font = pygame.font.SysFont(font_name, size)
        text = font.render(words, False, colour)
        text_size = text.get_size()
        if centered:
            pos[0] = pos[0] - text_size[0] // 2
            pos[1] = pos[1] - text_size[1] // 2
        screen.blit(text, pos)

    def load(self):
        self.back=pygame.image.load('pac_maze.png')
        self.back=pygame.transform.scale(self.back,(back_width,back_height))


        with open("blocks.txt",'r') as file:
            for y_index,line in  enumerate(file):
                for x_index,char in enumerate(line):
                    if char == "1":
                        self.blocks.append(vec(x_index,y_index))

                    elif char=="0":
                        self.foods.append(vec(x_index, y_index))

                    elif char=="P":
                        self.p_pos= [x_index,y_index]

                    elif char in ["2","3","4","5"]:
                        self.e_pos.append([x_index,y_index])
    def img(self):
        self.imag = pygame.image.load('pac.png')
        self.imag = pygame.transform.scale(self.imag, (50,50))

    def make_enemies(self):
        for index,pos in enumerate(self.e_pos):
            self.enemies.append(Enemy(self,vec(pos),index))

    def grid(self):
        for x in range(width//self.cell_width):
            pygame.draw.line(self.back,(107,107,107),(x*self.cell_width,0),(x*self.cell_width,height))

        for x in range(height//self.cell_height):
            pygame.draw.line(self.back,(107,107,107),(0,x*self.cell_height),(width,x*self.cell_height))

        for food in self.foods:
            pygame.draw.rect(self.back,(167,179,34),(food.x*self.cell_width,food.y*self.cell_height,self.cell_width,self.cell_height))

    def reset(self):
        self.player.lives = 1
        self.player.current_score = 0
        self.player.grid_pos = vec(self.player.starting_pos)
        self.player.pix_pos = self.player.get_pix_pos()
        self.player.direction *= 0
        for enemy in self.enemies:
            enemy.grid_pos = vec(enemy.starting_pos)
            enemy.pix_pos = enemy.get_pix_pos()
            enemy.direction *= 0

        self.foods = []
        with open("blocks.txt", 'r') as file:
            for yidx, line in enumerate(file):
                for xidx, char in enumerate(line):
                    if char == '0':
                        self.foods.append(vec(xidx, yidx))
        self.state = "playing"


    ################## STARTING METHODS ####################

    def initial_events(self):
        for event in pygame.event.get():
            if  event.type == pygame.QUIT:
                self.run = False
            if event.type==pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.state='playing'

    def initial_update(self):
        pass

    def initial_draw(self):
        self.screen.blit(self.imag, (int(width//2.2), int(height//3.6)))
        self.draw_text('PACMAN', self.screen,
                       [width // 2, height // 2.4], 28, (000, 51, 255), 'Comic Sans MS', centered=True)
        self.draw_text('PRESS SPACE BAR TO PLAY', self.screen,
                       [width // 2, height // 1.7], 28, (51, 255, 000), 'Comic Sans MS', centered=True)
        self.draw_text('HIGH SCORE:0', self.screen, [4, 1], 20, (255, 255, 000), 'Comic Sans MS')

        pygame.display.update()


    ################# PLAYING METHODS #################

    def playing_events(self):
        for event in pygame.event.get():
            if  event.type == pygame.QUIT:
                self.run = False
            if event.type==pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.player.move(vec(-1,0))
                if event.key == pygame.K_RIGHT:
                    self.player.move(vec(1, 0))
                if event.key == pygame.K_UP:
                    self.player.move(vec(0, -1))
                if event.key == pygame.K_DOWN:
                    self.player.move(vec(0, 1))


    def playing_update(self):
        self.player.update()
        for enemy in self.enemies:
            enemy.update()
        for enemy in self.enemies:
            if enemy.grid_pos==self.player.grid_pos:
                self.remove_life()

    def playing_draw(self):
         self.screen.fill((0,0,0))
         self.screen.blit(self.back, (top_bottom_space//2,top_bottom_space//2))
         self.draw_foods()
         #self.grid()
         self.draw_text('Current score:{}'.format(self.player.current_score), self.screen,[35,0], 18, (51, 255, 000), 'Comic Sans MS')
         self.draw_text('High score:0', self.screen, [width//2+65, 0], 18, (51, 255, 000), 'Comic Sans MS')
         self.player.draw()
         for enemy in self.enemies:
             enemy.draw()
         pygame.display.update()

    def remove_life(self):
        self.player.lives -= 1
        if self.player.lives == 0:
            self.state = "game over"
        else:
            self.player.grid_pos = vec(self.player.starting_pos)
            self.player.pix_pos = self.player.get_pix_pos()
            self.player.direction *= 0
            for enemy in self.enemies:
                enemy.grid_pos = vec(enemy.starting_pos)
                enemy.pix_pos = enemy.get_pix_pos()
                enemy.direction *= 0


    def draw_foods(self):
        for food in self.foods:
            pygame.draw.circle(self.screen,(204,153,000),(int(food.x*self.cell_width)+self.cell_width//2+top_bottom_space//2,
            int(food.y*self.cell_height)+self.cell_height//2+top_bottom_space//2),5)

 ############################# GAME OVER METHODS ####################################

    def game_over_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.reset()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False

    def game_over_update(self):
        pass


    def game_over_draw(self):
        self.screen.fill((0, 0, 0))
        quit_text = "Press the escape button to QUIT"
        again_text = "Press SPACE bar to PLAY AGAIN"
        self.draw_text("GAME OVER", self.screen, [width // 2, 100], 52, (208, 22, 22), "Comic Sans MS", centered=True)
        self.draw_text(again_text, self.screen, [
            width // 2, height // 2], 36, (190, 190, 190), "Comic Sans MS", centered=True)
        self.draw_text(quit_text, self.screen, [
            width // 2, height // 1.5], 36, (190, 190, 190), "Comic Sans MS", centered=True)
        pygame.display.update()

pac = pman()
pac.play()



