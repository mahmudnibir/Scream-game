import pygame
import sounddevice as sd
import numpy as np

# Initialize pygame
pygame.init()

# Set up the game window
WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Scream Game")

# Player properties
player = pygame.Rect(100, HEIGHT - 100, 50, 50)
velocity_y = 0
is_jumping = False

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

# Game settings
GRAVITY = 1
WALK_SPEED = 5
JUMP_STRENGTH = 20

bg = pygame.image.load("background.png")
bg = pygame.transform.scale(bg , (WIDTH, HEIGHT))

# Sound thresholds (adjust these based on your environment)
NOISE_FLOOR = 0.03    # Minimum intensity to ignore background noise
WALK_THRESHOLD = 0.06 # Volume needed to start walking (talking)
JUMP_THRESHOLD = 0.2  # Volume needed to trigger a jump (screaming)

def capture_sound(indata, frames, time, status):
    global sound_intensity
    sound_intensity = np.linalg.norm(indata) / np.sqrt(len(indata))

# Start capturing sound from microphone
sound_intensity = 0  # Initialize intensity variable
sd.InputStream(callback=capture_sound).start()

def game_loop():
    global is_jumping, velocity_y

    clock = pygame.time.Clock()
    running = True
    
    while running:
        win.blit(bg)
        
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Sound-based movement with noise filtering
        if sound_intensity > NOISE_FLOOR:
            if sound_intensity < WALK_THRESHOLD:
                # Soft talk -> Walk
                player.x += WALK_SPEED
            elif sound_intensity > JUMP_THRESHOLD and not is_jumping:
                # Scream -> Jump
                is_jumping = True
                velocity_y = -JUMP_STRENGTH
        
        # Apply gravity
        if is_jumping:
            velocity_y += GRAVITY
            player.y += velocity_y
            
            # Stop jump when player hits the ground
            if player.y >= HEIGHT - 100:
                player.y = HEIGHT - 100
                is_jumping = False
                velocity_y = 0

        # Draw the player
        pygame.draw.rect(win, BLUE, player)
        
        # Update display
        pygame.display.update()
        clock.tick(30)  # 30 FPS

    pygame.quit()

if __name__ == "__main__":
    game_loop()
