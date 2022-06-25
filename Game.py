from ctypes import sizeof
import pygame
import sys
import math

from urllib3 import Retry
from Player import Player

# Constantes
TILE_SIZE = 16
SCREEN_HEIGHT = 32*TILE_SIZE
SCREEN_WIDTH = SCREEN_HEIGHT

class Game():

    def __init__(self):
        # Initialisation de Pygame
        pygame.init()

        # Création de la fenêtre
        self.window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

        # Setup titre fenêtre
        pygame.display.set_caption("2D Genetic Algorithm")

        # Initialisation de la clock
        self.clock = pygame.time.Clock()

        # Initialisation de la carte
        self.map, self.map_size = self.getMap("map.txt")
        # Instanciation des murs
        self.walls = self.getWalls()

        # Initialisation des joueurs
        self.player = Player(24, 24)

        # Boucle de jeu
        self.start()

    def getMap(self, filename):
            f = open(filename, 'r')
            map = ""
            cpt = 0
            for line in f:
                line = line.split("\n")
                map = map + line[0]
                cpt += 1
            return map, cpt

    def getWalls(self):
        wall_list = []
        for row in range(self.map_size):
            for column in range(self.map_size):
                index = row*self.map_size + column
                l_index_x = row*self.map_size + column - 1
                n_index_x = row*self.map_size + column + 1
                l_index_y = (row - 1)*self.map_size + column 
                n_index_y = (row + 1)*self.map_size + column
                if self.map[index] == '#':
                    if (l_index_x > 0) and (l_index_x < 1024) and (self.map[l_index_x] == ' '):
                        wall_list.append(((column*TILE_SIZE, row*TILE_SIZE, column*TILE_SIZE, (row + 1)*TILE_SIZE)))
                    if (n_index_x > 0) and (n_index_x < 1024) and (self.map[n_index_x] == ' '):
                        wall_list.append((((column + 1)*TILE_SIZE, row*TILE_SIZE, (column + 1)*TILE_SIZE, (row + 1)*TILE_SIZE)))
                    if (l_index_y > 0) and (l_index_y < 1024) and (self.map[l_index_y] == ' '):
                        wall_list.append(((column*TILE_SIZE, row*TILE_SIZE, (column + 1)*TILE_SIZE, row*TILE_SIZE)))
                    if (n_index_y > 0) and (n_index_y < 1024) and (self.map[n_index_y] == ' '):
                        wall_list.append(((column*TILE_SIZE, (row + 1)*TILE_SIZE, (column + 1)*TILE_SIZE, (row + 1)*TILE_SIZE)))
        return(wall_list)

    def getIntercectionPoint(self, x1, y1, x2, y2, x3, y3, x4, y4):
        num = (x1 - x3)*(y1 - y2) - (y1 - y3)*(x1 - x2)
        denum = (x1 - x2)*(y3 - y4) - (y1 - y2)*(x3 - x4)
        u = num/denum
        if (0 <= u) and (u <= 1):
            inter_pt = (x3 + u*(x4 - x3), y3 + u*(y4 - y3))
            return True, inter_pt
        else:
            return False, (x2, y2)

    def drawMap(self):
        # Dessin de la carte
        self.clearMap()
        for row in range(self.map_size):
            for column in range(self.map_size):
                index = row*self.map_size + column
                if self.map[index] == '!':
                     pygame.draw.rect(
                        self.window,
                        (0, 255, 0),
                        (column*TILE_SIZE, row*TILE_SIZE, TILE_SIZE - 1, TILE_SIZE - 1)
                    )
                else:
                    pygame.draw.rect(
                        self.window,
                        (200, 200, 200) if self.map[index] == '#' else (100, 100, 100),
                        (column*TILE_SIZE, row*TILE_SIZE, TILE_SIZE - 1, TILE_SIZE - 1)
                    )
        # Dessin du joueur
        pygame.draw.circle(self.window, (255, 0, 0), (self.player.x, self.player.y), 5)
        for (x1, y1, x2, y2) in self.walls:
            test, pi = self.getIntercectionPoint(
                    self.player.x,
                    self.player.y,
                    self.player.x + math.sin(self.player.angle)*self.player.max_ray_length,
                    self.player.y + math.cos(self.player.angle)*self.player.max_ray_length,
                    x1,
                    y1,
                    x2,
                    y2
                )
            print(test, pi)
            if (test):
                pygame.draw.line(
                        self.window,
                        (0, 0, 255),
                        (self.player.x, self.player.y),
                        pi
                    )
                break
            
        for i in range(self.player.nb_ray//2):
            pygame.draw.line(
                self.window,
                (0, 0, 255),
                (self.player.x, self.player.y),
                (self.player.x + math.sin(self.player.angle + math.radians(self.player.fov/(2+i)))*self.player.max_ray_length,
                self.player.y + math.cos(self.player.angle + math.radians(self.player.fov/(2+i)))*self.player.max_ray_length)
            )
            pygame.draw.line(
                self.window,
                (0, 0, 255),
                (self.player.x, self.player.y),
                (self.player.x + math.sin(self.player.angle - math.radians(self.player.fov/(2+i)))*self.player.max_ray_length,
                self.player.y + math.cos(self.player.angle - math.radians(self.player.fov/(2+i)))*self.player.max_ray_length)
            )
    
    def clearMap(self):
        # Clear de la fenêtre
        self.window.fill((0, 0, 0))

    def start(self):
        while True:
            # Condition d'arrêt
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_z:
                        self.player.move_forward = 1
                    if event.key == pygame.K_s:
                        self.player.move_backward = 1
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_z:
                        self.player.move_forward = 0
                    if event.key == pygame.K_s:
                        self.player.move_backward = 0
            
            # Update player position
            cursor_x, cursor_y = pygame.mouse.get_pos()
            lx = cursor_x - self.player.x
            ly = cursor_y - self.player.y
            self.player.angle = math.atan2(lx, ly)
            self.player.x = self.player.x + (self.player.move_forward - self.player.move_backward)*self.player.speed*math.sin(self.player.angle)
            self.player.y = self.player.y + (self.player.move_forward - self.player.move_backward)*self.player.speed*math.cos(self.player.angle)
            
            # Draw map
            self.drawMap()

            # Mise à jour
            pygame.display.flip()

            # Setup des FPS
            self.clock.tick(30)

