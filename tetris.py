import pygame
import random

# Ukuran layar
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 600
BLOCK_SIZE = 30

# Warna
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
COLORS = [
    (0, 255, 255),  # Cyan
    (255, 165, 0),  # Orange
    (0, 0, 255),    # Blue
    (255, 0, 0),    # Red
    (128, 0, 128),  # Purple
    (0, 255, 0),    # Green
    (255, 255, 0)   # Yellow
]

# Bentuk Tetris
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1, 1], [0, 1, 0]],  # T
    [[1, 1], [1, 1]],  # O
    [[0, 1, 1], [1, 1, 0]],  # S
    [[1, 1, 0], [0, 1, 1]],  # Z
    [[1, 0, 0], [1, 1, 1]],  # L
    [[0, 0, 1], [1, 1, 1]]   # J
]

class Tetris:
    def __init__(self):
        self.board = [[0] * (SCREEN_WIDTH // BLOCK_SIZE) for _ in range(SCREEN_HEIGHT // BLOCK_SIZE)]
        self.current_shape = self.new_shape()
        self.current_position = [0, SCREEN_WIDTH // BLOCK_SIZE // 2 - 1]
        self.score = 0

    def new_shape(self):
        shape = random.choice(SHAPES)
        return shape

    def rotate_shape(self):
        self.current_shape = [list(row) for row in zip(*self.current_shape[::-1])]

    def valid_position(self, offset):
        for i, row in enumerate(self.current_shape):
            for j, block in enumerate(row):
                if block:
                    x = j + self.current_position[1] + offset[1]
                    y = i + self.current_position[0] + offset[0]
                    if x < 0 or x >= SCREEN_WIDTH // BLOCK_SIZE or y >= SCREEN_HEIGHT // BLOCK_SIZE or (y >= 0 and self.board[y][x]):
                        return False
        return True

    def merge_shape(self):
        for i, row in enumerate(self.current_shape):
            for j, block in enumerate(row):
                if block:
                    self.board[i + self.current_position[0]][j + self.current_position[1]] = 1
        self.clear_lines()

    def clear_lines(self):
        lines_to_clear = [i for i, row in enumerate(self.board) if all(row)]
        for i in lines_to_clear:
            del self.board[i]
            self.board.insert(0, [0] * (SCREEN_WIDTH // BLOCK_SIZE))
            self.score += 1

    def drop(self):
        if self.valid_position((1, 0)):
            self.current_position[0] += 1
        else:
            self.merge_shape()
            self.current_shape = self.new_shape()
            self.current_position = [0, SCREEN_WIDTH // BLOCK_SIZE // 2 - 1]
            if not self.valid_position((0, 0)):
                return False
        return True

def draw_board(screen, board):
    for i, row in enumerate(board):
        for j, block in enumerate(row):
            if block:
                pygame.draw.rect(screen, WHITE, (j * BLOCK_SIZE, i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

def draw_shape(screen, shape, position):
    for i, row in enumerate(shape):
        for j, block in enumerate(row):
            if block:
                pygame.draw.rect(screen, COLORS[SHAPES.index(shape)], ((position[1] + j) * BLOCK_SIZE, (position[0] + i) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

def show_speed_menu(screen):
    font = pygame.font.Font(None, 36)
    speed_options = ["1. Slow", "2. Normal", "3. Fast"]
    selected_speed = 1  # Default to Normal

    while True:
        screen.fill(BLACK)
        for i, option in enumerate(speed_options):
            text = font.render(option, True, WHITE)
            screen.blit(text, ( 20, 100 + i * 40))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    selected_speed = 5  # Slow
                    return selected_speed
                elif event.key == pygame.K_2:
                    selected_speed = 10  # Normal
                    return selected_speed
                elif event.key == pygame.K_3:
                    selected_speed = 15  # Fast
                    return selected_speed

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    tetris = Tetris()
    
    speed = show_speed_menu(screen)
    if speed is None:
        return

    running = True

    while running:
        screen.fill(BLACK)
        draw_board(screen, tetris.board)
        draw_shape(screen, tetris.current_shape, tetris.current_position)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and tetris.valid_position((0, -1)):
                    tetris.current_position[1] -= 1
                if event.key == pygame.K_RIGHT and tetris.valid_position((0, 1)):
                    tetris.current_position[1] += 1
                if event.key == pygame.K_DOWN:
                    tetris.drop()
                if event.key == pygame.K_UP:
                    tetris.rotate_shape()
                    if not tetris.valid_position((0, 0)):
                        tetris.rotate_shape()  # Undo rotation if invalid

        if not tetris.drop():
            print("Game Over! Your score:", tetris.score)
            running = False

        pygame.display.flip()
        clock.tick(speed)

    pygame.quit()

if __name__ == "__main__":
    main()