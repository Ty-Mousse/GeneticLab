import pygame
import sys
import math
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
        pygame.draw.line(
                self.window,
                (0, 0, 255),
                (self.player.x, self.player.y),
                (self.player.x + math.sin(self.player.angle)*self.player.max_ray_length,
                self.player.y + math.cos(self.player.angle)*self.player.max_ray_length)
            )
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

