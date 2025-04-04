import random

import pygame
import sys


# Constants
GRID_SIZE = 5
CELL_SIZE = 80  # Size of each grid cell
WINDOW_WIDTH = 500
WINDOW_HEIGHT = 600  # Extra space for color picker and timer

# Calculate grid dimensions
GRID_WIDTH = GRID_SIZE * CELL_SIZE
GRID_HEIGHT = GRID_SIZE * CELL_SIZE

# Calculate offsets to center the grid
grid_x_offset = (WINDOW_WIDTH - GRID_WIDTH) // 2
grid_y_offset = (WINDOW_HEIGHT - GRID_HEIGHT - 50) // 2  # Leave space for color picker leave space for the color picker


#WINDOW_SIZE = GRID_SIZE * CELL_SIZE + 50

#Four random colors at the start
COLORS = [(random.randint(0,255),random.randint(0,255), random.randint(0,255)),
          (random.randint(0,255),random.randint(0,255), random.randint(0,255)),
          (random.randint(0,255),random.randint(0,255), random.randint(0,255)),
          (random.randint(0,255),random.randint(0,255), random.randint(0,255))]

# Timer settings
TIMER_INITIAL = 30  # Starting time in seconds
TIMER_INCREMENT = 2  # Seconds added for each placed block
clock = pygame.time.Clock()

# Timer variables
timer = TIMER_INITIAL
last_tick_time = pygame.time.get_ticks()


# Pygame initialization
pygame.init()

# Creating a new window
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Color Fill Puzzle")


# Add scoring system and level-based timer carry-over
score = 0
level = 1


#Sound effect load
pygame.mixer.init()
game_over_sound = pygame.mixer.Sound("game-over-arcade-6435.mp3")
click_sound = pygame.mixer.Sound("D:\\Programming\\PyGame\\beep1.ogg")
# Initialize selected color
selected_color = None



def draw_score_and_level():
    """Display the current score and level on the screen."""
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    level_text = font.render(f"Level: {level}", True, (0, 0, 0))
    screen.blit(score_text, (10, 50))
    screen.blit(level_text, (WINDOW_WIDTH-100, 10))

