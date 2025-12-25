import pygame
from vector import Vector
class MyWorld:
    def __init__(self, dimension, bodies, axes=False):
        self.WIDTH, self.HEIGHT = dimension
        self.center = (self.WIDTH // 2, self.HEIGHT // 2)
        self.bodies = bodies
        self.screen = pygame.display.set_mode(dimension)
        self.axes = axes
    
    def draw(self):
        self.screen.fill((0, 0, 0))
        if self.axes:
            pygame.draw.line(self.screen, (100, 100, 100), (0, self.HEIGHT//2), (self.WIDTH, self.HEIGHT//2))
            pygame.draw.line(self.screen, (100, 100, 100), (self.WIDTH//2, 0), (self.WIDTH//2, self.HEIGHT))
        
        for body in self.bodies:
            body.draw(self.screen)
            
    def update(self, dt):
        for body in self.bodies:
            body.update(dt)
            body.get_world_space_vertices()
                        
            lx_min, lx_max, ly_min, ly_max = body.bounds # local box
            
            if body.position.x + lx_min < 0:
                body.velocity.x *= -1
                body.position.x = -lx_min
            elif body.position.x + lx_max > self.WIDTH:
                body.velocity.x *= -1
                body.position.x = self.WIDTH - lx_max
            
            if body.position.y + ly_min < 0:
                body.velocity.y *= -1
                body.position.y = -ly_min
            elif body.position.y + ly_max > self.HEIGHT:
                body.velocity.y *= -1
                body.position.y = self.HEIGHT - ly_max
        
        print(self.SAT_collision_dectection(self.bodies[0], self.bodies[1]))
    
    # SAT (Seperating Axis Theorem) for collision detection. Works only for convex polygons.
    # Algorithm : 
    #   1) For every edge on Body 1, project the vertices of Body 1 and Body 2 to its normal
    #   2) If overlaps are found, continue
    #   3) If for some edge, there is no overlap of the projected vertices, 
    #           then there exists a line seperating the bodies. (The line is perpendicular to this projected line)
    
    # takes 2 bodies and spits out a number (the distance between them)
    # positive = no collision, negative = collision
    def SAT_collision_dectection(self, body1, body2):
        verts1 = body1.world_vertices
        n = len(verts1)
        edges = [Vector(verts1[i][0], verts1[i][1]) - Vector(verts1[i-1][0], verts1[i-1][1]) for i in range(1, n)]
        edges.append(Vector(verts1[n-1][0], verts1[n-1][1]) - Vector(verts1[0][0], verts1[0][1]))
        
        verts2 = body2.world_vertices
        
        m = float('inf')
        
        for edge in edges:
            proj1, proj2 = [], []
            normal = edge.unit_normal()
            for v in verts1:
                temp = Vector(v[0], v[1])
                proj1.append(temp.dot(normal))
            for v in verts2:
                temp = Vector(v[0], v[1])
                proj2.append(temp.dot(normal))
            
            min1, max1 = min(proj1), max(proj1)
            min2, max2 = min(proj2), max(proj2)
            
            if max1 < min2 or max2 < min1:
                return 1
        
        return -1