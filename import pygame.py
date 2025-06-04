import pygame
import random

# Spielfeldgröße
WIDTH, HEIGHT = 10, 16
BLOCK_SIZE = 30
SCREEN_WIDTH, SCREEN_HEIGHT = WIDTH * BLOCK_SIZE, HEIGHT * BLOCK_SIZE

# Farben
COLORS = [(0, 0, 0), (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 165, 0), (128, 0, 128)]

# Tetromino-Formen
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[0, 1, 1], [1, 1, 0]],  # S
    [[1, 1, 0], [0, 1, 1]],  # Z
    [[1, 0, 0], [1, 1, 1]],  # L
    [[0, 0, 1], [1, 1, 1]],  # J
    [[0, 1, 0], [1, 1, 1]]  # T
]

class Tetromino:
    def __init__(self, shape):
        self.shape = shape
        self.x = WIDTH // 2 - len(shape[0]) // 2
        self.y = 0
        self.color = random.randint(1, len(COLORS) - 1)

    def rotate(self):
        self.shape = [list(row) for row in zip(*self.shape[::-1])]

def check_collision(grid, shape, offset):
    off_x, off_y = offset
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell and (x + off_x < 0 or x + off_x >= WIDTH or y + off_y >= HEIGHT or grid[y + off_y][x + off_x]):
                return True
    return False

def clear_rows(grid):
    new_grid = [row for row in grid if any(cell == 0 for cell in row)]
    while len(new_grid) < HEIGHT:
        new_grid.insert(0, [0] * WIDTH)
    return new_grid

def draw_grid(screen, grid):
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            color = COLORS[cell]
            pygame.draw.rect(screen, color, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)
            pygame.draw.rect(screen, (50, 50, 50), (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    grid = [[0] * WIDTH for _ in range(HEIGHT)]
    current_tetromino = Tetromino(random.choice(SHAPES))
    game_over = False

    while not game_over:
        screen.fill((0, 0, 0))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if not check_collision(grid, current_tetromino.shape, (current_tetromino.x - 1, current_tetromino.y)):
                        current_tetromino.x -= 1
                elif event.key == pygame.K_RIGHT:
                    if not check_collision(grid, current_tetromino.shape, (current_tetromino.x + 1, current_tetromino.y)):
                        current_tetromino.x += 1
                elif event.key == pygame.K_DOWN:
                    if not check_collision(grid, current_tetromino.shape, (current_tetromino.x, current_tetromino.y + 1)):
                        current_tetromino.y += 1
                elif event.key == pygame.K_UP:
                    rotated = [list(row) for row in zip(*current_tetromino.shape[::-1])]
                    if not check_collision(grid, rotated, (current_tetromino.x, current_tetromino.y)):
                        current_tetromino.shape = rotated

        if not check_collision(grid, current_tetromino.shape, (current_tetromino.x, current_tetromino.y + 1)):
            current_tetromino.y += 1
        else:
            for y, row in enumerate(current_tetromino.shape):
                for x, cell in enumerate(row):
                    if cell:
                        grid[current_tetromino.y + y][current_tetromino.x + x] = current_tetromino.color
            grid = clear_rows(grid)
            current_tetromino = Tetromino(random.choice(SHAPES))
            if check_collision(grid, current_tetromino.shape, (current_tetromino.x, current_tetromino.y)):
                game_over = True

        draw_grid(screen, grid)
        pygame.display.flip()
        clock.tick(5)
    
    pygame.quit()

if __name__ == "__main__":
    main()
