import pygame
pygame.init()

screen = pygame.display.set_mode((800, 600))

clock = pygame.time.Clock()
alpha = 255
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break
    screen.fill((0, 0, 0))

    test_surface = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    pygame.draw.rect(test_surface, (255, 0, 0, 255), pygame.Rect(300, 200, 200, 200))
    test_surface.set_alpha(alpha)
    screen.blit(test_surface, (0, 0))
    pygame.display.flip()

    alpha -= 0.1