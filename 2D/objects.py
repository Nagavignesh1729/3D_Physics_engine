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
    def __init__(self, vertices=None, color = (255, 255, 255)):
        self.vertices = vertices
        self.color = color
        
    def get_vertices(self):
        return self.vertices

    
class ShapeMaker:
    @staticmethod
    def make_square(length):
        return ShapeMaker.helper_make_regular_polygon(
            4, 
            length/math.sqrt(2), 
            math.pi/4
        )
    
    @staticmethod
    def make_triangle(length):
        return ShapeMaker.helper_make_regular_polygon(
            3, 
            length/(2*math.sin(math.pi/3)), 
            -math.pi/2
        )
    
    @staticmethod
    def make_regular_polygon(nsides, length, offset = 0):
        return ShapeMaker.helper_make_regular_polygon(
            nsides,
            length/(2*math.sin(math.pi/nsides)),
            0                       
        )
        
    @staticmethod
    def helper_make_regular_polygon(nverts, r, offset):
        verts = []
        theta = offset
        angle = math.pi * 2 / nverts 
        for i in range(nverts):
            verts.append((r * math.cos(theta), r * math.sin(theta)))
            theta += angle
        
        return Shape(
            vertices = verts
        )