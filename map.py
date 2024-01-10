import pygame
import sys

# 初始化 Pygame
pygame.init()

# 设置窗口大小
WIDTH, HEIGHT = 600, 400
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("A* Pathfinding Visualization")

# 颜色定义
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)

# 网格大小
ROWS, COLS = 20, 30
SQUARE_SIZE = WIDTH // COLS

# 网格
grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]

# 按钮定义
button_font = pygame.font.SysFont(None, 30)
button_text = button_font.render('Finished', True, BLACK)
button_rect = button_text.get_rect(center=(WIDTH - 50, HEIGHT / 2))

def draw_grid():
    for row in range(ROWS):
        for col in range(COLS):
            color = WHITE
            if grid[row][col] == 1:
                color = BLUE
            elif grid[row][col] == 2:
                color = BLACK
            elif grid[row][col] == 3:
                color = RED
            pygame.draw.rect(WIN, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            pygame.draw.rect(WIN, GRAY, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 1)

def draw_sidebar():
    # 绘制侧边栏背景
    pygame.draw.rect(WIN, WHITE, (WIDTH - 100, 0, 100, HEIGHT))
    # 绘制按钮
    pygame.draw.rect(WIN, GRAY, button_rect)  # 按钮背景
    WIN.blit(button_text, button_rect)
def draw_button():
    pygame.draw.rect(WIN, WHITE, button_rect)
    WIN.blit(button_text, button_rect)

def draw():
    WIN.fill(BLACK)
    draw_grid()
    draw_button()
    draw_sidebar()
    pygame.display.update()

def main():
    start = None
    end = None
    map_setup_done = False
    run = True
    while run:
        draw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN and not map_setup_done:
                pos = pygame.mouse.get_pos()
                if button_rect.collidepoint(pos):
                    map_setup_done = True
                else:
                    row, col = pos[1] // SQUARE_SIZE, pos[0] // SQUARE_SIZE
                    if not start and grid[row][col] == 0:
                        start = (row, col)
                        grid[row][col] = 1  # Start
                    elif not end and grid[row][col] == 0:
                        end = (row, col)
                        grid[row][col] = 2  # End
                    elif grid[row][col] == 0:
                        grid[row][col] = 3  # Obstacle

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    # TODO: Start A* algorithm
                    pass

    pygame.quit()

main()
