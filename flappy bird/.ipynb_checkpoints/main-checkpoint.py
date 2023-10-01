import pygame
import sys
import random
from pygame.locals import *

def motion_floor():
    screen.blit(floor, (floor_x_pos, 480))
    screen.blit(floor, (floor_x_pos + 480, 480))

def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop=(500, random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midtop=(500, random_pipe_pos - 680))
    return bottom_pipe, top_pipe

def move_pipe(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes

def draw_pipe(pipes):
    for pipe in pipes:
        if pipe.bottom >= 640:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)

def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            return False
    if bird_rect.top <= -50 or bird_rect.bottom >= 480:
        return False
    return True


pygame.init()
screen = pygame.display.set_mode((480, 640))
clock = pygame.time.Clock()
gravity = 0.25
bird_move = 0
game_active = True

bg = pygame.image.load('FileGame/assets/background-night.png').convert()
bg = pygame.transform.scale2x(bg)

floor = pygame.image.load('FileGame/assets/floor.png').convert()
floor = pygame.transform.scale2x(floor)
floor_x_pos = 0

bird = pygame.image.load('FileGame/assets/yellowbird-midflap.png').convert()
bird = pygame.transform.scale2x(bird)
bird_rect = bird.get_rect(center=(100, 320))

pipe_surface = pygame.image.load('FileGame/assets/pipe-green.png').convert()
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []

spawnpipe = pygame.USEREVENT
pygame.time.set_timer(spawnpipe, 1500)
pipe_height = [a for a in range(150, 400)]

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_SPACE and game_active:
                bird_move = 0
                bird_move = -7
            if event.key == K_SPACE and not game_active:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (100, 320)
                bird_move = 0
        if event.type == spawnpipe:
            pipe_list.extend(create_pipe())

    screen.blit(bg, (0, -90))
    screen.blit(bg, (216, -90))

    floor_x_pos -= 1
    motion_floor()
    if floor_x_pos <= -480:
        floor_x_pos = 0

    if game_active:
        bird_move += gravity
        bird_rect.centery += bird_move
        screen.blit(bird, bird_rect)
        game_active = check_collision(pipe_list)
        pipe_list = move_pipe(pipe_list)
        draw_pipe(pipe_list)

    pygame.display.update()
    clock.tick(60)
