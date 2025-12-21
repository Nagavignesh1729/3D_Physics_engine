import math
from quaternions import Quaternion, DualQuaternion
import random

class Mesh:
    # stores vertices and face data
    def __init__(self, vertices=None, faces=None):
        self.vertices = vertices or []
        self.faces = faces or []
    
    @classmethod
    def make_sphere(cls, radius, detail = 16, color=None):
        verts = []
        faces = []
        
        grid = []
        for i in range(detail + 1):
            row = []
            phi = math.pi * i / detail
            for j in range(detail + 1):
                theta = 2 * math.pi * j / detail
                x = radius * math.sin(phi) * math.cos(theta)
                y = radius * math.cos(phi)
                z = radius * math.sin(phi) * math.sin(theta)
                row.append(len(verts)) # storing index
                verts.append((x, y, z))
            grid.append(row)
        
        for i in range(detail):
            for j in range(detail):
                p1 = grid[i][j]
                p2 = grid[i][j+1]
                p3 = grid[i+1][j+1]
                p4 = grid[i+1][j]
                
                if color is None:
                    color = (random.randint(50, 200), 100, 255)
                faces.append(((p1, p2, p3, p4), color))
        
        return cls(verts, faces)


class RigidBody:
    def __init__(self, mesh, position=(0, 0, 0), orientation=None):
        self.mesh = mesh
        if orientation is None:
            orientation = Quaternion(1, 0, 0, 0)
        self.set_pose(position, orientation)
        self.linear_velocity = [0, 0, 0]
        self.angular_velocity = [0, 0, 0]
        
    def set_pose(self, position, orientation):
        q = orientation.normalize()
        tx, ty, tz = position

        self.dq = DualQuaternion(
            real=q,
            dual=Quaternion(0, tx/2, ty/2, tz/2) * q
        )

    def get_position(self):
        t_quat = (self.dq.dual.scalar_mul(2)) * self.dq.real.conjugate()
        return (t_quat.x, t_quat.y, t_quat.z)

    def get_transformed_vertices(self):
        return [self.dq.transform_point(v) for v in self.mesh.vertices]

    def integrate(self, dt):
        px, py, pz = self.get_position()
        vx, vy, vz = self.linear_velocity
        new_pos = (
            px + vx * dt,
            py + vy * dt,
            pz + vz * dt
        )
        
        # angular vlocity
        wx, wy, wz = self.angular_velocity
        omega_mag = math.sqrt(wx*wx + wy*wy + wz*wz)
        
        if omega_mag > 1e-8:
            axis = (wx/omega_mag, wy/omega_mag, wz/omega_mag)
            angle = omega_mag * dt
            dq = Quaternion.from_axis_angle(axis, angle)
            new_ori = dq * self.dq.real
        else:
            new_ori = self.dq.real
        
        self.set_pose(new_pos, new_ori)

CUBE_VERTICES = [
    (-50, -50, -50), (50, -50, -50), (50, -50, 50), (-50, -50, 50),
    (-50,  50, -50), (50,  50, -50), (50,  50, 50), (-50,  50, 50)
]

CUBE_FACES = [
    ((0, 1, 2, 3), (0, 255, 0)),   # Bottom
    ((4, 5, 6, 7), (255, 0, 0)),   # Top
    ((3, 2, 6, 7), (0, 0, 255)),   # Front
    ((0, 1, 5, 4), (255, 255, 255)),# Back
    ((0, 3, 7, 4), (255, 255, 0)),  # Left
    ((1, 2, 6, 5), (255, 0, 255))  # Right
]