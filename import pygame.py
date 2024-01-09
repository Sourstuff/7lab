import pygame
import random
import os


current_dir = os.path.dirname(os.path.abspath(__file__))

class LevelFacade:
    def __init__(self, current_dir):
        self.current_dir = current_dir
        self.current_dir = current_dir
        self.levels = []
        for level_file in ["level_1.txt", "level_2.txt", "level_3.txt", "level_4.txt", "level_5.txt"]:
            level_path = os.path.join(self.current_dir, level_file)
            with open(level_path, "r") as file:
                score_threshold = int(file.readline())
            self.levels.append({"file": level_path, "score_threshold": score_threshold})
        self.current_level = 0
        self.blocks_count = 0
        self.score_threshold = 0
        self.blocks = []

    def load_level(self, file_path):
        with open(file_path, "r") as file:
            lines = file.readlines()
            level = [line.split() for line in lines]
        return level

    def create_blocks_from_level(self, level):
        blocks = []
        rows = len(level)
        cols = len(level[0])
        for row in range(rows):
            for col in range(cols):
                x = col * (block_width + 5)
                y = row * (block_height + 5)
                if level[row][col] == "R":
                    color = (255, 0, 0)  # Красный блок
                elif level[row][col] == "Y":
                    color = (255, 255, 0)  # Жёлтый блок
                elif level[row][col] == "G":
                    color = (0, 255, 0)  # Зелёный блок
                else:
                    continue  
                hp = 1  
                blocks.append([x, y, color, hp])
        return blocks

    def setup_level(self):
        self.blocks.clear()
        level_file = self.levels[self.current_level]["file"]
        level_score_threshold = self.levels[self.current_level]["score_threshold"]
        self.score_threshold = level_score_threshold
        level = self.load_level(level_file)
        self.blocks = self.create_blocks_from_level(level)
        self.blocks_count = len(self.blocks)

pygame.init()

screen_width = 800
screen_height = 600

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Арканоид")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

platform_width = 100
platform_height = 20
platform_x = (screen_width - platform_width) // 2
platform_y = screen_height - platform_height - 10

ball_radius = 10
ball_x = screen_width // 2
ball_y = screen_height // 2
ball_dx = random.choice([-3, 3]) 
ball_dy = -3

block_width = 70
block_height = 20
blocks = []

current_level = 0
blocks_count = 0
score_threshold = 0


# Определение флагов для проверки состояния игры
game_over = False
bonus_active = False
bonus_timer = 10  # Время активации бонуса в секундах
bonus_start_time = None  # Время начала активации бонуса

# Переменные для системы уровней
score = 0

# Таблица рекордов
high_scores = [0] * 5  # Максимальное количество рекордов

clock = pygame.time.Clock()

# Главный игровой цикл
while not game_over:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

    # Обновление состояния платформы
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        platform_x -= 5
    if keys[pygame.K_RIGHT]:
        platform_x += 5

    if platform_x < 0:
        platform_x = 0
    elif platform_x > screen_width - platform_width:
        platform_x = screen_width - platform_width

    # Обновление состояния мяча
    ball_x += ball_dx
    ball_y += ball_dy

    # Обработка столкновений мяча со стенами
    if ball_x < ball_radius or ball_x > screen_width - ball_radius:
        ball_dx = -ball_dx
    if ball_y < ball_radius:
        ball_dy = -ball_dy

    # Обработка столкновений мяча с платформой
    if ball_y + ball_radius >= platform_y and ball_y - ball_radius <= platform_y + platform_height:
        if platform_x - ball_radius <= ball_x <= platform_x + platform_width + ball_radius:
            ball_dy = -ball_dy

    # Обработка столкновений мяча с блоками
    for block in blocks:
        block_x, block_y, block_color, block_hp = block

        if block_hp > 0:
            if block_x - ball_radius <= ball_x <= block_x + block_width + ball_radius and block_y - ball_radius <= ball_y <= block_y + block_height + ball_radius:
                if block_color == (255, 255, 0):  
                    score += 10  
                if block_color == (0, 255, 0):  
                    bonus_active = True
                    bonus_start_time = pygame.time.get_ticks() / 1000  # Получаем время в секундах
                    blocks.remove(block)
                    score += 50  # Прибавляем очки за бонус
                    continue
                elif bonus_active:  # Проверка активности бонуса
                    blocks.remove(block)
                    score += 10  # Прибавляем очки за каждое попадание
                    if block_color == (255, 255, 0):  # Проверка наличия жёлтого блока (за него начисляются больше очков)
                     score += 10  # Прибавляем 20 очков за жёлтый блок
                else:
                    block_hp -= 1
                    if block_hp == 0:
                        blocks.remove(block)
                    ball_dy = -ball_dy
                    score += 10  # Прибавляем очки за каждое попадание


    if ball_y > screen_height:
        game_over = True

    screen.fill(BLACK)

    
    pygame.draw.rect(screen, WHITE, (platform_x, platform_y, platform_width, platform_height))
    pygame.draw.ellipse(screen, WHITE, (platform_x - ball_radius, platform_y - ball_radius, ball_radius * 2, ball_radius * 2))
    pygame.draw.ellipse(screen, WHITE, (platform_x + platform_width - ball_radius, platform_y - ball_radius, ball_radius * 2, ball_radius * 2))

    pygame.draw.circle(screen, BLUE, (int(ball_x), int(ball_y)), ball_radius)

    for block in blocks:
        block_x, block_y, block_color, block_hp = block
        pygame.draw.rect(screen, BLACK, (block_x, block_y, block_width, block_height), 2)  # Чёрный контур
        pygame.draw.rect(screen, block_color, (block_x + 2, block_y + 2, block_width - 4, block_height - 4))

    
    if bonus_active:
        bonus_elapsed_time = pygame.time.get_ticks() / 1000 - bonus_start_time
        bonus_remaining_time = max(0, bonus_timer - bonus_elapsed_time)
        font = pygame.font.Font(None, 36)
        text = font.render(f"Bonus: {int(bonus_remaining_time)}s", True, WHITE)
        screen.blit(text, (10, screen_height - 40))
        if bonus_elapsed_time >= bonus_timer:
            bonus_active = False  

    # Отрисовка счета и уровня
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, WHITE)
    level_text = font.render(f"Level: {current_level + 1}", True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (10, 50))

    # Обновление экрана
    pygame.display.flip()

    # Ограничение частоты кадров
    clock.tick(60)

# Проверка состояния игры
if game_over:
    # Проверка нового рекорда
    if score > max(high_scores):
        high_scores.append(score)
        high_scores.sort(reverse=True)
        high_scores = high_scores[:5]  

    print("High Scores:")
    for i, high_score in enumerate(high_scores, 1):
        print(f"{i}. {high_score}")

    pygame.time.wait(2000)  
    pygame.quit()
