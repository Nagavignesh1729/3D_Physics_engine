import pygame

class MyWorld:
    def __init__(self, dimension, bodies, axes=False):
        self.WIDTH, self.HEIGHT = dimension
        self.center = (self.WIDTH // 2, self.HEIGHT // 2)
        self.bodies = bodies
        
        for body in self.bodies:
            body.set_position_at_center(self.center)
        
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
            
            lx_min, lx_max, ly_min, ly_max = body.bounds # local box
            
            if body.position.x + lx_min < 0:
                body.velocity.x *= -1
                body.position.x = -lx_min
            elif body.position.x + lx_max > self.WIDTH:
                body.velocity.x *= -1
                body.position.x = -lx_max
            
            if body.position.y + ly_min < 0:
                body.velocity.y *= -1
                body.position.y = -ly_min
            elif body.position.y + ly_max > self.WIDTH:
                body.velocity.y *= -1
                body.position.y = -ly_max