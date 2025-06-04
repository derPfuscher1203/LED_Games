import pygame
import time

# Spielfeldgröße
WIDTH, HEIGHT = 16, 10  # Lowpixel Style
BLOCK_SIZE = 80  # Kleinere Blöcke für bessere Darstellung
SCREEN_WIDTH, SCREEN_HEIGHT = WIDTH * BLOCK_SIZE, HEIGHT * BLOCK_SIZE

# Farben
BACKGROUND_COLOR = (0, 0, 0)
TEXT_COLOR = (255, 255, 255)

# LED-Matrix-Zahlen (3x5 Pixel pro Zahl)
NUMBERS = {
    "0": ["###", "# #", "# #", "# #", "###"],
    "1": [" # ", " # ", " # ", " # ", " # "],  # Schmale 1 als Balken
    "2": ["###", "  #", "###", "#  ", "###"],
    "3": ["###", "  #", "###", "  #", "###"],
    "4": ["# #", "# #", "###", "  #", "  #"],
    "5": ["###", "#  ", "###", "  #", "###"],
    "6": ["###", "#  ", "###", "# #", "###"],
    "7": ["###", "  #", "  #", "  #", "  #"],
    "8": ["###", "# #", "###", "# #", "###"],
    "9": ["###", "# #", "###", "  #", "###"],
    ":": ["   ", " # ", "   ", " # ", "   "]  # Doppelpunkt mittig
}

class LowpixelClock:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Lowpixel Clock")
        self.clock = pygame.time.Clock()
        self.running = True

    def draw_digit(self, digit, x_offset, y_offset):
        pattern = NUMBERS[digit]
        for row_idx, row in enumerate(pattern):
            for col_idx, pixel in enumerate(row):
                if pixel == "#":
                    pygame.draw.rect(self.screen, TEXT_COLOR, ((x_offset + col_idx) * BLOCK_SIZE, (y_offset + row_idx) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

    def draw_time(self):
        current_time = time.strftime("%H:%M")  # Format HH:MM ohne Sekunden
        hour = int(time.strftime("%H"))
        if hour > 19:
            return  # Uhr funktioniert nur bis 19 Uhr
        
        self.screen.fill(BACKGROUND_COLOR)
        
        # Berechnung der Startposition für zentrierte Anzeige
        total_width = 4 * 3 + 1 * 2 + 1  # 4 Ziffern á 3 Breite + 1 Doppelpunkt á 2 Breite + 1 Pixel Abstand nach den Stunden
        start_x = (WIDTH - total_width) // 2
        x_offset = start_x
        y_offset = 2  # Etwas nach unten setzen
        
        for digit in current_time:
            self.draw_digit(digit, x_offset, y_offset)
            x_offset += 2 if digit == "1" else (3 if digit != ":" else 2)  # 1 ist jetzt schmaler
            if digit == ":":
                x_offset += 1  # 1 Pixel Abstand nach den Stunden
        
        pygame.display.flip()

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            
            self.draw_time()
            self.clock.tick(1)  # Aktualisiert jede Sekunde
        
        pygame.quit()

if __name__ == "__main__":
    LowpixelClock().run()
