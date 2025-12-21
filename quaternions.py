import math

class Quaternion:
    def __init__(self, a0, a1, a2, a3):
        self.scalar = a0
        self.x = a1
        self.y = a2
        self.z = a3
        self.update_magnitude()
    
    def update_magnitude(self):
        self.magnitude = math.sqrt(self.scalar**2 + self.x**2 + self.y**2 + self.z**2)
        return self.magnitude
    
    def conjugate(self):
        return Quaternion(self.scalar, -self.x, -self.y, -self.z)
    
    def inverse(self):
        m = self.update_magnitude()
        ms = m * m
        return Quaternion(self.scalar/ms, -self.x/ms, -self.y/ms, -self.z/ms)
    
    def __add__(self, other):
        return Quaternion(
            self.scalar + other.scalar,
            self.x + other.x,
            self.y + other.y,
            self.z + other.z
        )

    def __mul__(self, other):
        w1, x1, y1, z1 = self.scalar, self.x, self.y, self.z
        w2, x2, y2, z2 = other.scalar, other.x, other.y, other.z

        return Quaternion(
            w1*w2 - x1*x2 - y1*y2 - z1*z2,
            w1*x2 + x1*w2 + y1*z2 - z1*y2,
            w1*y2 - x1*z2 + y1*w2 + z1*x2,
            w1*z2 + x1*y2 - y1*x2 + z1*w2
        )
    
    def normalize(self):
        m = self.update_magnitude()
        if m > 1e-8:
            self.scalar /= m
            self.x /= m
            self.y /= m
            self.z /= m
        self.magnitude = 1.0
        return self
        
    @staticmethod
    def from_axis_angle(axis, angle):
        ux, uy, uz = axis
        #print(ux, uy, uz)
        s = math.sin(angle / 2)
        return Quaternion(
            math.cos(angle / 2),
            ux * s,
            uy * s,
            uz * s
        )
    
    def dot(self, other):
        return (self.scalar * other.scalar + self.x * other.x + self.y * other.y + self.z * other.z)

    def rotate_vector(self, v):
        p = Quaternion(0, v[0], v[1], v[2])
        r = self * p * self.inverse()
        return (r.x, r.y, r.z)

    @staticmethod
    def slerp(q1, q2, t):
        dot = q1.dot(q2)
        
        if dot < 0:
            q1 = Quaternion(-q1.scalar, -q1.x, -q1.y, -q1.z)
            dot = -dot
        
        if dot > 0.9995:
            res = Quaternion(
                q1.scalar + t * (q2.scalar - q1.scalar),
                q1.x + t * (q2.x - q1.x),
                q1.y + t * (q2.y - q1.y),
                q1.z + t * (q2.z - q1.z)
            )
            return res.normalize()

        theta_0 = math.acos(dot)
        theta = theta_0 * t
        
        sin_theta_0 = math.sin(theta_0)
        sin_theta = math.sin(theta)
        
        s0 = math.cos(theta) - dot * sin_theta / sin_theta_0
        s1 = sin_theta / sin_theta_0

        return Quaternion(
            (q1.scalar * s0) + (q2.scalar * s1),
            (q1.x * s0) + (q2.x * s1),
            (q1.y * s0) + (q2.y * s1),
            (q1.z * s0) + (q2.z * s1)
        ).normalize()
    
    def scalar_mul(self, factor):
        return Quaternion(
            self.scalar * factor,
            self.x * factor,
            self.y * factor,
            self.z * factor
        )
        
        
    def __str__(self):
        return f"Quaternion is ({self._a0}, {self._a1}, {self._a2}, {self._a3}) with magnitude {self._magnitude}"

class DualQuaternion:
    def __init__(self, real: Quaternion, dual: Quaternion):
        self.real = real
        self.dual = dual
    
    def __add__(self, other):
        return DualQuaternion(
            real = self.real + other.real,
            dual = self.dual + other.dual
        )
    
    def __mul__(self, other):
        return DualQuaternion(
            real = self.real * other.real,
            dual = self.real*other.dual + self.dual*other.real
        )
    
    def conjugate(self):
        return DualQuaternion(
            real = self.real.conjugate(),
            dual = self.dual.conjugate().scalar_mul(-1)
        )
    
    @staticmethod
    def from_rotation(q_rot):
        return DualQuaternion(
            real = q_rot,
            dual = Quaternion(0, 0, 0, 0)
        )
    
    '''
    @staticmethod
    def from_translation(translation_vector):
        x, y, z = translation_vector
        qt = Quaternion(0, x/2, y/2, z/2)
        unit_q = Quaternion(1, 0, 0, 0)
        
        return DualQuaternion(
            real = unit_q,
            dual = qt
        )
    '''
    
    def combined_operator(self, q_trans, q_rot):
        return q_trans * q_rot

    def transform_point(self, v):
        p_real = Quaternion(1, 0, 0, 0)
        p_dual = Quaternion(0, v[0], v[1], v[2])
        p = DualQuaternion(p_real, p_dual)
        
        res = self * p * self.conjugate()
        
        return (res.dual.x, res.dual.y, res.dual.z)
    
    @staticmethod
    def sclerp(dq1, dq2, t):
        # slerp the rotation (real) parts
        real_interp = Quaternion.slerp(dq1.real, dq2.real, t)
        
        # Translation t = 2 * q_dual * q_real.conjugate()
        t1_quat = (dq1.dual.scalar_mul(2)) * dq1.real.conjugate()
        t2_quat = (dq2.dual.scalar_mul(2)) * dq2.real.conjugate()
        
        tx = t1_quat.x + t * (t2_quat.x - t1_quat.x)
        ty = t1_quat.y + t * (t2_quat.y - t1_quat.y)
        tz = t1_quat.z + t * (t2_quat.z - t1_quat.z)
        
        trans_quat = Quaternion(0, tx/2, ty/2, tz/2)
        
        dual_interp = trans_quat * real_interp
        return DualQuaternion(real_interp, dual_interp)
    