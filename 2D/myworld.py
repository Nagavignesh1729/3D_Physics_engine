class MyWorld:
    def __init__(self, screen, bodies):
        self.screen = screen
        self.bodies = bodies
    
    def update(self, dt):
        for body in self.bodies:
            body.update(dt)
            body.draw(self.screen)