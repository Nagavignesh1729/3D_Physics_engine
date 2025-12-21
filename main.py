import pygame
import sys
import math

from quaternions import Quaternion, DualQuaternion
from geometry import Mesh, RigidBody, CUBE_VERTICES, CUBE_FACES
from renderer import Renderer, Camera

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

cube_mesh = Mesh(CUBE_VERTICES, CUBE_FACES)
cube = RigidBody(cube_mesh, (0, 0, 0), Quaternion(1, 0, 0, 0))

view = Renderer(WIDTH, HEIGHT, focal=500, distance=800)
camera = Camera()

start_pos = [-250, -150, -100]
end_pos   = [ 250,  150, -200]

total_spins = 3

trail_3d = []
colors = [
    (255, 50, 50), (50, 255, 50), (50, 50, 255), (255, 255, 50),
    (255, 50, 255), (50, 255, 255), (255, 255, 255), (150, 150, 150)
]

pygame.event.set_grab(True)
running = True

cube.linear_velocity = [50, 20, 40]
cube.angular_velocity = [1, 1, 0]

while running:
    dt = clock.tick(60) / 1000
    
    screen.fill((10, 10, 15))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

    dx, dy = pygame.mouse.get_rel()
    camera.update_orientation(dx, dy)

    forward = camera.orientation.rotate_vector((0, 0, -1))
    right = camera.orientation.rotate_vector((1, 0, 0))

    keys = pygame.key.get_pressed()
    speed = 5
    if keys[pygame.K_w]:
        camera.position = [camera.position[i] + forward[i] * speed for i in range(3)]
    if keys[pygame.K_s]:
        camera.position = [camera.position[i] - forward[i] * speed for i in range(3)]
    if keys[pygame.K_a]:
        camera.position = [camera.position[i] - right[i] * speed for i in range(3)]
    if keys[pygame.K_d]:
        camera.position = [camera.position[i] + right[i] * speed for i in range(3)]


    #cube.set_pose(curr_pos, q_spin)
    cube.integrate(dt)

    t_quat = (cube.dq.dual.scalar_mul(2)) * cube.dq.real.conjugate()
    center = (t_quat.x, t_quat.y, t_quat.z)
    
    if not (-300 < center[0] < 300):
        cube.linear_velocity[0] *= -1
    if not (-300 < center[1] < 300):
        cube.linear_velocity[1] *= -1
    if not (-300 < center[2] < 300):
        cube.linear_velocity[2] *= -1

    
    trail_3d.append((center, (255, 0, 0)))

    verts = cube.get_transformed_vertices()
    for i, v in enumerate(verts):
        trail_3d.append((v, colors[i]))

    if len(trail_3d) > 18 * 120:
        trail_3d = trail_3d[9:]

    for p, c in trail_3d:
        sp = view.project(p, camera)
        if 0 <= sp[0] < WIDTH and 0 <= sp[1] < HEIGHT:
            pygame.draw.circle(screen, c, sp, 1)

    view.draw_grid(screen, camera)
    view.draw_body(screen, cube, camera)

    pygame.display.flip()

pygame.quit()
sys.exit()
