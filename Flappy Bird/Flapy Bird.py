import pygame
import random
import sys

pygame.init()

# ---------------- WINDOW ----------------
WIDTH = 400
HEIGHT = 600
gameWindow = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

clock = pygame.time.Clock()
FPS = 60

# ---------------- COLORS ----------------
WHITE = (255, 255, 255)
BLUE = (0, 150, 255)
GREEN = (0, 200, 0)
BLACK = (0, 0, 0)

# ---------------- BIRD ----------------
bird_x = 80
bird_y = HEIGHT // 2
bird_radius = 15
bird_velocity = 0
gravity = 0.5
jump_strength = -8

# ---------------- PIPES ----------------
pipe_width = 60
pipe_gap = 150
pipe_speed = 4

pipe_x = WIDTH
pipe_height = random.randint(150, 400)

# ---------------- SCORE ----------------
score = 0
font = pygame.font.SysFont(None, 40)
big_font = pygame.font.SysFont(None, 60)

game_over = False

# ---------------- FUNCTIONS ----------------
def draw_window():
    gameWindow.fill(BLUE)

    # Bird
    pygame.draw.circle(gameWindow, WHITE, (bird_x, bird_y), bird_radius)

    # Pipes
    pygame.draw.rect(gameWindow, GREEN, (pipe_x, 0, pipe_width, pipe_height))
    pygame.draw.rect(
        gameWindow,
        GREEN,
        (pipe_x, pipe_height + pipe_gap, pipe_width, HEIGHT)
    )

    # Score
    score_text = font.render("Score: " + str(score), True, BLACK)
    gameWindow.blit(score_text, (10, 10))


def check_collision():
    bird_rect = pygame.Rect(
        bird_x - bird_radius,
        bird_y - bird_radius,
        bird_radius * 2,
        bird_radius * 2
    )

    top_pipe = pygame.Rect(pipe_x, 0, pipe_width, pipe_height)
    bottom_pipe = pygame.Rect(
        pipe_x,
        pipe_height + pipe_gap,
        pipe_width,
        HEIGHT
    )

    if bird_rect.colliderect(top_pipe) or bird_rect.colliderect(bottom_pipe):
        return True

    if bird_y <= 0 or bird_y >= HEIGHT:
        return True

    return False


def show_message(text):
    msg = big_font.render(text, True, BLACK)
    gameWindow.blit(
        msg,
        (WIDTH // 2 - msg.get_width() // 2,
         HEIGHT // 2 - msg.get_height() // 2)
    )
    pygame.display.update()


# ---------------- MAIN LOOP ----------------
while True:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over:
                bird_velocity = jump_strength

            if event.key == pygame.K_RETURN and game_over:
                # Restart game
                bird_y = HEIGHT // 2
                bird_velocity = 0
                pipe_x = WIDTH
                pipe_height = random.randint(150, 400)
                score = 0
                game_over = False

    if not game_over:
        # Bird movement
        bird_velocity += gravity
        bird_y += bird_velocity

        # Pipe movement
        pipe_x -= pipe_speed

        if pipe_x + pipe_width < 0:
            pipe_x = WIDTH
            pipe_height = random.randint(150, 400)
            score += 1

        # Collision
        if check_collision():
            game_over = True

        draw_window()

    else:
        gameWindow.fill(BLUE)
        show_message("GAME OVER")
        restart_text = font.render("Press ENTER", True, BLACK)
        gameWindow.blit(restart_text, (WIDTH // 2 - 80, HEIGHT // 2 + 40))

    pygame.display.update()
