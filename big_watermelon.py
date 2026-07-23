import pygame
import random
import math
import os

# 自动创建图片文件夹
if not os.path.exists("fruit_img"):
    os.mkdir("fruit_img")

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("合成大西瓜")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

# 对应1-9级水果颜色
fruit_color_list = [
    (255, 30, 30),  # 0 樱桃
    (255, 60, 80),  # 1 草莓
    (120, 30, 160),  # 2 葡萄
    (255, 140, 0),  # 3 橘子
    (255, 220, 0),  # 4 柠檬
    (80, 160, 30),  # 5 猕猴桃
    (255, 40, 20),  # 6 番茄
    (255, 120, 130),  # 7 桃子
    (255, 200, 0),  # 8 菠萝
    (30, 180, 60),  # 9 西瓜
]

FRUIT_TYPES = [
    {"radius": 15, "score": 1},
    {"radius": 20, "score": 2},
    {"radius": 25, "score": 3},
    {"radius": 30, "score": 4},
    {"radius": 35, "score": 5},
    {"radius": 40, "score": 6},
    {"radius": 45, "score": 7},
    {"radius": 50, "score": 8},
    {"radius": 55, "score": 9},
    {"radius": 60, "score": 10},
]

# 自动生成水果图片文件
for i in range(10):
    r = FRUIT_TYPES[i]["radius"]
    surf = pygame.Surface((r * 2, r * 2), pygame.SRCALPHA)
    pygame.draw.circle(surf, fruit_color_list[i], (r, r), r)
    pygame.draw.circle(surf, (255, 255, 255), (int(r * 0.7), int(r * 0.7)), r // 4)
    pygame.image.save(surf, f"fruit_img/{i}.png")

# 加载生成好的图片
fruit_images = []
for i in range(10):
    img_path = os.path.join("fruit_img", f"{i}.png")
    img = pygame.image.load(img_path).convert_alpha()
    r = FRUIT_TYPES[i]["radius"]
    img = pygame.transform.scale(img, (r * 2, r * 2))
    fruit_images.append(img)


class Fruit:
    def __init__(self, x, y, level):
        self.x = x
        self.y = y
        self.level = level
        self.radius = FRUIT_TYPES[level]["radius"]
        self.vx = 0
        self.vy = 0
        self.mass = self.radius ** 2
        self.is_merged = False

    def draw(self):
        img = fruit_images[self.level]
        screen.blit(img, (self.x - self.radius, self.y - self.radius))

    def update(self, gravity=0.5, damping=0.98):
        self.vy += gravity
        self.vx *= damping
        self.vy *= damping
        self.x += self.vx
        self.y += self.vy

        if self.x - self.radius < 0:
            self.x = self.radius
            self.vx *= -0.8
        if self.x + self.radius > WIDTH:
            self.x = WIDTH - self.radius
            self.vx *= -0.8
        if self.y + self.radius > HEIGHT:
            self.y = HEIGHT - self.radius
            self.vy *= -0.6
            self.vx *= 0.9


def check_collision(f1, f2):
    dx = f2.x - f1.x
    dy = f2.y - f1.y
    distance = math.hypot(dx, dy)
    min_dist = f1.radius + f2.radius
    if distance < min_dist and distance > 0:
        angle = math.atan2(dy, dx)
        sin = math.sin(angle)
        cos = math.cos(angle)
        v1 = (f1.vx * cos + f1.vy * sin, -f1.vx * sin + f1.vy * cos)
        v2 = (f2.vx * cos + f2.vy * sin, -f2.vx * sin + f2.vy * cos)
        m1 = f1.mass
        m2 = f2.mass
        v1_new = ((m1 - m2) * v1[0] + 2 * m2 * v2[0]) / (m1 + m2)
        v2_new = ((m2 - m1) * v2[0] + 2 * m1 * v1[0]) / (m1 + m2)
        f1.vx = v1_new * cos - v1[1] * sin
        f1.vy = v1_new * sin + v1[1] * cos
        f2.vx = v2_new * cos - v2[1] * sin
        f2.vy = v2_new * sin + v2[1] * cos
        overlap = min_dist - distance
        f1.x -= overlap * cos * 0.5
        f1.y -= overlap * sin * 0.5
        f2.x += overlap * cos * 0.5
        f2.y += overlap * sin * 0.5
        if f1.level == f2.level and f1.level < 9:
            f1.is_merged = True
            f2.is_merged = True
            return True
    return False


def main():
    clock = pygame.time.Clock()
    running = True
    game_over = False
    fruits = []
    score = 0
    spawn_x = WIDTH // 2
    next_fruit_level = random.randint(0, 3)

    # 使用默认字体，避免中文乱码
    font = pygame.font.Font(None, 36)
    gameover_font = pygame.font.Font(None, 72)

    while running:
        screen.fill(WHITE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if not game_over and event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    # ✅ 修复：把生成位置从 y=50 改为 y=100，避免刚生成就触发游戏结束
                    new_fruit = Fruit(spawn_x, 100, next_fruit_level)
                    fruits.append(new_fruit)
                    next_fruit_level = random.randint(0, 3)
            if event.type == pygame.MOUSEMOTION:
                spawn_x = event.pos[0]

        if not game_over:
            for fruit in fruits:
                fruit.update()
                # ✅ 修复：把游戏结束判定从 y<80 改为 y<50，更合理
                if fruit.y < 50:
                    game_over = True

            merge_pairs = []
            for i in range(len(fruits)):
                for j in range(i + 1, len(fruits)):
                    if check_collision(fruits[i], fruits[j]):
                        merge_pairs.append((i, j))

            for i, j in reversed(merge_pairs):
                f1 = fruits[i]
                f2 = fruits[j]
                if f1.is_merged and f2.is_merged:
                    new_level = f1.level + 1
                    new_x = (f1.x + f2.x) / 2
                    new_y = (f1.y + f2.y) / 2
                    new_fruit = Fruit(new_x, new_y, new_level)
                    new_fruit.vx = (f1.vx + f2.vx) / 2
                    new_fruit.vy = (f1.vy + f2.vy) / 2
                    fruits.append(new_fruit)
                    score += FRUIT_TYPES[new_level]["score"] * 2
                    del fruits[j]
                    del fruits[i]

        # 绘制画面元素
        for fruit in fruits:
            fruit.draw()
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))
        next_fruit = Fruit(WIDTH - 50, 30, next_fruit_level)
        next_fruit.draw()
        hint_text = font.render("Next:", True, BLACK)
        screen.blit(hint_text, (WIDTH - 120, 20))
        pygame.draw.line(screen, GRAY, (spawn_x, 0), (spawn_x, 100), 2)
        # ✅ 同步更新警戒线位置到 y=50
        pygame.draw.line(screen, (255, 0, 0), (0, 50), (WIDTH, 50), 2)

        if game_over:
            over_text = gameover_font.render("Game Over", True, (255, 0, 0))
            screen.blit(over_text, (WIDTH // 2 - 120, HEIGHT // 2))

        pygame.display.flip()
        clock.tick(60)
    pygame.quit()


if __name__ == "__main__":
    main()