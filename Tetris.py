import pygame
import random

# Spielfeldgröße
WIDTH, HEIGHT = 10, 16
BLOCK_SIZE = 80
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
        self.last_move_time = 0
        self.last_rotate_time = 0

    def rotate(self, grid):
        rotated = [list(row) for row in zip(*self.shape[::-1])]
        if not check_collision(grid, rotated, (self.x, self.y)):
            self.shape = rotated

def check_collision(grid, shape, offset):
    off_x, off_y = offset
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:
                new_x = x + off_x
                new_y = y + off_y
                if new_x < 0 or new_x >= WIDTH or new_y < 0 or new_y >= HEIGHT:
                    return True
                if grid[new_y][new_x]:
                    return True
    return False

def clear_rows(grid):
    new_grid = [row for row in grid if any(cell == 0 for cell in row)]
    while len(new_grid) < HEIGHT:
        new_grid.insert(0, [0] * WIDTH)
    return new_grid

def draw_grid(screen, grid, current_tetromino):
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            color = COLORS[cell]
            pygame.draw.rect(screen, color, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)
            pygame.draw.rect(screen, (50, 50, 50), (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)
    
    for y, row in enumerate(current_tetromino.shape):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, COLORS[current_tetromino.color], 
                                 ((current_tetromino.x + x) * BLOCK_SIZE, (current_tetromino.y + y) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)
                pygame.draw.rect(screen, (50, 50, 50), 
                                 ((current_tetromino.x + x) * BLOCK_SIZE, (current_tetromino.y + y) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)

def game_loop():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    pygame.joystick.init()
    joystick = None
    if pygame.joystick.get_count() > 0:
        joystick = pygame.joystick.Joystick(0)
        joystick.init()
    
    while True:
        grid = [[0] * WIDTH for _ in range(HEIGHT)]
        current_tetromino = Tetromino(random.choice(SHAPES))
        game_over = False
        fall_time = 0
        fall_speed = 500
        move_delay = 150  # Minimum Zeit zwischen Bewegungen
        last_move_time = 0
        last_rotate_time = 0

        while not game_over:
            screen.fill((0, 0, 0))
            delta_time = clock.tick(60)
            fall_time += delta_time
            current_time = pygame.time.get_ticks()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT and not check_collision(grid, current_tetromino.shape, (current_tetromino.x - 1, current_tetromino.y)):
                        current_tetromino.x -= 1
                    elif event.key == pygame.K_RIGHT and not check_collision(grid, current_tetromino.shape, (current_tetromino.x + 1, current_tetromino.y)):
                        current_tetromino.x += 1
                    elif event.key == pygame.K_DOWN and not check_collision(grid, current_tetromino.shape, (current_tetromino.x, current_tetromino.y + 1)):
                        current_tetromino.y += 1
                    elif event.key == pygame.K_UP:
                        current_tetromino.rotate(grid)
            
            if joystick:
                if current_time - last_move_time > move_delay:
                    axis_x = joystick.get_axis(0)
                    axis_y = joystick.get_axis(1)
                    if axis_x < -0.5 and not check_collision(grid, current_tetromino.shape, (current_tetromino.x - 1, current_tetromino.y)):
                        current_tetromino.x -= 1
                    elif axis_x > 0.5 and not check_collision(grid, current_tetromino.shape, (current_tetromino.x + 1, current_tetromino.y)):
                        current_tetromino.x += 1
                    if axis_y > 0.5 and not check_collision(grid, current_tetromino.shape, (current_tetromino.x, current_tetromino.y + 1)):
                        current_tetromino.y += 1
                    last_move_time = current_time
                if joystick.get_button(0) and current_time - last_rotate_time > move_delay:
                    current_tetromino.rotate(grid)
                    last_rotate_time = current_time
            
            if fall_time >= fall_speed:
                if not check_collision(grid, current_tetromino.shape, (current_tetromino.x, current_tetromino.y + 1)):
                    current_tetromino.y += 1
                else:
                    for y, row in enumerate(current_tetromino.shape):
                        for x, cell in enumerate(row):
                            if cell and 0 <= current_tetromino.y + y < HEIGHT and 0 <= current_tetromino.x + x < WIDTH:
                                grid[current_tetromino.y + y][current_tetromino.x + x] = current_tetromino.color
                    grid = clear_rows(grid)
                    current_tetromino = Tetromino(random.choice(SHAPES))
                    if check_collision(grid, current_tetromino.shape, (current_tetromino.x, current_tetromino.y)):
                        game_over = True
                fall_time = 0

            draw_grid(screen, grid, current_tetromino)
            pygame.display.flip()

if __name__ == "__main__":
    game_loop()