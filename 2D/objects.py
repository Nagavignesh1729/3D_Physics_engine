import pygame
from complexMaths import Complex
import math

class Body:    
    def __init__(self, position, orientation, shape):
        self.position = position
        self.orientation = orientation
        self.shape = shape
        
    def update(self, position=None, orientation=None, shape=None):
        self.position = position if position is not None else self.position
        self.orientation = orientation if orientation is not None else self.orientation
        self.shape = shape if shape is not None else self.shape
    
    def draw(self, screen):
        vertices = self.shape.get_vertices()
        res = []
        theta = (self.orientation * math.pi / 180)
        rotate_complex = Complex(math.cos(theta), math.sin(theta)).normalize()
        
        for i in range(len(vertices)):
            x, y = (vertices[i][0], vertices[i][1])
            point = Complex(x, y)
            new_point = rotate_complex * point
            res.append((self.position[0] + new_point.re, self.position[1] + new_point.im))
            
        pygame.draw.polygon(screen, self.shape.color, res)

class Shape:
    def __init__(self, vertices=None, color=(255, 255, 255)):
        self.vertices = vertices
        self.color = color
        
    def get_vertices(self):
        return self.vertices
    
    def square(self, r):
        self.vertices = [(-r, -r), (-r, +r), (+r, +r), (+r, -r)]        