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

reg = ShapeMaker.make_square(80, BLUE)
subject1 = Body(
    position = Vector(WIDTH//2, HEIGHT//2),
    orientation = 0,
    shape = reg,
    velocity = Vector(150, -100),
    rotation_speed = 90
)

subjects = []
pallete = [WHITE, BLUE, RED, GREEN, PURPLE, YELLOW]
for i in range(6):
    subjects.append(
        Body(
            position = Vector(WIDTH//2 + i*30, HEIGHT//2 - i*30),
            orientation = 25 * i,
            shape = ShapeMaker.make_square(20*i, pallete[i]),
            velocity = Vector(10 * i, - 20 * i),
            rotation_speed = 20 * i
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