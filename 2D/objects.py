import pygame
from vector import Vector
import math

class Body:    
    def __init__(self, position, orientation, shape, velocity, rotation_speed):
        self.position = position
        self.orientation = orientation
        self.shape = shape
        self.velocity = velocity
        self.rotation_speed = rotation_speed
        self.bounds = self.set_local_boundary()
        
    def update(self, dt):
        self.position += self.velocity * dt
        self.orientation += self.rotation_speed * dt
        #self.shape = shape if shape is not None else self.shape
    
    def draw(self, screen):
        vertices = self.shape.get_vertices()
        res = []
        theta = (self.orientation * math.pi / 180)
        rotate_vector = Vector(math.cos(theta), math.sin(theta))
        
        for v in vertices:
            point = Vector(v[0], v[1])
            new_point = point.rotate_by(rotate_vector)
            res.append((self.position.x + new_point.x, self.position.y + new_point.y))
            
        pygame.draw.polygon(screen, self.shape.color, res)

    def set_local_boundary(self):
        verts = self.shape.get_vertices()
        min_x = min(v[0] for v in verts)
        max_x = max(v[0] for v in verts)
        min_y = min(v[1] for v in verts)
        max_y = max(v[1] for v in verts)
        
        return (min_x, max_x, min_y, max_y)
    
class Shape:
    def __init__(self, vertices=None, color = (255, 255, 255)):
        self.vertices = vertices
        self.color = color
        
    def get_vertices(self):
        return self.vertices

    
class ShapeMaker:
    @staticmethod
    def make_square(length, color):
        return ShapeMaker.helper_make_regular_polygon(
            4, 
            length/math.sqrt(2), 
            math.pi/4,
            color
        )
    
    @staticmethod
    def make_triangle(length, color):
        return ShapeMaker.helper_make_regular_polygon(
            3, 
            length/(2*math.sin(math.pi/3)), 
            -math.pi/2,
            color
        )
    
    @staticmethod
    def make_regular_polygon(nsides, length, offset=0, color=(255, 255, 255)):
        return ShapeMaker.helper_make_regular_polygon(
            nsides,
            length/(2*math.sin(math.pi/nsides)),
            offset,
            color                  
        )
        
    @staticmethod
    def helper_make_regular_polygon(nverts, r, offset, color):
        verts = []
        theta = offset
        angle = math.pi * 2 / nverts 
        for i in range(nverts):
            verts.append((r * math.cos(theta), r * math.sin(theta)))
            theta += angle
        
        return Shape(
            vertices = verts,
            color = color
        )