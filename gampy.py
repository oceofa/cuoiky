import pygame
import random
import sys
from PIL import Image

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dinosaur Jump Game")

# Load images
background_image = pygame.image.load('background.jpg')  # Tải hình ảnh nền
background_image = pygame.transform.scale(background_image, (800, 400))  # Resize background image
# Dinosaur GIF processing
dino_gif = Image.open('dino.gif')  # Load GIF using Pillow
dino_frames = []  # To store each frame of the GIF
frame_count = dino_gif.n_frames  # Number of frames in the GIF

# Extract frames from the GIF
for frame in range(frame_count):
    dino_gif.seek(frame)  # Move to the next frame
    frame_image = pygame.image.fromstring(dino_gif.tobytes(), dino_gif.size, dino_gif.mode)
    dino_frames.append(pygame.transform.scale(frame_image, (50, 50)))  # Resize to fit the game window

# Obstacle properties
obstacle_image = pygame.image.load('obstacle.jpg')  # Ensure the obstacle image exists
obstacle_image = pygame.transform.scale(obstacle_image, (20, 50))  # Resize obstacle image
obstacle_speed = 7  # Initial obstacle speed

# Dinosaur properties
dino_width = 50
dino_height = 50
dino_x = 50
dino_y = HEIGHT - dino_height - 10
jumping = False
jump_count = 10

# Other setup
clock = pygame.time.Clock()
FPS = 60
font = pygame.font.SysFont("Arial", 36)
score = 0
obstacles = []

# Timer for obstacle generation
pygame.time.set_timer(pygame.USEREVENT, 1500)

# Game loop
running = True
start_ticks = pygame.time.get_ticks()  # Track the starting time
frame_index = 0  # For cycling through GIF frames
while running:
    screen.blit(background_image, (0, 0))  # Display background image
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.USEREVENT:  # Generate new obstacle
            obstacle_x = WIDTH
            obstacle_y = HEIGHT - obstacle_image.get_height() - 10
            obstacles.append(pygame.Rect(obstacle_x, obstacle_y, obstacle_image.get_width(), obstacle_image.get_height()))

    # Get pressed keys
    keys = pygame.key.get_pressed()

    # Jumping logic
    if not jumping:
        if keys[pygame.K_SPACE]:  # Jump when SPACE is pressed
            jumping = True
    else:
        if jump_count >= -10:
            neg = 1
            if jump_count < 0:
                neg = -1
            dino_y -= (jump_count ** 2) * 0.7 * neg  # Adjust jump speed (height)
            jump_count -= 1
        else:
            jumping = False
            jump_count = 10  # Reset jump count

    # Update obstacles
    for obstacle in obstacles[:]:
        obstacle.x -= obstacle_speed
        if obstacle.colliderect(pygame.Rect(dino_x, dino_y, dino_width, dino_height)):
            # Game Over logic
            game_over_text = font.render("Game Over!", True, (255, 0, 0))
            screen.blit(game_over_text, (WIDTH // 3, HEIGHT // 3))
            pygame.display.flip()
            pygame.time.delay(2000)  # Wait for 2 seconds before quitting
            running = False
        if obstacle.x < 0:
            obstacles.remove(obstacle)
            score += 1
            obstacle_speed +=0.3

    # Display Dinosaur (using GIF frames)
    screen.blit(dino_frames[frame_index], (dino_x, dino_y))

    # Draw obstacles (using image)
    for obstacle in obstacles:
        screen.blit(obstacle_image, (obstacle.x, obstacle.y))

    # Display score
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))

    # Cycle through GIF frames to animate the dinosaur
    frame_index = (frame_index + 1) % frame_count  # Loop through frames    

    # Update the display
    pygame.display.flip()  
    clock.tick(FPS)       

# Quit the game
pygame.quit()
sys.exit()