import pygame
import os
pygame.init()



SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
RED_COLOR = (255, 0, 0)
WHITE_COLOR = (255, 0, 0)
FPS = 60

PATH = os.path.dirname(__file__) + os.path.sep



####

#class map

#class tank

#class enemy tank

class Level:
    def __init__(self, level_number: int):
        pass

    def load_map(self, level_number: int):
        pass

    def update(self):
        pass

    def draw(self, screen):
        pass
    

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Batle city ramake")
clock = pygame.time.Clock()

current_level = Level(1)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False



clock.tick(FPS)
pygame.display.update()

current_level.update()
screen.fill((0, 0, 0))
current_level.draw(screen)

pygame.quit()
