import pygame
import animation_pygame as an
from parAnimation import *

pygame.init()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

event_open_shop = pygame.event.custom_type()


test_surface = pygame.Surface((100, 100), pygame.SRCALPHA)
test_surface.fill((0,0,0, 255))
animator = an.Animator(60)
anim = animator.create_animation(test_surface, "test1", 20,
                                 par_positions=[Position(0,5, "linear", pygame.Vector2(0,250), pygame.Vector2(700,250)), Position(7,12, "linear", pygame.Vector2(700,250), pygame.Vector2(0,0)), ],
                                 par_rotations=[Rotation(0, 20, "linear", 0, 2000)],
                                 par_scales=[Scale(5, 7, "linear", 2) ],
                                 par_transparencys=[Transparency(0,5, "linear", 0, 70), Transparency(5,7, "linear", 70, 100), Transparency(7,12, "linear", 100, 20), ])
print(anim)
animator.start_animation("test1")
color = (0,255,255)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    screen.fill(color)
    animator.play_animations(screen)
    pygame.display.flip()
    clock.tick(60)