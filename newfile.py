import pygame
import random
import sys
import os

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dinosaur Jump Game")

# Tạo một thư mục chứa các tệp ảnh (assets)
assets_folder = "assets"

# Load images
dino_image = pygame.image.load('dino.gif').convert_alpha()
background_image = pygame.image.load('background1.JPG').convert_alpha()
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
menu_background = pygame.image.load('menu_background.gif').convert_alpha()
menu_background = pygame.transform.scale(menu_background, (WIDTH, HEIGHT))

# Resize images
dino_width = 100
dino_height = 100
dino_image = pygame.transform.scale(dino_image, (dino_width, dino_height))

# Load obstacle images
obstacle_images = [
    pygame.image.load('obstacle1.png').convert_alpha(),
    pygame.image.load('obstacle2.png').convert_alpha(),
    pygame.image.load('obstacle3.png').convert_alpha()
]
obstacle_images = [pygame.transform.scale(img, (50, 50)) for img in obstacle_images]

# Load item images
item_images = [
    pygame.image.load('item1.png').convert_alpha(),
    pygame.image.load('item2.png').convert_alpha()
]
item_images = [pygame.transform.scale(img, (30, 30)) for img in item_images]

# Load sounds
pygame.mixer.init()
game_over_sound = pygame.mixer.Sound("game_over.mp3")
jump_sound = pygame.mixer.Sound("jump_sound.mp3")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Clock and FPS
clock = pygame.time.Clock()
FPS = 60

# Player (Dinosaur) properties
dino_x = 50
dino_y = HEIGHT - dino_height - 10
jumping = False
jump_count = 10

# Obstacle properties
obstacle_speed = 10
obstacle_frequency = 2000
obstacles = []

# Item properties
item_frequency = 5000  # Frequency of item appearance (ms)
items = []

# Font
font = pygame.font.SysFont("Arial", 36)
title_font = pygame.font.SysFont("Arial", 48, bold=True)

# Score
score = 0
bg_x = 0
bg_speed = 3

# Timer for obstacle and item generation
pygame.time.set_timer(pygame.USEREVENT, obstacle_frequency)
pygame.time.set_timer(pygame.USEREVENT + 1, item_frequency)

# Animation properties
animation_timer = 0
dino_frames = []
for i in range(1, 7):
    frame_path = os.path.join(assets_folder, f'dino_frame{i}.png')
    dino_frame = pygame.image.load(frame_path).convert_alpha()
    dino_frame = pygame.transform.scale(dino_frame, (dino_width, dino_height))
    dino_frames.append(dino_frame)
dino_frame_index = 0

# High Score Functions
def load_high_score(file_name="high_score.txt"):
    try:
        with open(file_name, "r") as file:
            return int(file.read().strip())
    except FileNotFoundError:
        with open(file_name, "w") as file:
            file.write("0")
        return 0

def save_high_score(high_score, file_name="high_score.txt"):
    with open(file_name, "w") as file:
        file.write(str(high_score))

# High Score
high_score = load_high_score()

# Menu Function
def show_menu():
    menu_running = True
    global high_score
    while menu_running:
        screen.blit(menu_background, (0, 0))
        title_text = title_font.render("Dinosaur Jump Game", True, BLACK)
        play_text = font.render("Press SPACE to Play", True, BLACK)
        quit_text = font.render("Press Q to Quit", True, BLACK)
        high_score_text = font.render(f"High Score: {high_score}", True, BLACK)

        # Draw menu elements
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 4))
        screen.blit(play_text, (WIDTH // 2 - play_text.get_width() // 2, HEIGHT // 2 - 60))
        screen.blit(quit_text, (WIDTH // 2 - quit_text.get_width() // 2, HEIGHT // 2 + 10))
        screen.blit(high_score_text, (WIDTH // 2 - high_score_text.get_width() // 2, HEIGHT // 2 + 70))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            menu_running = False
        if keys[pygame.K_q]:
            pygame.quit()
            sys.exit()

# Game loop
running = True
show_menu()
while running:
    screen.blit(background_image, (bg_x, 0))
    screen.blit(background_image, (bg_x + WIDTH, 0))
    bg_x -= bg_speed
    if bg_x <= -WIDTH:
        bg_x = 0

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.USEREVENT:
            obstacle_x = WIDTH
            obstacle_y = HEIGHT - 50
            obstacle_image = random.choice(obstacle_images)
            obstacles.append((obstacle_image, pygame.Rect(obstacle_x, obstacle_y, 20, 20)))
        if event.type == pygame.USEREVENT + 1:
            item_x = WIDTH
            item_y = random.randint(50, HEIGHT - 100)
            item_image = random.choice(item_images)
            items.append((item_image, pygame.Rect(item_x, item_y, 30, 30)))

    # Get pressed keys
    keys = pygame.key.get_pressed()

    # Jumping logic
    if not jumping:
        if keys[pygame.K_SPACE]:
            jumping = True
            jump_sound.play()
    else:
        if jump_count >= -10:
            neg = 1
            if jump_count < 0:
                neg = -1
            dino_y -= (jump_count ** 2) * 0.4 * neg
            jump_count -= 1
        else:
            jumping = False
            jump_count = 10

    # Update obstacles
    for obstacle_image, rect in obstacles[:]:
        rect.x -= obstacle_speed
        if rect.colliderect(pygame.Rect(dino_x, dino_y, dino_width, dino_height)):
            game_over_sound.play()
            if score > high_score:
                high_score = score
                save_high_score(high_score)
            game_over_text = font.render("Game Over!", True, RED)
            screen.blit(game_over_text, (WIDTH // 3, HEIGHT // 3))
            pygame.display.flip()
            pygame.time.delay(2000)
            running = False
        if rect.x < 0:
            obstacles.remove((obstacle_image, rect))
            score += 1

    # Update items
    for item_image, rect in items[:]:
        rect.x -= obstacle_speed
        if rect.colliderect(pygame.Rect(dino_x, dino_y, dino_width, dino_height)):
            items.remove((item_image, rect))
            score += 5
        elif rect.x < 0:
            items.remove((item_image, rect))

    # Update animation
    animation_timer += 1
    if animation_timer % 10 == 0:
        dino_frame_index = (dino_frame_index + 1) % len(dino_frames)

    # Draw Dinosaur
    screen.blit(dino_frames[dino_frame_index], (dino_x, dino_y))

    # Draw obstacles
    for obstacle_image, rect in obstacles:
        screen.blit(obstacle_image, rect.topleft)

    # Draw items
    for item_image, rect in items:
        screen.blit(item_image, rect.topleft)

    # Display score and high score
    score_text = font.render(f"Score: {score}", True, BLACK)
    high_score_text = font.render(f"High Score: {high_score}", True, BLACK)
    screen.blit(score_text, (10, 10))
    screen.blit(high_score_text, (10, 50))

    # Update the display
    pygame.display.flip()
    clock.tick(FPS)

# Quit the game
pygame.quit()

