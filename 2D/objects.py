import pygame
from complexMaths import Complex

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
        for i in range(len(vertices)):
            res.append((self.position[0] + vertices[i][0], self.position[1] + vertices[i][1]))
        pygame.draw.polygon(screen, self.shape.color, res)

class Shape:
    def __init__(self, vertices=None, color=(255, 255, 255)):
        self.vertices = vertices
        self.color = color
        
    def get_vertices(self):
        return self.vertices
    
    def square(self, r):
        self.vertices = [(-r, -r), (-r, +r), (+r, +r), (+r, -r)]