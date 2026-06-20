import math
import pygame



# ease-In

def easeInExpo(t):
    if t == 0:
        return 0
    return math.pow(2, 10 * (t - 1))
def easeInQuint(t):
    if t == 0:
        return 0
    return t**5
def easeInQuart(t):
    if t == 0:
        return 0
    return t**4
def easeInCubic(t):
    if t == 0:
        return 0
    return t**3
def easeInQuad(t):
    if t == 0:
        return 0
    return t**2

def decelerate(t):
    if t == 0:
        return 0
    return 1 - (1 - t)**2

# ease-Out

def easeOutExpo(t):
    if t == 0:
        return 0
    return 1-math.pow(2, -10*t)
def easeOutQuint(t):
    if t == 0:
        return 0
    return 1-math.pow((1-t), 5)
def easeOutQuart(t):
    if t == 0:
        return 0
    return 1-math.pow((1-t), 4)
def easeOutCubic(t):
    if t == 0:
        return 0
    return 1-math.pow((1-t), 3)
def easeOutQuad(t):
    if t == 0:
        return 0
    return 1-math.pow((1-t), 2)

# ease-In-Out

def easeInOutExpo(t):
    if t == 0:
        return 0
    if t < 0.5:
        return (2 ** (10 * (2 * t - 1))) / 2
    else:
        return 1 - (2 ** (-10 * (2 * t - 1))) / 2
def easeInOutQuint(t):
    if t == 0:
        return 0
    elif t < 0.5:
        return 16 * t ** 5
    else:
        return 1 - ((-2 * t + 2) ** 5) / 2
def easeInOutQuart(t):
    if t == 0:
        return 0
    elif t < 0.5:
        return 8 * t ** 4
    else:
        return 1 - ((-2 * t + 2) ** 4) / 2
def easeInOutCubic(t):
    if t == 0:
        return 0
    elif t < 0.5:
        return 4 * t ** 3
    else:
        return 1 - ((-2 * t + 2) ** 3) / 2
def easeInOutQuad(t):
    if t == 0:
        return 0
    elif t < 0.5:
        return 2 * t ** 2
    else:
        return 1 - ((-2 * t + 2) ** 2) / 2

# bounce

def bounceOut(t):
    if t < 1/2.75:
        return 7.5625 * t * t
    elif t < 2/2.75:
        t -= 1.5/2.75
        return 7.5625 * t * t + 0.75
    elif t < 2.5/2.75:
        t -= 2.25/2.75
        return 7.5625 * t * t + 0.9375
    else:
        t -= 2.625/2.75
        return 7.5625 * t * t + 0.984375

def bounceIn(t):
    return 1 - bounceOut(1 - t)

def bounceInOut(t):
    if t < 0.5:
        return 0.5 * bounceIn(t * 2)
    else:
        return 0.5 * bounceOut(t * 2 - 1) + 0.5

#elastic

def elasticIn(t):
    if t == 0 or t == 1:
        return t
    p = 0.3
    s = p / 4
    return -math.pow(2, 10 * (t - 1)) * math.sin((t - 1 - s) * (2 * math.pi) / p)

def elasticOut(t):
    if t == 0 or t == 1:
        return t
    p = 0.3
    s = p / 4
    return math.pow(2, -10 * t) * math.sin((t - s) * (2 * math.pi) / p) + 1

def elasticInOut(t):
    if t == 0 or t == 1:
        return t
    p = 0.45
    s = p / 4
    if t < 0.5:
        return -0.5 * math.pow(2, 10 * (2 * t - 1)) * math.sin((2 * t - 1 - s) * (2 * math.pi) / p)
    else:
        return math.pow(2, -10 * (2 * t - 1)) * math.sin((2 * t - 1 - s) * (2 * math.pi) / p) * 0.5 + 1

def linear(t):
    return t

if __name__ == "__main__":
    pygame.init()
    WIDTH, HEIGHT = 600, 400
    screen = pygame.display.set_mode((WIDTH, 600))
    clock = pygame.time.Clock()

    start = 0
    end = 100
    frames = 60


    values = []
    for frame in range(frames + 1):
        t = frame / frames
        eased = bounceIn(t)
        value = start + (end - start) * eased
        values.append(value)

    values2 = []
    for frame in range(frames + 1):
        t = frame / frames
        eased = bounceOut(t)
        value = start + (end - start) * eased
        values2.append(value)



    # Масштабування для екрану
    def scale_y(value):
        return HEIGHT - (value / end * HEIGHT)  # щоб графік йшов знизу вгору


    # Основний цикл
    running = True
    while running:
        screen.fill((30, 30, 30))

        # Малюємо графік
        for i in range(1, len(values)):
            pygame.draw.line(
                screen,
                (255, 0, 0),
                ((i-1)*7, scale_y(values[i-1])+150),
                (i*7, scale_y(values[i])+150),
                2
            )
        for i in range(1, len(values2)):
            pygame.draw.line(
                screen,
                (0, 255, 0),
                ((i-1)*7, scale_y(values2[i-1])+150),
                (i*7, scale_y(values2[i])+150),
                2
            )

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        clock.tick(60)

    pygame.quit()