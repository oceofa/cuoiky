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
assets_folder = "assets"  # Thư mục chứa ảnh

# Load images
dino_image = pygame.image.load('dino.gif').convert_alpha()
background_image = pygame.image.load('background1.JPG').convert_alpha()
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
menu_background = pygame.image.load('menu_background.gif').convert_alpha()
menu_background = pygame.transform.scale(menu_background, (WIDTH, HEIGHT))

# Resize images
dino_image = pygame.transform.scale(dino_image, (100, 100))

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Clock and FPS
clock = pygame.time.Clock()
FPS = 60

# Player (Dinosaur) properties
dino_width = 50
dino_height = 50
dino_x = 50
dino_y = HEIGHT - dino_height - 10
jumping = False
jump_count = 10

# Obstacle properties
obstacle_speed = 5
obstacle_frequency = 2000
obstacles = []

# Font
font = pygame.font.SysFont("Arial", 36)
title_font = pygame.font.SysFont("Arial", 48, bold=True)

# Score
score = 0
bg_x = 0
bg_speed = 3

# Timer for obstacle generation
pygame.time.set_timer(pygame.USEREVENT, obstacle_frequency)

# Animation properties
animation_timer = 0
# Tải ảnh khung hình động của dinosaur
dino_frames = []
for i in range(1, 7):
    frame_path = os.path.join(assets_folder, f'dino_frame{i}.png')  # Đường dẫn đến tệp ảnh
    dino_frame = pygame.image.load(frame_path).convert_alpha()  # Tải ảnh
    dino_frame = pygame.transform.scale(dino_frame, (50, 50))  # Chỉnh kích thước khung hình động
    dino_frames.append(dino_frame)
dino_frame_index = 0

# High Score Functions
def load_high_score(file_name="high_score.txt"):
    try:
        with open(file_name, "r") as file:
            return int(file.read().strip())
    except FileNotFoundError:
        with open(file_name, "w") as file:
            file.write("0")  # Nếu file không tồn tại, tạo file mới với giá trị 0
        return 0

def save_high_score(high_score, file_name="high_score.txt"):
    with open(file_name, "w") as file:
        file.write(str(high_score))

# Biến điểm cao
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
            obstacle_type = random.choice(["rect", "ellipse"])
            obstacle_x = WIDTH
            obstacle_y = HEIGHT - random.randint(20, 30)
            obstacle_width = random.randint(20, 30)
            obstacle_height = random.randint(20, 30)
            obstacles.append((obstacle_type, pygame.Rect(obstacle_x, obstacle_y, obstacle_width, obstacle_height), random.choice([RED, GREEN])))

    # Get pressed keys
    keys = pygame.key.get_pressed()

    # Jumping logic
    if not jumping:
        if keys[pygame.K_SPACE]:
            jumping = True
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
    for obstacle in obstacles[:]:
        obstacle[1].x -= obstacle_speed
        if obstacle[1].colliderect(pygame.Rect(dino_x, dino_y, dino_width, dino_height)):
            # Update high score and save if needed
            if score > high_score:
                high_score = score
                save_high_score(high_score)
            game_over_text = font.render("Game Over!", True, RED)
            screen.blit(game_over_text, (WIDTH // 3, HEIGHT // 3))
            pygame.display.flip()
            pygame.time.delay(2000)
            running = False
        if obstacle[1].x < 0:
            obstacles.remove(obstacle)
            score += 1

    # Update animation
    animation_timer += 1
    if animation_timer % 10 == 0:
        dino_frame_index = (dino_frame_index + 1) % len(dino_frames)

    # Draw Dinosaur
    screen.blit(dino_frames[dino_frame_index], (dino_x, dino_y))

    # Draw obstacles
    for obstacle_type, rect, color in obstacles:
        if obstacle_type == "rect":
            pygame.draw.rect(screen, color, rect)
        elif obstacle_type == "ellipse":
            pygame.draw.ellipse(screen, color, rect)

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
