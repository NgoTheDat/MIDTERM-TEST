import random
import pygame
import time
import heapq
from collections import deque

# Kích thước mê cung và ô
n, m         = 10, 10        # số hàng, số cột nếu bạn muốn tự sinh
cell_size    = 30            # pixel / ô

# Màu RGB
GREEN       = (0, 255, 0)     # Start
RED         = (255, 0, 0)     # Goal
YELLOW      = (255, 255, 0)   # Frontier
LIGHT_GREY  = (160, 160, 160) # Visited
BLUE        = (0, 0, 255)     # Path
BLACK       = (0, 0, 0)       # Viền / chữ trên ô sáng
WHITE       = (255, 255, 255) # Nền ô trống / chữ trên ô tối

# Khởi tạo cửa sổ Pygame
pygame.init()
pygame.mixer.init()
WIDTH, HEIGHT = m * cell_size, n * cell_size
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Search Visualizer")




# ====== VẼ 1 Ô BẤT KỲ LÊN MÀN HÌNH ======
def draw_cell(x, y, maze):
    rect = pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size)
    font = pygame.font.SysFont(None, cell_size)
    text = WHITE
    if maze[y][x] == "S":
        color = GREEN    
    elif maze[y][x] == "G":
        color = RED
    else: 
        color = WHITE
        text = BLACK
    
    pygame.draw.rect(screen, color, rect)
    pygame.draw.rect(screen, BLACK, rect, 1)
    
    label = font.render(str(maze[y][x]), True, text)
    text_rect = label.get_rect(center=rect.center)
    screen.blit(label, text_rect)
    
    pygame.display.update()

# ====== SINH MÊ CUNG NGẪU NHIÊN (PRIM'S) ======
def maze_generation(start, goal, n, m, cell_size):

    maze = [[True for i in range (m)] for j in range(n)]
    visited = [[False for i in range(m)] for j in range(n)]
    
    frontier = []
    
    def add_frontier(x, y):
        for i in range(4):
            dx = x + [2,0,-2,0][i]
            dy = y + [0,2,0,-2][i]
            if 0 <= dy < n and 0 <= dx < m and not visited[dy][dx]:
                frontier.append((x, y, dx, dy))
    
    def ensure_goal_path(x, y):
        for i in range(4):
            dx = x + [2,0,-2,0][i]
            dy = y + [0,2,0,-2][i]
            if 0 <= dy < n and 0 <= dx < m and not visited[dy][dx]:
                mx, my = (dx + x) // 2, (dy + y) // 2
                maze[my][mx] = random.randint(1, 9)
                visited[my][mx] = True
                draw_cell(mx, my, maze)
        
    (sx, sy) = start
    (gx, gy) = goal
    maze[sy][sx] = 'S'
    maze[gy][gx] = 'G'
    visited[sy][sx] = True
    visited[gy][gx] = True
    draw_cell(sx, sy, maze)        
    draw_cell(gx, gy, maze)
    
    ensure_goal_path(gx, gy)
    add_frontier(sx, sy)
    
    while frontier:
        (x, y, dx, dy) = random.choice(frontier)
        frontier.remove((x, y, dx, dy))
        if visited[dy][dx]:
            continue
        
        mx, my = (dx + x) // 2, (dy + y) // 2
        maze[my][mx] = random.randint(1, 9)
        maze[dy][dx] = random.randint(1, 9)
        
        visited[dy][dx] = True
        draw_cell(mx, my, maze)
        draw_cell(dx, dy, maze)
        add_frontier(dx, dy)

    return maze

# ====== VẼ MÊ CUNG CÓ SẴN ======
def draw_static_maze(screen, maze, cell_size):
    for y in range(len(maze)):
        for x in range(len(maze[0])):
            if maze[y][x] is not True:
                draw_cell(x, y, maze)




