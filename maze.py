import pygame
from block import Block
from fruit import Fruit
from random import randrange


class Maze:
    BLUE = (25, 25, 166)
    WHITE = (255, 255, 255)
    PELLET_YELLOW = (255, 255, 0)

    def __init__(self, screen, maze_map_file):
        self.screen = screen
        self.map_file = maze_map_file
        self.block_size = 20
        self.block_image = pygame.Surface((self.block_size, self.block_size))
        self.block_image.fill(Maze.BLUE)
        self.shield_image = pygame.Surface((self.block_size, self.block_size // 2))
        self.shield_image.fill(Maze.WHITE)
        self.pellet_image = pygame.Surface((self.block_size // 4, self.block_size // 4))
        pygame.draw.circle(self.pellet_image, Maze.PELLET_YELLOW,
                           (self.block_size // 8, self.block_size // 8), self.block_size // 8)
        self.ppellet_image = pygame.Surface((self.block_size // 2, self.block_size // 2))
        pygame.draw.circle(self.ppellet_image, Maze.WHITE,
                           (self.block_size // 4, self.block_size // 4), self.block_size // 4)
        with open(self.map_file, 'r') as file:
            self.map_lines = file.readlines()
        self.maze_blocks = pygame.sprite.Group()
        self.shield_blocks = pygame.sprite.Group()
        self.pellets = pygame.sprite.Group()
        self.power_pellets = pygame.sprite.Group()
        self.fruits = pygame.sprite.Group()
        self.player_spawn = None
        self.ghost_spawn = []
        self.build_maze()

    def pellets_left(self):

        return True if self.pellets or self.power_pellets else False

    def build_maze(self):
        if self.maze_blocks or self.pellets or self.fruits or self.power_pellets or self.shield_blocks:
            self.maze_blocks.empty()
            self.pellets.empty()
            self.power_pellets.empty()
            self.fruits.empty()
            self.shield_blocks.empty()
        if len(self.ghost_spawn) > 0:
            self.ghost_spawn.clear()
        y_start = self.screen.get_height() // 12
        y = 0
        for i in range(len(self.map_lines)):
            line = self.map_lines[i]
            x_start = self.screen.get_width() // 5
            x = 0
            for j in range(len(line)):
                co = line[j]
                if co == 'x':
                    self.maze_blocks.add(Block(x_start + (x * self.block_size),
                                               y_start + (y * self.block_size),
                                               self.block_size, self.block_size,
                                               self.block_image))
                elif co == '*':
                    if randrange(0, 100) > 1:
                        self.pellets.add(Block(x_start + (self.block_size // 3) + (x * self.block_size),
                                               y_start + (self.block_size // 3) + (y * self.block_size),
                                               self.block_size, self.block_size,
                                               self.pellet_image))
                    else:
                        self.fruits.add(Fruit(x_start + (self.block_size // 4) + (x * self.block_size),
                                              y_start + (self.block_size // 4) + (y * self.block_size),
                                              self.block_size, self.block_size))
                elif co == '@':
                    self.power_pellets.add(Block(x_start + (self.block_size // 3) + (x * self.block_size),
                                                 y_start + (self.block_size // 3) + (y * self.block_size),
                                                 self.block_size, self.block_size,
                                                 self.ppellet_image))
                elif co == 's':
                    self.shield_blocks.add(Block(x_start + (x * self.block_size),
                                                 y_start + (y * self.block_size),
                                                 self.block_size // 2, self.block_size // 2,
                                                 self.shield_image))
                elif co == 'o':
                    self.player_spawn = [(i, j), (x_start + (x * self.block_size) + (self.block_size // 2),
                                         y_start + (y * self.block_size) + (self.block_size // 2))]
                elif co == 'g':
                    self.ghost_spawn.append(((i, j), (x_start + (x * self.block_size),
                                            y_start + (y * self.block_size))))
                x += 1
            y += 1

    def remove_shields(self):
        self.shield_blocks.empty()

    def blit(self):
        self.maze_blocks.draw(self.screen)
        self.pellets.draw(self.screen)
        self.power_pellets.draw(self.screen)
        self.fruits.draw(self.screen)
        self.shield_blocks.draw(self.screen)
