import sys
import math
import random
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QComboBox, QLabel

# 定义常量
WIDTH, HEIGHT = 950, 900  # 调整窗口大小
MAP_ROWS, MAP_COLS = 20, 20  # 初始地图大小
SQUARE_SIZE = 40
WHITE = QColor(255, 255, 255)
BLACK = QColor(0, 0, 0)
RED = QColor(255, 0, 0)
BLUE = QColor(0, 0, 255)
YELLOW = QColor(255, 255, 0)

class Node:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.g = 0
        self.h = 0
        self.f = 0
        self.parent = None
        self.state = 0  # 0表示空格，1表示起点，2表示终点，3表示障碍，4表示路径

class AStarVisualization(QWidget):
    def __init__(self):
        super().__init__()
        self.grid = [[Node(row, col) for col in range(MAP_COLS)] for row in range(MAP_ROWS)]
        self.start_node = None
        self.end_node = None
        self.path = []
        self.draw_state = 0  # 0表示绘制起点，1表示绘制终点，2表示绘制障碍
        self.heuristic = self.euclideanDistance  # 默认启发函数
        self.initUI()

    def initUI(self):
        self.setWindowTitle("A* Pathfinding Visualization")
        self.setFixedSize(WIDTH, HEIGHT)  # 调整窗口大小

        self.layout = QHBoxLayout()  # 使用水平布局管理器

        self.map_widget = QWidget()
        self.map_layout = QVBoxLayout()
        self.map_layout.setSpacing(0)
        self.map_layout.setContentsMargins(0, 0, 0, 0)
        self.map_widget.setLayout(self.map_layout)

        self.side_bar = QWidget()
        self.side_layout = QVBoxLayout()
        self.side_layout.setSpacing(0)
        self.side_layout.setContentsMargins(0, 0, 0, 0)
        self.side_bar.setLayout(self.side_layout)

        # 创建侧边栏按钮部件
        self.button_widget = QWidget()
        self.button_layout = QVBoxLayout()

        self.side_layout.setAlignment(Qt.AlignTop | Qt.AlignRight)  # 将侧边栏放置在右上角

        self.button_layout.setSpacing(0)
        self.button_layout.setContentsMargins(0, 0, 0, 0)
        self.button_widget.setLayout(self.button_layout)

        self.button_start = QPushButton("Start")
        self.button_start.clicked.connect(self.findPath)
        self.button_start.setFixedSize(80, 30)

        self.button_clear = QPushButton("Clear")
        self.button_clear.clicked.connect(self.clearGrid)
        self.button_clear.setFixedSize(80, 30)

        self.button_random = QPushButton("Random")
        self.button_random.clicked.connect(self.randomSetup)
        self.button_random.setFixedSize(80, 30)

        self.button_layout.addWidget(self.button_start)
        self.button_layout.addWidget(self.button_clear)
        self.button_layout.addWidget(self.button_random)

        # 添加下拉选项和标签到侧边栏
        self.combo_box_label = QLabel("Choose Heuristic:")
        self.combo_box = QComboBox()
        self.combo_box.addItem("Euclidean Distance")
        self.combo_box.addItem("Manhattan Distance")

        # 连接选择改变的信号到处理函数
        self.combo_box.currentIndexChanged.connect(self.updateHeuristic)

        self.side_layout.addWidget(self.combo_box_label)
        self.side_layout.addWidget(self.combo_box)
        self.side_layout.addWidget(self.button_widget)  # 将按钮部件添加到侧边栏

        self.layout.addWidget(self.map_widget)  # 放置地图部件在左侧
        self.layout.addWidget(self.side_bar)  # 放置侧边栏在右侧

        self.setLayout(self.layout)

        # 设置侧边栏的位置
        self.side_bar.setMaximumWidth(150)  # 设置最大宽度，可以根据需要调整

    def findPath(self):
        if self.start_node and self.end_node:
            open_list = [self.start_node]
            closed_list = []

            while open_list:
                current_node = min(open_list, key=lambda node: node.f)
                open_list.remove(current_node)
                closed_list.append(current_node)

                if current_node == self.end_node:
                    self.path = []
                    while current_node:
                        self.path.append(current_node)
                        current_node = current_node.parent
                    break

                neighbors = self.getNeighbors(current_node)
                for neighbor in neighbors:
                    if neighbor in closed_list:
                        continue

                    tentative_g = current_node.g + 1
                    if neighbor not in open_list or tentative_g < neighbor.g:
                        neighbor.g = tentative_g
                        neighbor.h = self.heuristic(neighbor, self.end_node)  # 使用所选的启发函数
                        neighbor.f = neighbor.g + neighbor.h
                        neighbor.parent = current_node
                        if neighbor not in open_list:
                            open_list.append(neighbor)

            self.update()

    def clearGrid(self):
        self.grid = [[Node(row, col) for col in range(MAP_COLS)] for row in range(MAP_ROWS)]
        self.start_node = None
        self.end_node = None
        self.path = []
        self.draw_state = 0
        self.update()

    def randomSetup(self):
        # 清除现有的起点、终点和障碍
        self.clearGrid()

        # 随机设置起点
        while True:
            row = random.randint(0, MAP_ROWS - 1)
            col = random.randint(0, MAP_COLS - 1)
            if self.grid[row][col].state == 0:
                self.grid[row][col].state = 1
                self.start_node = self.grid[row][col]
                break

        # 随机设置终点，确保不与起点重叠
        while True:
            row = random.randint(0, MAP_ROWS - 1)
            col = random.randint(0, MAP_COLS - 1)
            if self.grid[row][col].state == 0:
                self.grid[row][col].state = 2
                self.end_node = self.grid[row][col]
                break

        # 在计算路径前，先随机设置障碍，确保存在解
        while True:
            temp_grid = [[node.state for node in row] for row in self.grid]
            num_obstacles = MAP_ROWS * MAP_COLS // 2
            for _ in range(num_obstacles):
                row = random.randint(0, MAP_ROWS - 1)
                col = random.randint(0, MAP_COLS - 1)
                if temp_grid[row][col] == 0 and not (row == self.start_node.row and col == self.start_node.col) and not (row == self.end_node.row and col == self.end_node.col):
                    temp_grid[row][col] = 3
                else:
                    continue

            # 使用A*算法检查是否存在路径
            open_list = [self.start_node]
            closed_list = []

            while open_list:
                current_node = min(open_list, key=lambda node: node.f)
                open_list.remove(current_node)
                closed_list.append(current_node)

                if current_node == self.end_node:
                    break

                neighbors = self.getNeighbors(current_node)
                for neighbor in neighbors:
                    if neighbor in closed_list:
                        continue

                    if temp_grid[neighbor.row][neighbor.col] != 3:
                        if neighbor not in open_list:
                            open_list.append(neighbor)

            if self.end_node in closed_list:
                for row in range(MAP_ROWS):
                    for col in range(MAP_COLS):
                        self.grid[row][col].state = temp_grid[row][col]
                self.draw_state = 0
                break

        self.update()

    def getNeighbors(self, node):
        neighbors = []
        row, col = node.row, node.col
        if row > 0:
            neighbors.append(self.grid[row - 1][col])
        if row < MAP_ROWS - 1:
            neighbors.append(self.grid[row + 1][col])
        if col > 0:
            neighbors.append(self.grid[row][col - 1])
        if col < MAP_COLS - 1:
            neighbors.append(self.grid[row][col + 1])
        return [neighbor for neighbor in neighbors if neighbor.state != 3]

    def euclideanDistance(self, node1, node2):
        dx = node1.col - node2.col
        dy = node1.row - node2.row
        return math.sqrt(dx * dx + dy * dy)

    def manhattanDistance(self, node1, node2):
        return abs(node1.row - node2.row) + abs(node1.col - node2.col)

    def updateHeuristic(self, index):
        # 更新所选的启发函数
        if index == 0:
            self.heuristic = self.euclideanDistance
        elif index == 1:
            self.heuristic = self.manhattanDistance

    def mousePressEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            row = event.y() // SQUARE_SIZE
            col = event.x() // SQUARE_SIZE

            if self.draw_state == 0:  # 绘制起点
                if self.grid[row][col].state != 3:
                    self.grid[row][col].state = 1
                    self.start_node = self.grid[row][col]
                    self.draw_state = 1
            elif self.draw_state == 1:  # 绘制终点
                if self.grid[row][col].state != 3:
                    self.grid[row][col].state = 2
                    self.end_node = self.grid[row][col]
                    self.draw_state = 2
            elif self.draw_state == 2:  # 绘制障碍
                self.grid[row][col].state = 3
            self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        for row in range(MAP_ROWS):
            for col in range(MAP_COLS):
                node = self.grid[row][col]
                color = WHITE
                if node.state == 1:
                    color = BLUE
                elif node.state == 2:
                    color = RED
                elif node.state == 3:
                    color = BLACK
                elif node.state == 4:
                    color = YELLOW

                painter.fillRect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE, color)
                painter.drawRect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)

        # 绘制路径
        for node in self.path:
            painter.fillRect(node.col * SQUARE_SIZE, node.row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE, YELLOW)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Space:
            if self.draw_state == 2:  # 切换到绘制空格状态
                self.draw_state = 0

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QMainWindow()
    central_widget = AStarVisualization()
    window.setCentralWidget(central_widget)
    window.show()
    sys.exit(app.exec_())