# ====== HÀM TIỆN VẼ (dùng cho BFS/DFS/UCS) ======
def color_cell(pos, color, cell_size, char=None):
    x, y = pos
    rect = pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size)
    pygame.draw.rect(screen, color, rect)
    if char:                           # vẽ lại ký hiệu nếu cần
        font = pygame.font.SysFont(None, cell_size)
        label = font.render(char, True, BLACK)
        screen.blit(label, label.get_rect(center=rect.center))
    pygame.draw.rect(screen, BLACK, rect, 1)  # viền
    pygame.display.update()

def bfs(maze, start, goal, cell_size):
    q = deque([start])
    came_from = {start: None}
    visited_set = set([start])
    frontier_color, visited_color, path_color = YELLOW, LIGHT_GREY, BLUE
    expanded_count = 0
    max_frontier_size = 1
    start_time = time.time()

    while q:
        pygame.event.pump()              
        current = q.popleft()
        expanded_count += 1
        max_frontier_size = max(max_frontier_size, len(q))
        
        if current not in (start, goal):
            color_cell(current, visited_color, cell_size, str(maze[current[1]][current[0]]))

        if current == goal:
            break

        x, y = current
        for dx, dy in [(1,0),(-1,0),(0,1),(0,-1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(maze[0]) and 0 <= ny < len(maze):
                if maze[ny][nx] is not True and (nx, ny) not in visited_set:
                    visited_set.add((nx, ny))
                    came_from[(nx, ny)] = current
                    q.append((nx, ny))
                    if (nx, ny) not in (start, goal):
                        color_cell((nx, ny), frontier_color, cell_size, str(maze[ny][nx]))  # frontier
        pygame.time.delay(100)  # tốc độ mô phỏng

    path_cost = 0
    node = goal
    while node and node != start:
        if node not in (start, goal):
            color_cell(node, path_color, cell_size, str(maze[node[1]][node[0]]))
            path_cost += int(maze[node[1]][node[0]])
        node = came_from.get(node)
        pygame.time.delay(15)
        
    end_time = time.time()
    execution_time = end_time - start_time
    
    print("\nBFS Statistics:")
    print(f"\tPath cost of the solution: {path_cost}")
    print(f"\tNumber of nodes expanded: {expanded_count}")
    print(f"\tMaximum size of the frontier: {max_frontier_size}")
    print(f"\tExecution time: {execution_time:.4f} seconds")

def ucs(maze, start, goal, cell_size):
    heap = [(0, start)]                       # (cost, node)
    came_from = {start: None}
    cost_so_far = {start: 0}
    visited_set = set()
    frontier_color, visited_color, path_color = YELLOW, LIGHT_GREY, BLUE
    expanded_count, max_frontier_size = 0, 1
    start_time = time.time()

    while heap:
        pygame.event.pump()
        current_cost, current = heapq.heappop(heap)
        if current in visited_set:            # bỏ node trùng
            continue
        visited_set.add(current)
        expanded_count += 1
        max_frontier_size = max(max_frontier_size, len(heap))

        if current not in (start, goal):
            color_cell(current, visited_color, cell_size, str(maze[current[1]][current[0]]))

        if current == goal:
            break

        x, y = current
        for dx, dy in [(1,0),(-1,0),(0,1),(0,-1)]:
            nx, ny = x+dx, y+dy
            if 0 <= nx < len(maze[0]) and 0 <= ny < len(maze):
                val = maze[ny][nx]
                if val is True:               # tường
                    continue

                # ---- cost của ô ----
                cost = 0 if val in ('S', 'G') else int(val)

                new_cost = cost_so_far[current] + cost
                next_node = (nx, ny)
                if next_node not in cost_so_far or new_cost < cost_so_far[next_node]:
                    cost_so_far[next_node] = new_cost
                    came_from[next_node] = current
                    heapq.heappush(heap, (new_cost, next_node))
                    if next_node not in (start, goal):
                        color_cell(next_node, frontier_color, cell_size, str(val))
        pygame.time.delay(50)

    # ---- tô đường đi ----
    path_cost = 0
    node = goal
    while node and node != start:
        if node not in (start, goal):
            val = maze[node[1]][node[0]]
            path_cost += int(val)             # val chắc chắn là số
            color_cell(node, path_color, cell_size, str(val))
        node = came_from.get(node)
        pygame.time.delay(15)

    exec_time = time.time() - start_time
    print("\nUCS Statistics:")
    print(f"\tPath cost of the solution: {path_cost}")
    print(f"\tNumber of nodes expanded: {expanded_count}")
    print(f"\tMaximum size of the frontier: {max_frontier_size}")
    print(f"\tExecution time: {exec_time:.4f} seconds")

def dfs(maze, start, goal, cell_size):
    stack = [start]
    came_from = {start: None}
    visited_set = set([start])
    frontier_color, visited_color, path_color = YELLOW, LIGHT_GREY, BLUE

    expanded_count = 0
    max_frontier_size = 1
    start_time = time.time()

    while stack:
        pygame.event.pump()
        current = stack.pop()

        if current not in (start, goal):
            color_cell(current, visited_color, cell_size, str(maze[current[1]][current[0]]))
        expanded_count += 1
        max_frontier_size = max(max_frontier_size, len(stack))

        if current == goal:
            break

        x, y = current
        for dx, dy in [(1,0),(-1,0),(0,1),(0,-1)]:
            nx, ny = x+dx, y+dy
            neighbor = (nx, ny)
            if 0 <= nx < len(maze[0]) and 0 <= ny < len(maze):
                if maze[ny][nx] is not True and neighbor not in visited_set:
                    visited_set.add(neighbor)
                    came_from[neighbor] = current
                    stack.append(neighbor)
                    if neighbor not in (start, goal):
                        color_cell(neighbor, frontier_color, cell_size, str(maze[ny][nx]))
        pygame.time.delay(100)

    path_cost = 0
    node = goal
    while node and node != start:
        if node not in (start, goal):
            color_cell(node, path_color, cell_size, str(maze[node[1]][node[0]]))
            path_cost += int(maze[node[1]][node[0]])
        node = came_from.get(node)
        pygame.time.delay(50)

    exec_time = time.time() - start_time
    print("\nDFS Statistics:")
    print(f"\tPath cost of the solution: {path_cost}")
    print(f"\tNumber of nodes expanded: {expanded_count}")
    print(f"\tMaximum size of the frontier: {max_frontier_size}")
    print(f"\tExecution time: {exec_time:.4f} seconds")




# ====== CHẠY TEST ======
if __name__ == "__main__": 
    # # TH1: Nếu tự tạo maze thì dùng hàm draw_static_maze(screen, maze, cell_size) và chạy thuật toán
    # maze = [
    #     ['S', 9,   True, 1,  1 ],
    #     [1,   1,   True, 9,  True],
    #     [True, 1,  1,    1,  1 ],
    #     [9,   True, True, 1, True],
    #     [1,   1,   1,   1,  'G']
    # ]
    # # Phải thay đổi start và goal phù hợp với maze đã tạo không thì sẽ lỗi thuật toán search
    # start, goal  = (0, 0), (4, 4)
    # draw_static_maze(screen, maze, cell_size)
    
    # bfs(maze, start, goal, cell_size)
    # screen.fill(BLACK)
    # draw_static_maze(screen, maze, cell_size)
    
    # pygame.time.delay(1000)
    # ucs(maze, start, goal, cell_size)
    # screen.fill(BLACK)
    # draw_static_maze(screen, maze, cell_size)
    
    # pygame.time.delay(1000)
    # dfs(maze, start, goal, cell_size)
    
    
    # TH2: Nếu dùng hàm maze_generation thì set start và goal vào vị trí mong muốn
    start, goal = (0, 0), (9, 9)
    maze = maze_generation(start,goal,n,m,cell_size)
    
    bfs(maze, start, goal, cell_size)
    screen.fill(BLACK)
    draw_static_maze(screen, maze, cell_size)
    
    pygame.time.delay(1000)
    ucs(maze, start, goal, cell_size)
    screen.fill(BLACK)
    draw_static_maze(screen, maze, cell_size)
    
    pygame.time.delay(1000)
    dfs(maze, start, goal, cell_size)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
    pygame.quit()