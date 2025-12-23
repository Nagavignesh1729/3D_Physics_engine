import math
import sys
import pygame
from objects import Shape, Body

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

origin = (WIDTH // 2, HEIGHT // 2)

def axes(screen):
    pygame.draw.line(screen, WHITE, (0, origin[1]), (WIDTH, origin[1]))
    pygame.draw.line(screen, WHITE, (origin[0], 0), (origin[0], HEIGHT))

sq = Shape(color = BLUE)
sq.square(40)

test = Body((origin[0] + 100, origin[1] - 100), 0, sq)

running = True
while running:
    dt = clock.tick(60) / 1000
    
    #screen.fill((0, 0, 0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    axes(screen)
    test.draw(screen)
    
    pygame.display.flip()

pygame.quit()
sys.exit()