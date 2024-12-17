import pygame
import random
import sys
import os

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Back to School 1")

# Asset folder
assets_folder = "assets"

# Load images
dino_image = pygame.image.load('dino.gif').convert_alpha()
background_images = [
    pygame.image.load('background1.JPG').convert_alpha(),
    pygame.image.load('background2.JPG').convert_alpha()
]
background_images = [pygame.transform.scale(bg, (WIDTH, HEIGHT)) for bg in background_images]
menu_background = pygame.image.load('menu_background.gif').convert_alpha()
menu_background = pygame.transform.scale(menu_background, (WIDTH, HEIGHT))

# Resize dinosaur
dino_width, dino_height = 100, 100
dino_image = pygame.transform.scale(dino_image, (dino_width, dino_height))

# Load obstacle images
obstacle_images = [
    pygame.image.load('obstacle1.png').convert_alpha(),
    pygame.image.load('obstacle2.png').convert_alpha(),
    pygame.image.load('obstacle3.png').convert_alpha()
]
obstacle_images = [pygame.transform.scale(img, (50, 50)) for img in obstacle_images]

# Load powerup image
powerup_image = pygame.image.load('powerup.png').convert_alpha()
powerup_image = pygame.transform.scale(powerup_image, (40, 40))

# Load sounds
pygame.mixer.init()
game_over_sound = pygame.mixer.Sound("game_over.mp3")
jump_sound = pygame.mixer.Sound("jump_sound.mp3")
background_music = os.path.join(assets_folder, "background_music.mp3")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Clock and FPS
clock = pygame.time.Clock()
FPS = 60

# Player properties
dino_x = 50
dino_y = HEIGHT - dino_height - 10
dino_ground = HEIGHT - dino_height - 10
jumping = False
jump_strength = 10
jump_count = jump_strength

# Obstacle properties
obstacle_speed = 7
obstacle_frequency = 4000
obstacles = []

# Powerup properties
powerups = []
powerup_frequency = 7000
pygame.time.set_timer(pygame.USEREVENT + 1, powerup_frequency)

# Invincibility state
invincible = False
invincible_start_time = 0
invincible_duration = 5000  # 5 seconds of invincibility

# Font
font = pygame.font.SysFont("Arial", 36)
title_font = pygame.font.SysFont("Arial", 48, bold=True)

# Score
score = 0
bg_x = 0
bg_speed = 3
current_background = 0

# Timer for obstacle generation
pygame.time.set_timer(pygame.USEREVENT, obstacle_frequency)

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

# High score
high_score = load_high_score()

# Menu Function
def show_menu():
    menu_running = True
    global high_score
    while menu_running:
        screen.blit(menu_background, (0, 0))
        title_text = title_font.render("Dinosaur Jump Game", True, BLACK)
        play_text = font.render("Press SPACE to Play", True, BLACK)
        pygame.mixer.music.load("background_music.mp3")
        pygame.mixer.music.play(-1)
        quit_text = font.render("Press Q to Quit", True, BLACK)
        high_score_text = font.render(f"High Score: {high_score}", True, BLACK)

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
    screen.blit(background_images[current_background], (bg_x, 0))
    screen.blit(background_images[current_background], (bg_x + WIDTH, 0))
    bg_x -= bg_speed

    if bg_x <= -WIDTH:
        bg_x = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.USEREVENT:
            obstacle_x = WIDTH
            obstacle_y = HEIGHT - 50
            obstacle_image = random.choice(obstacle_images)
            obstacles.append((obstacle_image, pygame.Rect(obstacle_x, obstacle_y, 10, 10)))
        if event.type == pygame.USEREVENT + 1:
            powerup_x = WIDTH
            powerup_y = random.randint(HEIGHT // 2, HEIGHT - 60)
            powerups.append(pygame.Rect(powerup_x, powerup_y, 40, 40))

    keys = pygame.key.get_pressed()

    if not jumping:
        if keys[pygame.K_SPACE]:
            jumping = True
            jump_sound.play()
    else:
        if jump_count >= -jump_strength:
            neg = 1 if jump_count >= 0 else -1
            dino_y -= (jump_count ** 2) * 0.25 * neg
            jump_count -= 1
        else:
            jumping = False
            jump_count = jump_strength
            dino_y = dino_ground

    for obstacle_image, rect in obstacles[:]:
        rect.x -= obstacle_speed
        if not invincible and rect.colliderect(pygame.Rect(dino_x, dino_y, dino_width, dino_height)):
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
            obstacle_speed += 0.8
            if score % 5 == 0:
                current_background = (current_background + 1) % 2

    for powerup_rect in powerups[:]:
        powerup_rect.x -= obstacle_speed
        if powerup_rect.colliderect(pygame.Rect(dino_x, dino_y, dino_width, dino_height)):
            invincible = True
            invincible_start_time = pygame.time.get_ticks()
            powerups.remove(powerup_rect)
        if powerup_rect.x < 0:
            powerups.remove(powerup_rect)

    if invincible and pygame.time.get_ticks() - invincible_start_time > invincible_duration:
        invincible = False

    animation_timer += 1
    if animation_timer % 10 == 0:
        dino_frame_index = (dino_frame_index + 1) % len(dino_frames)

    screen.blit(dino_frames[dino_frame_index], (dino_x, dino_y))

    for obstacle_image, rect in obstacles:
        screen.blit(obstacle_image, rect.topleft)

    for powerup_rect in powerups:
        screen.blit(powerup_image, powerup_rect.topleft)

    if invincible:
        pygame.draw.rect(screen, (0, 255, 0), (dino_x - 5, dino_y - 5, dino_width + 10, dino_height + 10), 3)

    score_text = font.render(f"Score: {score}", True, BLACK)
    high_score_text = font.render(f"High Score: {high_score}", True, BLACK)
    screen.blit(score_text, (10, 10))
    screen.blit(high_score_text, (10, 50))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
