import pygame

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
    
    # SAT (Seperating Axis Theorem) for collision detection. Works only for convex polygons.
    # Algorithm : 
    #   1) For every edge on Body 1, project the vertices of Body 1 and Body 2 to its normal
    #   2) If overlaps are found, continue
    #   3) If for some edge, there is no overlap of the projected vertices, 
    #           then there exists a line seperating the bodies. (The line is perpendicular to this projected line)
    
    # takes 2 bodies and spits out a number (the distance bewtween them)
    # positive = no collision, negative = collision
    def SAT_collision_dectection(self, body1, body2):
        verts = body1.world_vertices
        n = len(verts)
        edges = [Vector(verts[i][0], verts[i][1]) - Vector(verts[i-1][0], verts[i-1][1]) for i in range(1, n)]
        edges.append(Vector(verts[n-1][0], verts[n-1][1]) - Vector(verts[0][0], verts[0][1]))
        
        verts2 = body2.world_vertices
        
        for edge in edges:
            normal = edges.unit_normal()
            for v in verts2:
                