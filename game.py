import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Constants
GRID_SIZE = 5
TILE_SIZE = 64
SCREEN_WIDTH = GRID_SIZE * TILE_SIZE  # 320
SCREEN_HEIGHT = GRID_SIZE * TILE_SIZE  # 320
FPS = 10

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (50, 50, 50)
ROSE = (255, 192, 203)

# Setup screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Cute Wumpus World")
clock = pygame.time.Clock()

# Game state
player_pos = [0, 0]
visited = [[False for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
game_over = False
showing_leaderboard = False
end_message = ""
points = 0
player_name = ""

# Load all player options
player_options = [
    pygame.image.load("assets/player1.png").convert_alpha(),
    pygame.image.load("assets/player2.png").convert_alpha(),
    pygame.image.load("assets/player3.png").convert_alpha(),
]

# Load other images
WUMPUS_IMG = pygame.image.load("assets/wumpus.png").convert_alpha()
GOLD_IMG = pygame.image.load("assets/gold.png").convert_alpha()
PIT_IMG = pygame.image.load("assets/pit.png").convert_alpha()
BREEZE_IMG = pygame.image.load("assets/breeze.png").convert_alpha()

# Resize all images to 64x64
for i in range(len(player_options)):
    player_options[i] = pygame.transform.scale(player_options[i], (64, 64))
WUMPUS_IMG = pygame.transform.scale(WUMPUS_IMG, (64, 64))
GOLD_IMG = pygame.transform.scale(GOLD_IMG, (64, 64))
PIT_IMG = pygame.transform.scale(PIT_IMG, (64, 64))
BREEZE_IMG = pygame.transform.scale(BREEZE_IMG, (64, 64))

# Temporary default, will be overwritten by chosen character
PLAYER_IMG = player_options[0]

def random_positions():
    positions = []
    while len(positions) < 3:
        pos = [random.randint(1, 4), random.randint(1, 4)]
        if pos not in positions:
            positions.append(pos)
    return positions

gold_pos, pit_pos, wumpus_pos = random_positions()

def show_start_screen():
    font = pygame.font.SysFont("Arial", 24)
    button_font = pygame.font.SysFont("Arial", 18)
    button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 60, SCREEN_HEIGHT // 2 - 25, 120, 40)

    while True:
        screen.fill(ROSE)
        title = font.render("Cute Wumpus World", True, (0, 0, 0))
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 100))

        pygame.draw.rect(screen, (255, 255, 255), button_rect)
        start_text = button_font.render("Start Game", True, (0, 0, 0))
        screen.blit(start_text, (button_rect.x + 20, button_rect.y + 10))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and button_rect.collidepoint(event.pos):
                return

def get_player_name():
    name = ""
    font = pygame.font.SysFont("Arial", 24)
    input_active = True

    while input_active:
        screen.fill((30, 30, 30))
        text = font.render("Enter Your Name:", True, (255, 255, 255))
        name_display = font.render(name + "|", True, (0, 255, 0))

        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 100))
        screen.blit(name_display, (SCREEN_WIDTH // 2 - name_display.get_width() // 2, 150))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                else:
                    name += event.unicode
    return name

def choose_character():
    choosing = True
    while choosing:
        screen.fill((30, 30, 30))
        font = pygame.font.SysFont("Arial", 16)
        text = font.render("Choose Your Character: Press 1, 2, or 3", True, (255, 255, 255))
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 20))

        for i, img in enumerate(player_options):
            screen.blit(img, (30 + i * 90, 80))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return player_options[0]
                elif event.key == pygame.K_2:
                    return player_options[1]
                elif event.key == pygame.K_3:
                    return player_options[2]

def draw_grid():
    for x in range(0, SCREEN_WIDTH, TILE_SIZE):
        pygame.draw.line(screen, WHITE, (x, 0), (x, SCREEN_HEIGHT))
    for y in range(0, SCREEN_HEIGHT, TILE_SIZE):
        pygame.draw.line(screen, WHITE, (0, y), (SCREEN_WIDTH, y))

