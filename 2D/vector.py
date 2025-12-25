import math

class Vector:
    def __init__(self, x_component, y_component):
        self.x = x_component
        self.y = y_component
        self.r = self.norm()
        self.theta = math.atan2(self.y, self.x)
        
    def __add__(self, other):
        return Vector(
            self.x + other.x,
            self.y + other.y
        )
        
    def __sub__(self, other):
        return Vector(
            self.x - other.x,
            self.y - other.y
        )
    
    # scalar multiplication
    def __mul__(self, other):
        return Vector(
            self.x * other,
            self.y * other
        )
    
    def __rmul__(self, other):
        return self.__mul__(other)
    
    def rotate_by(self, other):
        return Vector(
            self.x * other.x - self.y * other.y,
            self.x * other.y + self.y * other.x
        )
        
    '''
    def __mul__(self, other):
        return Complex(
            self.x * other.x - self.y * other.y,
            self.x * other.y + self.y * other.x
        )
    '''
    
    def norm(self):
        self.r = math.sqrt(self.x * self.x + self.y * self.y)
        return self.r

    '''
    def conjugate(self):
        return Complex(
            self.re,
            -self.im
        )
    '''
    
    def normalize(self):
        mag = self.norm()
        self.x /= mag
        self.y /= mag
        self.r = 1
        return self
    
    def unit_normal(self):
        return Vector(
            -self.x,
            self.y
        ).normalize()  