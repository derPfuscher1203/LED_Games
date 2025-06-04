import pygame

def check_controllers():
    pygame.init()
    pygame.joystick.init()
    
    num_joysticks = pygame.joystick.get_count()
    if num_joysticks == 0:
        print("Kein Controller gefunden!")
        return
    
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    print(f"Gefundener Controller: {joystick.get_name()}")
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.JOYBUTTONDOWN:
                print(f"Taste {event.button} gedrückt")
            elif event.type == pygame.JOYBUTTONUP:
                print(f"Taste {event.button} losgelassen")
            elif event.type == pygame.JOYAXISMOTION:
                print(f"Achse {event.axis} bewegt: {event.value:.2f}")
            elif event.type == pygame.JOYHATMOTION:
                print(f"D-Pad bewegt: {event.value}")
        
        pygame.time.wait(100)
    
    pygame.quit()

if __name__ == "__main__":
    check_controllers()