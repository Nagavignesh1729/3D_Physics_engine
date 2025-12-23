import math

class Complex:
    def __init__(self, real, imaginary):
        self.re = real
        self.im = imaginary
        self.r = self.magnitude()
        self.theta = math.atan(self.im/self.re)
        
    def __add__(self, other):
        return Complex(
            self.re + other.re,
            self.im + other.im
        )
    
    def __mul__(self, other):
        return Complex(
            self.re * other.re - self.im * other.im,
            self.re * other.im + self.im * other.re
        )
    
    def magnitude(self):
        return math.sqrt(self.re * self.re + self.im * self.im)

    def conjugate(self):
        return Complex(
            self.re,
            -self.im
        )