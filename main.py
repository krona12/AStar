import pygame
from queue import PriorityQueue

# 初始化 Pygame
pygame.init()

# 设置窗口大小
WIDTH, HEIGHT = 600, 400
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("A* Pathfinding Visualization")

# 颜色定义
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
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

class Node:
    def __init__(self, position, parent=None):
        self.position = position
        self.parent = parent
        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position

    def __hash__(self):
        return hash(self.position)

    def __lt__(self, other):
        return self.f < other.f


def heuristic(a, b):
    x1, y1 = a
    x2, y2 = b
    return abs(x1 - x2) + abs(y1 - y2)

def astar(grid, start, end):
    start_node = Node(start)
    end_node = Node(end)

    open_set = PriorityQueue()
    open_set.put((0, start_node))
    came_from = {}

    g_score = {start_node: 0}
    f_score = {start_node: heuristic(start_node.position, end_node.position)}

    open_set_hash = {start_node}

    while not open_set.empty():
        current_node = open_set.get()[1]
        open_set_hash.remove(current_node)

        if current_node == end_node:
            path = []
            while current_node:
                path.append(current_node.position)
                current_node = current_node.parent
            return path[::-1]

        for new_position in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])
            neighbor = Node(node_position, current_node)

            if 0 <= node_position[0] < ROWS and 0 <= node_position[1] < COLS and grid[node_position[0]][node_position[1]] != 3:
                temp_g_score = g_score[current_node] + 1

                if temp_g_score < g_score.get(neighbor, float("inf")):
                    came_from[neighbor] = current_node
                    g_score[neighbor] = temp_g_score
                    f_score[neighbor] = temp_g_score + heuristic(node_position, end_node.position)
                    if neighbor not in open_set_hash:
                        open_set.put((f_score[neighbor], neighbor))
                        open_set_hash.add(neighbor)

    return []

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
            elif grid[row][col] == 4:
                color = YELLOW
            pygame.draw.rect(WIN, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            pygame.draw.rect(WIN, GRAY, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 1)

def draw_sidebar():
    pygame.draw.rect(WIN, WHITE, (WIDTH - 100, 0, 100, HEIGHT))
    WIN.blit(button_text, button_rect)

def draw():
    WIN.fill(BLACK)
    draw_grid()
    draw_sidebar()
    pygame.display.update()

def main():
    start = None
    end = None
    map_setup_done = False
    path = []
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
                    if start and end:
                        path = astar(grid, start, end)
                else:
                    row, col = pos[1] // SQUARE_SIZE, pos[0] // SQUARE_SIZE
                    if not start and grid[row][col] == 0:
                        start = (row, col)
                        grid[row][col] = 1
                    elif not end and grid[row][col] == 0:
                        end = (row, col)
                        grid[row][col] = 2
                    elif grid[row][col] == 0:
                        grid[row][col] = 3

        if map_setup_done and path:
            for position in path:
                if position != start and position != end:
                    grid[position[0]][position[1]] = 4
                    draw()
                    pygame.time.delay(1000)  # 1格/s 的速度显示路径

    pygame.quit()

main()