def draw_entities():
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if visited[row][col]:
                pygame.draw.rect(screen, GRAY, (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            else:
                pygame.draw.rect(screen, BLACK, (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE))

    draw_grid()
    screen.blit(PLAYER_IMG, (player_pos[1] * TILE_SIZE, player_pos[0] * TILE_SIZE))

    if player_pos == gold_pos:
        screen.blit(GOLD_IMG, (gold_pos[1] * TILE_SIZE, gold_pos[0] * TILE_SIZE))
    if player_pos == pit_pos:
        screen.blit(PIT_IMG, (pit_pos[1] * TILE_SIZE, pit_pos[0] * TILE_SIZE))
    if player_pos == wumpus_pos:
        screen.blit(WUMPUS_IMG, (wumpus_pos[1] * TILE_SIZE, wumpus_pos[0] * TILE_SIZE))

    if abs(player_pos[0] - pit_pos[0]) + abs(player_pos[1] - pit_pos[1]) == 1:
        screen.blit(BREEZE_IMG, (player_pos[1] * TILE_SIZE, player_pos[0] * TILE_SIZE))

    if abs(player_pos[0] - wumpus_pos[0]) + abs(player_pos[1] - wumpus_pos[1]) == 1:
        screen.blit(BREEZE_IMG, (player_pos[1] * TILE_SIZE, player_pos[0] * TILE_SIZE))

    score_font = pygame.font.SysFont("Arial", 12)
    score_text = score_font.render(f"Points: {points}", True, (255, 255, 0))
    screen.blit(score_text, (10, 5))

def check_game_status():
    global end_message, points, game_over, showing_leaderboard

    if player_pos == gold_pos:
        points += 10
        end_message = f"🎉 You found the gold! +10 pts 😍 Total: {points} | Press R to Restart or L for Leaderboard"
        game_over = True
        with open("leaderboard.txt", "a") as f:
            f.write(f"{player_name}:{points}\n")

    elif player_pos == pit_pos:
        points -= 5
        end_message = f" You fell into a pit! 😢 -5 pts | Total: {points} | Press R to Restart or L for Leaderboard"
        game_over = True
        with open("leaderboard.txt", "a") as f:
            f.write(f"{player_name}:{points}\n")

    elif player_pos == wumpus_pos:
        points -= 5
        end_message = f" The Wumpus got you! 😖 -5 pts | Total: {points} | Press R to Restart or L for Leaderboard"
        game_over = True
        with open("leaderboard.txt", "a") as f:
            f.write(f"{player_name}:{points}\n")

def restart_game():
    global player_pos, gold_pos, pit_pos, wumpus_pos, visited, game_over, end_message, showing_leaderboard
    player_pos = [0, 0]
    visited = [[False for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    gold_pos, pit_pos, wumpus_pos = random_positions()
    game_over = False
    showing_leaderboard = False
    end_message = ""

def show_message(text):
    font = pygame.font.SysFont("Arial", 14)
    words = text.split(" ")
    lines = []
    current_line = ""

    for word in words:
        test_line = current_line + word + " "
        if font.size(test_line)[0] < SCREEN_WIDTH - 20:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word + " "
    lines.append(current_line)

    # Draw each line centered
    y = SCREEN_HEIGHT // 2 - (len(lines) * 10)
    for line in lines:
        rendered = font.render(line, True, WHITE)
        rect = rendered.get_rect(center=(SCREEN_WIDTH // 2, y))
        screen.blit(rendered, rect)
        y += 20


def show_leaderboard():
    screen.fill(BLACK)
    try:
        with open("leaderboard.txt", "r") as f:
            entries = [line.strip().split(":") for line in f]
            sorted_scores = sorted(entries, key=lambda x: int(x[1]), reverse=True)[:5]
    except:
        sorted_scores = []

    font = pygame.font.SysFont("Arial", 16)
    y_offset = 100
    title = font.render("🏆 Leaderboard:", True, (255, 215, 0))
    screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, y_offset))
    y_offset += 30

    for name, score in sorted_scores:
        score_line = font.render(f"{name}: {score} pts", True, (255, 255, 255))
        screen.blit(score_line, (SCREEN_WIDTH // 2 - score_line.get_width() // 2, y_offset))
        y_offset += 25

    back_msg = font.render("Press M to return to Menu", True, (200, 200, 200))
    screen.blit(back_msg, (SCREEN_WIDTH // 2 - back_msg.get_width() // 2, y_offset + 20))

# Run intro + character select
show_start_screen()
player_name = get_player_name()
PLAYER_IMG = choose_character()

# Main loop
while True:
    if showing_leaderboard:
        show_leaderboard()
    else:
        screen.fill(BLACK)
        draw_entities()
        visited[player_pos[0]][player_pos[1]] = True

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if showing_leaderboard:
                if event.key == pygame.K_m:
                    showing_leaderboard = False
            elif not game_over:
                if event.key == pygame.K_UP and player_pos[0] > 0:
                    player_pos[0] -= 1
                elif event.key == pygame.K_DOWN and player_pos[0] < GRID_SIZE - 1:
                    player_pos[0] += 1
                elif event.key == pygame.K_LEFT and player_pos[1] > 0:
                    player_pos[1] -= 1
                elif event.key == pygame.K_RIGHT and player_pos[1] < GRID_SIZE - 1:
                    player_pos[1] += 1
            else:
                if event.key == pygame.K_r:
                    restart_game()
                elif event.key == pygame.K_l:
                    showing_leaderboard = True

    if not game_over and not showing_leaderboard:
        check_game_status()
    elif game_over and not showing_leaderboard:
        show_message(end_message)

    pygame.display.flip()
    clock.tick(FPS)

