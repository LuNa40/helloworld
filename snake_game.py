import pygame
import random
import sys

# 初始化 pygame
pygame.init()

# 游戏常量
WIDTH, HEIGHT = 400, 400
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE
FPS = 10

# 颜色定义
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# 创建窗口
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("贪吃蛇游戏")
clock = pygame.time.Clock()

# 字体（用内置默认字体）
font = pygame.font.Font(None, 36)

def draw_snake(snake):
    """绘制蛇身"""
    for segment in snake:
        pygame.draw.rect(screen, GREEN, (segment[0]*GRID_SIZE, segment[1]*GRID_SIZE, GRID_SIZE-1, GRID_SIZE-1))

def draw_food(food):
    """绘制食物"""
    pygame.draw.rect(screen, RED, (food[0]*GRID_SIZE, food[1]*GRID_SIZE, GRID_SIZE-1, GRID_SIZE-1))

def show_score(score):
    """显示当前得分"""
    text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(text, (10, 10))

def show_pause():
    """显示暂停提示"""
    pause_text = font.render("PAUSED", True, WHITE)
    screen.blit(pause_text, (WIDTH//2 - 40, HEIGHT//2 - 20))

def main():
    # 初始化蛇：列表存储身体坐标，方向初始向右
    snake = [(GRID_WIDTH//2, GRID_HEIGHT//2)]
    direction = (1, 0)  # (dx, dy) → 右
    next_direction = direction

    # 随机生成食物
    def generate_food():
        while True:
            food = (random.randint(0, GRID_WIDTH-1), random.randint(0, GRID_HEIGHT-1))
            if food not in snake:
                return food
    food = generate_food()
    score = 0

    running = True
    paused = False  # 暂停状态

    while running:
        # 处理事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # 方向控制（防止180度转向）
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused  # 空格切换暂停/继续
                if not paused:  # 只有非暂停状态才响应方向键
                    if event.key == pygame.K_UP and direction != (0, 1):
                        next_direction = (0, -1)
                    elif event.key == pygame.K_DOWN and direction != (0, -1):
                        next_direction = (0, 1)
                    elif event.key == pygame.K_LEFT and direction != (1, 0):
                        next_direction = (-1, 0)
                    elif event.key == pygame.K_RIGHT and direction != (-1, 0):
                        next_direction = (1, 0)

        if not paused:  # 非暂停状态才更新游戏逻辑
            # 更新方向
            direction = next_direction

            # 计算新的蛇头位置
            head_x, head_y = snake[0]
            new_head = (head_x + direction[0], head_y + direction[1])

            # 碰撞检测：边界或自身
            if (new_head[0] < 0 or new_head[0] >= GRID_WIDTH or
                new_head[1] < 0 or new_head[1] >= GRID_HEIGHT or
                new_head in snake):
                running = False  # 游戏结束

            # 把新蛇头加入蛇身
            snake.insert(0, new_head)

            # 吃到食物：不删除尾部，生成新食物，加分
            if new_head == food:
                score += 10
                food = generate_food()
            else:
                # 没吃到食物：删除尾部
                snake.pop()

        # 绘制画面
        screen.fill(BLACK)
        draw_snake(snake)
        draw_food(food)
        show_score(score)
        if paused:
            show_pause()  # 暂停时显示提示
        pygame.display.flip()

        # 控制帧率
        clock.tick(FPS)

    # 游戏结束后显示最终得分
    game_over_text = font.render("Game Over!", True, WHITE)
    score_text = font.render(f"Final Score: {score}", True, WHITE)
    screen.blit(game_over_text, (WIDTH//2 - 70, HEIGHT//2 - 20))
    screen.blit(score_text, (WIDTH//2 - 70, HEIGHT//2 + 20))
    pygame.display.flip()

    # 等待2秒后退出
    pygame.time.wait(2000)
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()