def draw_color_picker():
    """Draw the color selection area at the bottom of the screen."""
    for i, color in enumerate(COLORS):
        color_rect = pygame.Rect(i * (WINDOW_WIDTH // len(COLORS)), WINDOW_HEIGHT - 50, WINDOW_WIDTH // len(COLORS), 50)
        pygame.draw.rect(screen, color, color_rect)
        pygame.draw.rect(screen, (0, 0, 0), color_rect, 1)  # Black border


def handle_click(pos):
    """Handle user clicking on a square to apply the selected color."""
    global selected_color, timer
    x, y = pos
    if y > WINDOW_HEIGHT - 50:  # Clicked in the color selection area
        selected_color_index = x // (WINDOW_WIDTH // len(COLORS))
        selected_color = COLORS[selected_color_index]
    else:  # Clicked on the grid
        click_sound.play()
        col = (x - grid_x_offset) // CELL_SIZE
        row = (y - grid_y_offset) // CELL_SIZE
        if 0 <= col < GRID_SIZE and 0 <= row < GRID_SIZE:  # Ensure click is within the grid
            if selected_color and grid[row][col] is None:
                grid[row][col] = selected_color
                if has_adjacent_match(row, col):
                    game_over_screen()  # End the game if an adjacent match is found
                else:
                    timer += 1  # Increase the timer

def has_adjacent_match(row, col):
    """Check if the placed square has the same color as any adjacent squares."""
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Top, bottom, left, right
    for dr, dc in directions:
        nr, nc = row + dr, col + dc
        if 0 <= nr < GRID_SIZE and 0 <= nc < GRID_SIZE:
            if grid[nr][nc] == grid[row][col]:  # Match with adjacent square
                return True
    return False

def update_timer():
    """Update the timer and check for timeout."""
    global timer, last_tick_time
    current_time = pygame.time.get_ticks()
    if current_time - last_tick_time >= 1000:  # 1 second
        timer -= 1
        last_tick_time = current_time

    # Display the timer on the screen
    font = pygame.font.Font(None, 36)
    timer_text = font.render(f"Time: {timer}s", True, (0, 0, 0))
    screen.blit(timer_text, (10, 10))

    # Check for timeout
    if timer <= 0:
        game_over_screen()

def reset_game():
    """Reset the game to its initial state."""
    global grid, timer, score, level, selected_color
    grid = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    initialize_random_blocks(num_blocks=5)  # Reinitialize the grid
    timer = TIMER_INITIAL  # Reset timer
    score = 0  # Reset score
    level = 1  # Reset level
    selected_color = None  # Reset selected color

def initialize_random_blocks(num_blocks=5):
    """Randomly initialize some blocks with valid colors."""
    for _ in range(num_blocks):
        while True:
            row = random.randint(0, GRID_SIZE - 1)
            col = random.randint(0, GRID_SIZE - 1)

            # Only place a color in an empty block
            if grid[row][col] is None:
                valid_colors = COLORS[:]

                # Remove colors of adjacent cells
                if row > 0 and grid[row - 1][col] in valid_colors:  # Above
                    valid_colors.remove(grid[row - 1][col])
                if col > 0 and grid[row][col - 1] in valid_colors:  # Left
                    valid_colors.remove(grid[row][col - 1])
                if row < GRID_SIZE - 1 and grid[row + 1][col] in valid_colors:  # Below
                    valid_colors.remove(grid[row + 1][col])
                if col < GRID_SIZE - 1 and grid[row][col + 1] in valid_colors:  # Right
                    valid_colors.remove(grid[row][col + 1])

                # Assign a random valid color to the block
                if valid_colors:
                    grid[row][col] = random.choice(valid_colors)
                    break


# Initialize the grid with random blocks
grid = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
initialize_random_blocks(num_blocks=5)

def draw_grid():
    """Draw the grid with the current block colors."""
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            x = grid_x_offset + col * CELL_SIZE
            y = grid_y_offset + row * CELL_SIZE
            rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
            color = grid[row][col] if grid[row][col] else (200, 200, 200)  # Light gray for empty cells
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, (0, 0, 0), rect, 1)  # Black border


def is_valid_color(row, col, color):
    """Checks if the color is a valid position"""
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up,down,left and right pos
    for dr, dc in directions:
        nr, nc = row + dr, col + dc
        if 0 <= nr < GRID_SIZE and 0 <= nc < GRID_SIZE and grid[nr][nc] == color:
            return False
    return True

def next_level():
    """Prepare for the next level by resetting the grid and increasing the difficulty."""
    global grid, timer, level
    grid = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    initialize_random_blocks(num_blocks=5 + level)  # Increase difficulty with more blocks
    level += 1

def check_victory():
    """Check if the player has successfully completed the level."""
    global score, timer
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if grid[row][col] is None or not is_valid_color(row, col, grid[row][col]):
                return False
    # Level completed: award points and move to next level
    score += 100 + timer  # Reward for remaining time
    next_level()
    return True

def check_game_over():
    """Check if there are any invalid moves on the board."""
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            color = grid[row][col]
            if color and not is_valid_color(row, col, color):
                return True
    return False


def game_over_screen():
    """Display a 'Game Over' screen and reset the game."""
    global grid, timer, score, level, selected_color
    game_over_sound.play()

    screen.fill((0, 0, 0))  # Black background
    font = pygame.font.Font(None, 74)
    text = font.render("Game Over!", True, (255, 0, 0))  # Red text
    screen.blit(text, (WINDOW_WIDTH // 4, WINDOW_HEIGHT // 3))
    final_score_text = font.render(f"Score: {score}", True, (255, 255, 255))  # White text
    screen.blit(final_score_text, (WINDOW_WIDTH // 4, WINDOW_HEIGHT // 3 + 80))
    pygame.display.flip()  # Update the display to show the message
    pygame.time.wait(1000)  # Wait for 1 second before restarting

def victory_screen():
    """Display a 'Victory' screen."""
    font = pygame.font.Font(None, 74)
    text = font.render("Level Up!", True, (random.randint(0, 255),
                                                             random.randint(0, 255),
                                                             random.randint(0, 255)))  # Randomly chosen color
    screen.blit(text, (WINDOW_WIDTH // 4, WINDOW_HEIGHT // 3))
    pygame.display.flip()
    pygame.time.wait(2000)


# Main Game
running = True
while running:
    screen.fill((255, 255, 255))  # White Background
    draw_grid()
    draw_color_picker()
    draw_score_and_level()
    update_timer()

    if check_game_over():
        game_over_screen()
        reset_game()

    if check_victory():
        victory_screen()

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            handle_click(event.pos)

    clock.tick(60)

pygame.quit()
