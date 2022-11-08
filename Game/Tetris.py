import pygame, sys
from copy import deepcopy
from Game import config
from random import choice, randrange
import numpy as np

class Tetris:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(config.resolution)
        self.clock = pygame.time.Clock()
        self.running = True
        self.grid = [[pygame.Rect(x * config.tile_size, y*config.tile_size, config.tile_size,config.tile_size) for y in range(config.height)] for x in range(config.width)]
        self.figures = [[pygame.Rect(x + config.width // 2, y + 1, 1, 1) for x, y in fig_pos] for fig_pos in config.figures_pos]
        self.figure_rect = pygame.Rect(0, 0, config.tile_size - 2, config.tile_size - 2)
        self.current_figure = deepcopy(choice(self.figures))
        self.figure_dx = 0
        self.rotate = False 
        self.anim_count = 0
        self.anim_limit = config.anim_limit_relaxed
        self.game_field = [[0 for _ in range(config.height)] for _ in range(config.width)]
        self.score = 0


    #main loop of the game
    def run(self):
        while self.running:
            self.events()
            self.update()
            self.draw()
            pygame.time.delay(50) 
        pygame.quit()
        sys.exit()
    
    #1 step of the game for the Ai
    def step(self):
        self.draw()
        self.update()
        self.events()
        # pygame.time.delay(50)
    
    def events(self):
        for event in pygame.event.get():
            if event.type== pygame.QUIT:
                self.running=False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.figure_dx = -1
                if event.key == pygame.K_RIGHT:
                    self.figure_dx = 1
                if event.key == pygame.K_DOWN:
                    self.anim_limit = config.anim_limit_pressed
                if event.key == pygame.K_UP:
                    self.rotate = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    self.anim_limit = config.anim_limit_relaxed

                    

    def update(self):
        # move figure along the x axis
        temp_figure = deepcopy(self.current_figure)
        for i in range(4):
            self.current_figure[i].x += self.figure_dx
            if(not Tetris.check_borders(self.current_figure[i], self.game_field)):
                self.current_figure = deepcopy(temp_figure)
                break

        # move figure along the y axis
        self.anim_count += config.anim_speed
        if self.anim_count > self.anim_limit:
            self.anim_count = 0
            temp_figure = deepcopy(self.current_figure)
            for i in range(4):
                self.current_figure[i].y += 1
                if(not Tetris.check_borders(self.current_figure[i], self.game_field)):
                    for j in range(4):
                        self.game_field[temp_figure[j].x][temp_figure[j].y] = 1
                    self.current_figure = deepcopy(choice(self.figures))
                    break
        
        # rotate figure
        if(self.rotate):
            temp_figure = deepcopy(self.current_figure)
            centre = self.current_figure[0]
            for i in range(4):
                x = self.current_figure[i].y - centre.y
                y = self.current_figure[i].x - centre.x
                self.current_figure[i].x = centre.x - x
                self.current_figure[i].y = centre.y + y
                if not Tetris.check_borders(self.current_figure[i],self.game_field):
                    self.current_figure = deepcopy(temp_figure)
            self.rotate = False
        
        # remove full horizontal lines
        full_rows = []
        for row in range(config.height):
            count = np.array(self.game_field).T[row].sum()
            if(count == config.width):
                full_rows.append(row)
                self.score += config.width
        if(len(full_rows)!=0):
            game_field = np.array(self.game_field).T
            for row in full_rows:
                game_field[1:row+1] = game_field[0:row] 
            self.game_field = list(game_field.T)


        # check game over
        if np.array(self.game_field).T[0].sum() > 0:
            print("Game over")


        self.figure_dx = 0
        self.clock.tick()


    def draw(self):
        self.screen.fill(pygame.Color('black'))

        for x in range(config.width):
            for y in range(config.height):
                pygame.draw.rect(self.screen, (config.tile_size,config.tile_size,config.tile_size), self.grid[x][y], 1)

        for tile in range(4):
            self.figure_rect.x = self.current_figure[tile].x * config.tile_size
            self.figure_rect.y = self.current_figure[tile].y * config.tile_size
            pygame.draw.rect(self.screen, pygame.Color("white"),self.figure_rect)
        
        for x in range(config.width):
            for y in range(config.height):
                if(self.game_field[x][y]==1):
                    self.figure_rect.x, self.figure_rect.y = x*config.tile_size, y*config.tile_size
                    pygame.draw.rect(self.screen, pygame.Color("white"),self.figure_rect)

            
        pygame.display.update()


    @staticmethod
    def check_borders(figure, game_field):
        if figure.x < 0 or figure.x>(config.width-1):
            return False
        elif figure.y > (config.height-1) or figure.y < (0) or game_field[figure.x][figure.y]:
            return False
        return True
