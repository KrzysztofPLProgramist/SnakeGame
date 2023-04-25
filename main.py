import pygame
import random
import datetime

tile_size = 15

screen_size = (800, 600)

columns = screen_size[0] // tile_size
rows = screen_size[1] // tile_size

pygame.init()

screen = pygame.display.set_mode(screen_size)


def generate_grid(apple=True):
    global grid
    grid = []
    for row in range(rows+1):
        grid.append([])
        for col in range(columns+1):
            # grid[-1].append(random.choice(['apple', 'nothing', 'snake']))
            grid[-1].append('nothing')
    apples_in_random(1)
    return grid


def apples_in_random(num):
    global grid
    for _ in range(num):
        if grid[random.randint(0, rows - 1)][random.randint(0, columns - 1)] != 'apple':
            grid[random.randint(0, rows - 1)][random.randint(0, columns - 1)] = 'apple'
        else:
            grid[random.randint(0, rows - 1)][random.randint(0, columns - 1)] = 'apple'


def draw_grid(grid):
    for row, i in enumerate(grid):
        for col, l in enumerate(i):
            if l == 'snake':
                if (row, col) in snake:
                    pygame.draw.rect(screen, (0, 255, 0),
                                     (col * tile_size, row * tile_size, (col + 1) * tile_size, (row + 1) * tile_size))
                elif grid[row][col] != 'apple':
                    grid[row][col] = 'nothing'
                else:
                    snake_lenght += 1
            elif l == 'nothing':
                pygame.draw.rect(screen, (15, 15, 15),
                                 (col * tile_size, row * tile_size, (col + 1) * tile_size, (row + 1) * tile_size))
            elif l == 'apple':
                pygame.draw.rect(screen, (255, 0, 0),
                                 (col * tile_size, row * tile_size, (col + 1) * tile_size, (row + 1) * tile_size))


grid = generate_grid()

head = (5, 5)

global os
os = ''

time = datetime.datetime.now().second


def events(move, WSAD=True):
    global grid, dire, os, pause, time
    keys = pygame.key.get_pressed()

    if keys[pygame.K_r]:
        reset()
    if keys[pygame.K_SPACE]:
        if time + 0.5 < datetime.datetime.now().second + 0.0:
            pause = not pause
            time = datetime.datetime.now().second
    if move:
        if WSAD:
            if keys[pygame.K_w] and os != 's':
                dire = (-1, 0)
                os = 'w'
            else:
                if keys[pygame.K_d] and os != 'a':
                    dire = (0, 1)
                    os = 'd'
                else:
                    if keys[pygame.K_a] and os != 'd':
                        dire = (0, -1)
                        os = 'a'
                    else:
                        if keys[pygame.K_s] and os != 'w':
                            dire = (1, 0)
                            os = 's'
        else:
            if keys[pygame.K_UP] and os != 's':
                dire = (-1, 0)
                os = 'w'
            else:
                if keys[pygame.K_RIGHT] and os != 'a':
                    dire = (0, 1)
                    os = 'd'
                else:
                    if keys[pygame.K_LEFT] and os != 'd':
                        dire = (0, -1)
                        os = 'a'
                    else:
                        if keys[pygame.K_DOWN] and os != 'w':
                            dire = (1, 0)
                            os = 's'

        snake.append((head[0] + dire[0], head[1] + dire[1]))


def reset():
    global snake_lenght, dire, snake, os, hi_score
    if snake_lenght > hi_score:
        hi_score = snake_lenght
    snake_lenght = 100
    dire = (0, 0)
    snake = [(5, 5)]
    os = ''
    generate_grid()


global snake, snake_lenght, dire, hi_score
dire = (0, 0)
snake = [head]
snake_lenght = 1
clock = pygame.time.Clock()
pause = False


def score():
    global hi_score
    if snake_lenght > hi_score:
        hi_score = snake_lenght
    font = pygame.font.SysFont(('comicsansms'), 55)
    txt = font.render(str(snake_lenght), True, (100, 100, 100))
    screen.blit(txt, (10, 0))
    txt = font.render('HI: '+str(hi_score), True, (100, 100, 100))
    screen.blit(txt, (screen_size[0]-(30*len('HI: '+str(hi_score))), 0))

hi_score = 1

music = 'miusic.wav'
pygame.mixer.music.load(music)
pygame.mixer.music.play(10**5)

while True:
    snake = snake[-snake_lenght:]
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
        if event.type == pygame.KEYDOWN:
            # if event.type == pygame.K_r:
            #     generate_grid()
            #     print('yep')
            pass
    if pause:
        events(False)
    else:
        events(True, False)
    s = []
    for i in snake:
        try:
            if i[1] > columns or i[0] > rows or i[1] < 0 or i[0] < 0:
                reset()
            if grid[i[0]][i[1]] == 'apple':
                snake_lenght += 3
                apples_in_random(1)
            if i in s and not pause:
                reset()
            grid[i[0]][i[1]] = 'snake'
            s.append(i)
        except:
            pass
    head = snake[-1]
    draw_grid(grid)
    score()
    pygame.display.flip()
    clock.tick(5)
