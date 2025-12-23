import math

class Complex:
    def __init__(self, real, imaginary):
        self.re = real
        self.im = imaginary
        self.r = self.magnitude()
        self.theta = math.atan2(self.im/self.re)
        
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
        self.r = math.sqrt(self.re * self.re + self.im * self.im)
        return self.r

    def conjugate(self):
        return Complex(
            self.re,
            -self.im
        )
    
    def normalize(self):
        mag = self.magnitude()
        self.re /= mag
        self.im /= mag
        self.r = 1
        return self        