import math
import sys
import pygame
from objects import Shape, Body, ShapeMaker
from myworld import MyWorld
from vector import Vector

pygame.init()

WIDTH, HEIGHT = 800, 600
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 255)
PURPLE = (255, 0, 255)
YELLOW = (255, 255, 0)

subjects = []
pallete = [WHITE, BLUE, RED, GREEN, PURPLE, YELLOW]

subjects.append(
    Body(
        position = Vector(WIDTH//2 + 50, HEIGHT//2 - 50),
        orientation = 45,
        shape = ShapeMaker.make_square(80, pallete[2]),
        velocity = Vector(150, -75),
        rotation_speed = 20
    )
)

subjects.append(
    Body(
        position = Vector(WIDTH//2 - 50, HEIGHT//2 + 50),
        orientation = 0,
        shape = ShapeMaker.make_square(80, pallete[2]),
        velocity = Vector(-100, -175),
        rotation_speed = 35
    )
)

universe = MyWorld((WIDTH, HEIGHT), subjects, axes=True)

running = True
while running:
    dt = clock.tick(60) / 1000
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    universe.update(dt)
    universe.draw()

    pygame.display.flip()

pygame.quit()
sys.exit()