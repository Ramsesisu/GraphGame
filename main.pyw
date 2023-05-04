# made by https://github.com/Ramsesisu

import random
# noinspection PyUnresolvedReferences
from math import *

import pygame

pygame.init()

width = 800
height = 600

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)
GREEN = (34, 139, 34)
LIGHT_GREEN = (144, 238, 144)
RED = (255, 0, 0)
DARK_RED = (139, 0, 0)
BLUE = (0, 0, 255)
GOLD = (218, 165, 32)

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("GraphGame")

title = pygame.font.SysFont(None, 36)
numbers = pygame.font.SysFont(None, 22)
info = pygame.font.SysFont(None, 100)

clock = pygame.time.Clock()
clock.tick(60)

active = True
start = True
solution = False
waiting = False
levelup = False

func = ""
cursor = 0

level = 1

increment_x = 12
increment_y = 12

target_x = 0
target_y = 0

obstacles = []

while active:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            active = False
        elif event.type == pygame.VIDEORESIZE:
            width = screen.get_width()
            height = screen.get_height()
            screen = pygame.display.set_mode((width, height))
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or start or levelup:
                if event.key == pygame.K_ESCAPE:
                    level -= 1
                    if level == 0:
                        level = 1

                while True:
                    increment_x = random.randrange(4, 40, 2)
                    if width % increment_x == 0:
                        break
                while True:
                    increment_y = random.randrange(4, 30, 2)
                    if height % increment_y == 0:
                        break

                target_x = random.randint((-increment_x + 2) // 2 + 1, increment_x // 2 - 1)
                target_y = random.randint(-increment_y // 2 + 1, increment_y // 2 - 1)

                obstacles = []
                amount = level
                for o in range(amount):
                    rand_w = random.randint(0, width)
                    rand_h = random.randint(0, height)

                    target_w = target_x * width / increment_x + width / 2
                    target_h = -target_y * height / increment_y + height / 2
                    distance = sqrt((rand_w - target_w) ** 2 + (rand_h - target_h) ** 2)
                    lenght = len(obstacles)
                    if lenght == 0:
                        lenght = 1
                    if lenght > 20:
                        lenght = 20
                    if distance > int(width / (2 * lenght) + width / 20):
                        obstacles.append([rand_w, rand_h])

                levelup = False
            elif event.key == pygame.K_BACKSPACE:
                func = func[0:cursor - 1] + func[cursor:]
                if len(func) == 0:
                    cursor = 1
                cursor -= 1
            elif event.key == pygame.K_LEFT:
                if cursor == 0:
                    cursor = 1
                cursor -= 1
            elif event.key == pygame.K_RIGHT:
                if cursor == len(func):
                    cursor = len(func) - 1
                cursor += 1
            elif event.key == pygame.K_RETURN:
                if solution:
                    solution = False
                    continue
                if not start:
                    solution = True
                    continue
            else:
                if not waiting:
                    func = func.replace("**", "^")
                    len_old = len(func)
                    len_part = len(func[0:cursor])
                    if len_part > 0:
                        if func[0:cursor][len_part - 1] == "^" and event.unicode == "^":
                            event.unicode = "2"
                    func = func[0:cursor] + event.unicode + func[cursor:]
                    if not len(func) == len_old:
                        cursor += 1
            if start:
                func = ""
                start = False
            solution = False
            if waiting:
                waiting = False

    if waiting:
        continue

    if solution:
        incre = width / increment_x

        w_last = None
        h_last = None

        win = False
        crashed = False
        for w in range(int(width)):
            try:
                x = (w % (increment_x * incre) - (increment_x * incre - 2) / 2) / incre
                i = len(func)
                for c in range(i):
                    i -= 1
                    if i > 0:
                        if func[i] == "x" and func[i - 1] == "x":
                            func = func[0:i] + "*" + func[i:]
                        if func[i].isalpha() or func[i] == "(":
                            if func[i - 1].isnumeric():
                                func = func[0:i] + "*" + func[i:]
                        if func[i] == "(":
                            if func[i - 1] == "x":
                                func = func[0:i] + "*" + func[i:]
                    if i < len(func) - 1:
                        if func[i].isalpha() or func[i] == ")":
                            if func[i + 1].isnumeric():
                                func = func[0:i + 1] + "*" + func[i + 1:]
                        if func[i] == ")":
                            if func[i + 1] == "x":
                                func = func[0:i + 1] + "*" + func[i + 1:]
                y = eval(func.replace("^", "**").replace("ln(", "log("))

                w = x * width / increment_x + width / 2
                h = -y * height / increment_y + height / 2

                if w_last is not None:
                    if w > w_last:
                        if not crashed:
                            pygame.draw.line(screen, GREEN, [w_last, h_last], [w, h], 3)

                w_last = w
                h_last = h

                screen.blit(title.render(f" f(x) = {func}   ", True, BLACK, LIGHT_GREEN), (10, 10))

                target_w = target_x * width / increment_x + width / 2
                target_h = -target_y * height / increment_y + height / 2
                distance = sqrt((w - target_w) ** 2 + (h - target_h) ** 2)
                if distance < int(height / 20):
                    if not win:
                        if not crashed:
                            pygame.draw.circle(screen, GOLD, [w, h], 8, 8)

                        win = True

                for o in obstacles:
                    distance = sqrt((w - o[0]) ** 2 + (h - o[1]) ** 2)
                    lenght = len(obstacles)
                    if lenght == 0:
                        lenght = 1
                    if lenght > 20:
                        lenght = 20
                    if distance < int(width / (2 * lenght)):
                        if not crashed:
                            pygame.draw.circle(screen, GOLD, [w, h], 8, 8)
                        crashed = True

                if w >= width:
                    if not 0 <= h <= height:
                        font = info.render("Failed!", True, DARK_RED)
                        screen.blit(font, ((width - font.get_width()) / 2, (height - font.get_height()) / 2))

                        pygame.display.flip()

                        level -= 1
                        if level == 0:
                            level = 1

                        waiting = True
                        levelup = False
                    elif crashed:
                        font = info.render("Crashed!", True, DARK_RED)
                        screen.blit(font, ((width - font.get_width()) / 2, (height - font.get_height()) / 2))

                        pygame.display.flip()

                        level -= 1
                        if level == 0:
                            level = 1

                        waiting = True
                        levelup = False
                    elif win:
                        font = info.render("Level-Up!", True, GOLD)
                        screen.blit(font, ((width - font.get_width()) / 2, (height - font.get_height()) / 2))
                        pygame.draw.circle(screen, GOLD, [w, h], 8, 8)

                        level += 1
                        func = ""
                        cursor = len(func)

                        waiting = True
                        levelup = True
                    else:
                        font = info.render("Missed!", True, DARK_RED)
                        screen.blit(font, ((width - font.get_width()) / 2, (height - font.get_height()) / 2))

                        pygame.display.flip()

                        level -= 1
                        if level == 0:
                            level = 1

                        waiting = True
                        levelup = False

                    pygame.display.flip()

                    cursor = len(func)
                    break
            except:
                w_last = None
        continue

    if start:
        screen.fill(LIGHT_GREEN)
        screen.blit(title.render("GraphGame", True, DARK_GRAY), (width / 2 - 60, height / 2 - 40))

        pygame.display.flip()
        continue

    screen.fill(WHITE)

    pygame.draw.line(screen, BLACK, (0, height / 2), (width, height / 2), 2)
    max_x = int(increment_x) - 1
    step = 1
    if max_x < 10:
        step = 2
        max_x += 1
    if max_x < 6:
        step = 4
        max_x += 1
    index = 0
    label = int(increment_x / 2 * -1) + 1 / step
    for i in range(max_x * step):
        index += int((width / increment_x) / step)
        if label != 0:
            pygame.draw.line(screen, GRAY, (index, 0), (index, height), 1)
            pygame.draw.line(screen, BLACK, (index, height / 2 - 5), (index, height / 2 + 5), 2)
            screen.blit(numbers.render(str(label).replace(".0", ""), True, BLACK), (index, height / 2 + 10))
        label += 1 / step
    pygame.draw.polygon(screen, BLACK,
                        [(width - 15, height / 2 + 7), (width - 15, height / 2 - 7), (width - 5, height / 2)])

    pygame.draw.line(screen, BLACK, (width / 2, 0), (width / 2, height), 2)
    max_y = int(increment_y) - 1
    step = 1
    if max_y < 10:
        step = 2
        max_y += 1
    if max_y < 6:
        step = 4
        max_y += 1
    index = 0
    label = int(increment_y / 2 * -1) + 1 / step
    for i in range(max_y * step):
        index += int((height / increment_y) / step)
        if label != 0:
            pygame.draw.line(screen, GRAY, (0, index), (width, index), 1)
            pygame.draw.line(screen, BLACK, (width / 2 - 5, index), (width / 2 + 5, index), 2)
            screen.blit(numbers.render(str(-label).replace(".0", ""), True, BLACK), (width / 2 + 10, index))
        label += 1 / step
    pygame.draw.polygon(screen, BLACK, [(width / 2 + 7, 10), (width / 2 - 7, 10), (width / 2, 0)])

    for o in obstacles:
        lenght = len(obstacles)
        if lenght == 0:
            lenght = 1
        if lenght > 20:
            lenght = 20
        pygame.draw.circle(screen, DARK_GRAY, o, int(width / (2 * lenght)), int(width / (2 * lenght)))
        pygame.draw.circle(screen, RED, o, int(width / (2 * lenght)), int(width / (20 * lenght)))

    target_w = target_x * width / increment_x + width / 2
    target_h = -target_y * height / increment_y + height / 2
    pygame.draw.circle(screen, BLUE, [target_w, target_h], int(height / 20), int(height / 20))
    font = title.render("X", True, BLACK)
    screen.blit(font, (target_w - font.get_width() / 2, target_h - font.get_height() / 2))

    pygame.draw.line(screen, GREEN, [0, 0], [0, height], 10)
    pygame.draw.line(screen, BLUE, [width, 0], [width, height], 10)

    screen.blit(title.render(f" f(x) = {func[0:cursor] + '_' + func[cursor:]} ", True, BLACK, GRAY), (10, 10))
    font = title.render(f" Level: {level} ", True, BLACK, GRAY)
    screen.blit(font, (width - font.get_width() - 10, 10))

    pygame.display.flip()
