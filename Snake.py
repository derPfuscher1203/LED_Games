import pygame
import random

# Spielfeldgröße
WIDTH, HEIGHT = 10, 16
BLOCK_SIZE = 50
SCREEN_WIDTH, SCREEN_HEIGHT = WIDTH * BLOCK_SIZE, HEIGHT * BLOCK_SIZE

# Farben
BACKGROUND_COLOR = (0, 0, 0)
SNAKE_COLOR =  (252, 188, 27) 
FOOD_COLOR =  (0, 255, 0) 

class SnakeGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.reset()
        self.speed = 7  # Geschwindigkeit angepasst
        
        # Controller initialisieren
        pygame.joystick.init()
        self.joystick = None
        if pygame.joystick.get_count() > 0:
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()
        
        # Eingabe-Verzögerung reduzieren
        self.move_delay = 100  # Millisekunden
        self.last_move_time = 0

    def flash_red(self):
        for _ in range(3):
            self.screen.fill((255, 0, 0))  # Rotes Blinken
            pygame.display.flip()
            pygame.time.delay(200)  # 200ms warten
            self.screen.fill(BACKGROUND_COLOR)
            pygame.display.flip()
            pygame.time.delay(200)

    def reset(self):
        self.snake = [(WIDTH // 2, HEIGHT // 2)]
        self.direction = (0, -1)
        self.food = self.spawn_food()
        self.grow_snake = False

    def spawn_food(self):
        while True:
            food = (random.randint(0, WIDTH - 1), random.randint(0, HEIGHT - 1))
            if food not in self.snake:
                return food

    def handle_events(self):
        current_time = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and self.direction != (0, 1):
                    self.direction = (0, -1)
                elif event.key == pygame.K_DOWN and self.direction != (0, -1):
                    self.direction = (0, 1)
                elif event.key == pygame.K_LEFT and self.direction != (1, 0):
                    self.direction = (-1, 0)
                elif event.key == pygame.K_RIGHT and self.direction != (-1, 0):
                    self.direction = (1, 0)
        
        # Controller Steuerung mit minimaler Verzögerung für flüssige Eingabe
        if self.joystick and current_time - self.last_move_time > self.move_delay:
            axis_x = self.joystick.get_axis(0)
            axis_y = self.joystick.get_axis(1)
            if axis_y < -0.5 and self.direction != (0, 1):
                self.direction = (0, -1)
            elif axis_y > 0.5 and self.direction != (0, -1):
                self.direction = (0, 1)
            elif axis_x < -0.5 and self.direction != (1, 0):
                self.direction = (-1, 0)
            elif axis_x > 0.5 and self.direction != (-1, 0):
                self.direction = (1, 0)
            self.last_move_time = current_time

    def update(self):
        head_x, head_y = self.snake[0]
        new_head = (head_x + self.direction[0], head_y + self.direction[1])

        # Wenn die Schlange aus dem Spielfeld fährt, auf der anderen Seite wieder erscheinen lassen
        new_head = (new_head[0] % WIDTH, new_head[1] % HEIGHT)

        if new_head in self.snake:
            self.flash_red()
            self.reset()
            return

        self.snake.insert(0, new_head)

        if new_head == self.food:
            self.food = self.spawn_food()
        else:
            self.snake.pop()

    def draw(self):
        self.screen.fill(BACKGROUND_COLOR)
        
        for x, y in self.snake:
            pygame.draw.rect(self.screen, SNAKE_COLOR, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
        
        fx, fy = self.food
        pygame.draw.rect(self.screen, FOOD_COLOR, (fx * BLOCK_SIZE, fy * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
        
        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(self.speed)  # Geschwindigkeit regulieren
        pygame.quit()

if __name__ == "__main__":
    SnakeGame().run()
