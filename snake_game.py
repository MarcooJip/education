import pygame
import time
import random

# Inisialisasi Pygame
pygame.init()

# Ukuran layar
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
BLOCK_SIZE = 10

# Warna
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Kecepatan ular
SNAKE_SPEED = 15

# Fungsi untuk menggambar ular
def draw_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(screen, GREEN, [x[0], x[1], snake_block, snake_block])

# Fungsi utama untuk game
def game_loop():
    game_over = False
    game_close = False

    x1 = SCREEN_WIDTH / 2
    y1 = SCREEN_HEIGHT / 2

    x1_change = 0
    y1_change = 0

    snake_list = []
    length_of_snake = 1

    foodx = round(random.randrange(0, SCREEN_WIDTH - BLOCK_SIZE) / 10.0) * 10.0
    foody = round(random.randrange(0, SCREEN_HEIGHT - BLOCK_SIZE) / 10.0) * 10.0

    while not game_over:

        while game_close == True:
            screen.fill(BLACK)
            font_style = pygame.font.SysFont("bahnschrift", 25)
            mesg = font_style.render("Game Over! Press C-Play Again or Q-Quit", True, RED)
            screen.blit(mesg, [SCREEN_WIDTH / 6, SCREEN_HEIGHT / 3])
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        game_loop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -BLOCK_SIZE
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = BLOCK_SIZE
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -BLOCK_SIZE
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = BLOCK_SIZE
                    x1_change = 0

        if x1 >= SCREEN_WIDTH or x1 < 0 or y1 >= SCREEN_HEIGHT or y1 < 0:
            game_close = True

        x1 += x1_change
        y1 += y1_change
        screen.fill(BLACK)
        pygame.draw.rect(screen, WHITE, [foodx, foody, BLOCK_SIZE, BLOCK_SIZE])
        snake_head = []
        snake_head.append(x1)
        snake_head.append(y1)
        snake_list.append(snake_head)
        if len(snake_list) > length_of_snake:
            del snake_list[0]

        for x in snake_list[:-1]:
            if x == snake_head:
                game_close = True

        draw_snake(BLOCK_SIZE, snake_list)

        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, SCREEN_WIDTH - BLOCK_SIZE) / 10.0) * 10.0
            foody = round(random.randrange(0, SCREEN_HEIGHT - BLOCK_SIZE) / 10.0) * 10.0
            length_of_snake += 1

        clock.tick(SNAKE_SPEED)

    pygame.quit()

# Membuat layar
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Snake Game')
clock = pygame.time.Clock()

# Memulai game
game_loop()