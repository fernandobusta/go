import pygame
import sys
from pygame.locals import QUIT, MOUSEBUTTONDOWN

# Constants
GRID_SIZE = 9
CELL_SIZE = 100
BUFFER_SIZE = 50  # Adjust this value based on your needs
WINDOW_SIZE = (GRID_SIZE * CELL_SIZE) + 2 * BUFFER_SIZE

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Initialize Pygame
pygame.init()

# Create the Pygame window
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("Go Game")


def draw_inter():
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            pygame.draw.line(screen, RED, (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE), (col * CELL_SIZE + CELL_SIZE // 2, (row + 1) * CELL_SIZE), 1)
            pygame.draw.line(screen, RED, (col * CELL_SIZE, row * CELL_SIZE + CELL_SIZE // 2), ((col + 1) * CELL_SIZE, row * CELL_SIZE + CELL_SIZE // 2), 1)


def place_black_dot(row, col):
    pygame.draw.circle(screen, BLACK, (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 2 - 2)
    print(f"Clicked on square at ({row}, {col})")

# Main game loop
clock = pygame.time.Clock()
screen.fill(WHITE)

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            clicked_row = mouse_pos[1] // CELL_SIZE
            clicked_col = mouse_pos[0] // CELL_SIZE
            place_black_dot(clicked_row, clicked_col)

    # Draw the board
    draw_inter()

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)