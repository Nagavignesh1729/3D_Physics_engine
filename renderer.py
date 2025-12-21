import pygame
import math
from quaternions import Quaternion, DualQuaternion

class Renderer:
    def __init__(self, width, height, focal, distance):
        self.width = width
        self.height = height
        self.center = (width // 2, height // 2)
        self.focal = focal
        self.distance = distance
    
    def project(self, point_3d, camera):
        x = point_3d[0] - camera.position[0]
        y = point_3d[1] - camera.position[1]
        z = point_3d[2] - camera.position[2]
        
        # rotate by inverse camera orientation ( world turns around us... hihihi )
        rotated_rel = camera.orientation.inverse().rotate_vector((x, y, z))
        rx, ry, rz = rotated_rel
        
        dist_infront = -rz
        if dist_infront <= 10:
            dist_infront = 10
            
        factor = self.focal/(dist_infront)
        return (int(self.center[0] + rx*factor), int(self.center[1] - ry*factor))

    def draw_body(self, screen, body, camera):
        world_vertices = body.get_transformed_vertices()
        
        
        # if q = qr + k*qd then translation t = 2 * qd * qr.conjugate()
        t_quat = (body.dq.dual.scalar_mul(2)) * body.dq.real.conjugate()
        body_pos = (t_quat.x, t_quat.y, t_quat.z)
        
        def get_face_depth(face_indices):
            avg_x = sum(world_vertices[i][0] for i in face_indices) / len(face_indices)
            avg_y = sum(world_vertices[i][1] for i in face_indices) / len(face_indices)
            avg_z = sum(world_vertices[i][2] for i in face_indices) / len(face_indices)
        
            return (avg_x - camera.position[0])**2 + \
                   (avg_y - camera.position[1])**2 + \
                   (avg_z - camera.position[2])**2
        
        #painter's algorithm, sort faces relative to camera
        sorted_faces = sorted(
            body.mesh.faces, 
            key=lambda f: get_face_depth(f[0]),
            reverse=True
        )
        
        for face_indices, color in sorted_faces:
            #rel_z = sum((world_vertices[i][2] - camera.position[2]) for i in face_indices) / 4
            #if rel_z < 10:
            #   continue
        
            points_2d = [self.project(world_vertices[idx], camera) for idx in face_indices]
            #print(points_2d)
            pygame.draw.polygon(screen, color, points_2d)
    
    def draw_grid(self, screen, camera, step=100, size=300):
        """Draws a 3D coordinate grid."""
        # parallel to y
        for x in range(-size, size+1, step):
            for z in range(-size, size+1, step):
                if x == 0 and z == 0:
                    pygame.draw.line(screen, (100, 100, 100), self.project((x, -300, z), camera), self.project((x, 300, z), camera), 2)
                else:
                    pygame.draw.line(screen, (30, 30, 60), self.project((x, -300, z), camera), self.project((x, 300, z), camera))
        
        # parallel to x
        for y in range(-size, size+1, step):
            for z in range(-size, size+1, step):
                if y == 0 and z == 0:
                    pygame.draw.line(screen, (100, 100, 100), self.project((-300, y, z), camera), self.project((300, y, z), camera), 2)
                else:
                    pygame.draw.line(screen, (30, 30, 60), self.project((-300, y, z), camera), self.project((300, y, z), camera))
        
        # parallel to z
        for x in range(-size, size+1, step):
            for y in range(-size, size+1, step):
                if x == 0 and y == 0:
                    pygame.draw.line(screen, (100, 100, 100), self.project((x, y, -300), camera), self.project((x, y, 300), camera), 2)
                else:
                    pygame.draw.line(screen, (30, 30, 60), self.project((x, y, -300), camera), self.project((x, y, 300), camera))
    


class Camera:
    def __init__(self, position = [0, 0, 400]):
        self.position = position
        self.orientation = Quaternion(1, 0, 0, 0)
        self.yaw = 0 # looking left/right
        self.pitch = 0 # looking up/down
    
    def update_orientation(self, dx, dy):
        self.yaw -= dx * 0.02
        self.pitch -= dy * 0.02
        
        # clamping pitch to prevent backflipping
        self.pitch = max(-math.pi/2, min(math.pi/2, self.pitch))
        
        # left/right means axis of rotation is y
        # up/down means axis of rotation is x
        q_yaw = Quaternion.from_axis_angle([0, 1, 0], self.yaw)
        q_pitch = Quaternion.from_axis_angle([1, 0, 0], self.pitch)
        
        # yaw then pitch
        self.orientation = q_yaw * q_pitch