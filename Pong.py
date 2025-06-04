import pygame

# Spielfeldgröße
WIDTH, HEIGHT = 16, 10  # Gedrehtes Spielfeld
BLOCK_SIZE = 50
SCREEN_WIDTH, SCREEN_HEIGHT = WIDTH * BLOCK_SIZE, HEIGHT * BLOCK_SIZE

# Farben
BACKGROUND_COLOR = (0, 0, 0)
PADDLE_COLOR = (255, 255, 255)
BALL_COLOR = (255, 255, 255)

class PongGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.reset()

    def reset(self):
        self.paddle1 = pygame.Rect(1 * BLOCK_SIZE, (HEIGHT // 2 - 2) * BLOCK_SIZE, BLOCK_SIZE, 2 * BLOCK_SIZE)
        self.paddle2 = pygame.Rect((WIDTH - 2) * BLOCK_SIZE, (HEIGHT // 2 - 2) * BLOCK_SIZE, BLOCK_SIZE, 2 * BLOCK_SIZE)
        self.ball = pygame.Rect(WIDTH // 2 * BLOCK_SIZE, HEIGHT // 2 * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)  # Quadratisch
        self.ball_speed = [BLOCK_SIZE // 4, BLOCK_SIZE // 4]
        self.paddle_speed = BLOCK_SIZE // 2

    def handle_events(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and self.paddle1.top > 0:
            self.paddle1.y -= self.paddle_speed
        if keys[pygame.K_s] and self.paddle1.bottom < SCREEN_HEIGHT:
            self.paddle1.y += self.paddle_speed
        if keys[pygame.K_UP] and self.paddle2.top > 0:
            self.paddle2.y -= self.paddle_speed
        if keys[pygame.K_DOWN] and self.paddle2.bottom < SCREEN_HEIGHT:
            self.paddle2.y += self.paddle_speed
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
        self.ball.x += self.ball_speed[0]
        self.ball.y += self.ball_speed[1]
        
        if self.ball.top <= 0 or self.ball.bottom >= SCREEN_HEIGHT:
            self.ball_speed[1] = -self.ball_speed[1]

        if self.ball.colliderect(self.paddle1) or self.ball.colliderect(self.paddle2):
            self.ball_speed[0] = -self.ball_speed[0]

        if self.ball.left <= 0 or self.ball.right >= SCREEN_WIDTH:
            self.reset()

    def draw(self):
        self.screen.fill(BACKGROUND_COLOR)
        pygame.draw.rect(self.screen, PADDLE_COLOR, self.paddle1)
        pygame.draw.rect(self.screen, PADDLE_COLOR, self.paddle2)
        pygame.draw.rect(self.screen, BALL_COLOR, self.ball)  # Quadratische Darstellung
        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(30)
        pygame.quit()

if __name__ == "__main__":
    PongGame().run()
