import pygame
import random
import os

from level_facade import LevelFacade

class Game:
    def __init__(self):
        pygame.init()

        self.screen_width = 800
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Арканоид")

        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.BLUE = (0, 0, 255)

        self.platform_width = 100
        self.platform_height = 20
        self.platform_x = (self.screen_width - self.platform_width) // 2
        self.platform_y = self.screen_height - self.platform_height - 10

        self.ball_radius = 10
        self.ball_x = self.screen_width // 2
        self.ball_y = self.screen_height // 2
        self.ball_dx = random.choice([-3, 3])
        self.ball_dy = -3

        self.block_width = 70
        self.block_height = 20
        self.blocks = []

        self.current_level = 0
        self.blocks_count = 0
        self.score_threshold = 0

        self.level_facade = LevelFacade(os.path.dirname(os.path.abspath(__file__)))
        self.level_facade.setup_level()

        self.game_over = False
        self.bonus_active = False
        self.bonus_timer = 10
        self.bonus_start_time = None

        self.score = 0
        self.high_scores = [0] * 5

        self.clock = pygame.time.Clock()

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_over = True

    def update_platform(self, keys):
        if keys[pygame.K_LEFT]:
            self.level_facade.platform_x -= 5
        if keys[pygame.K_RIGHT]:
            self.level_facade.platform_x += 5

        if self.level_facade.platform_x < 0:
            self.level_facade.platform_x = 0
        elif self.level_facade.platform_x > self.screen_width - self.level_facade.platform_width:
            self.level_facade.platform_x = self.screen_width - self.level_facade.platform_width

    def update_ball(self):
        self.level_facade.ball_x += self.level_facade.ball_dx
        self.level_facade.ball_y += self.level_facade.ball_dy

        if self.level_facade.ball_x < self.level_facade.ball_radius or self.level_facade.ball_x > self.screen_width - self.level_facade.ball_radius:
            self.level_facade.ball_dx = -self.level_facade.ball_dx
        if self.level_facade.ball_y < self.level_facade.ball_radius:
            self.level_facade.ball_dy = -self.level_facade.ball_dy

        if (
            self.level_facade.ball_y + self.level_facade.ball_radius >= self.level_facade.platform_y
            and self.level_facade.ball_y - self.level_facade.ball_radius <= self.level_facade.platform_y + self.level_facade.platform_height
        ):
            if (
                self.level_facade.platform_x - self.level_facade.ball_radius <= self.level_facade.ball_x <= self.level_facade.platform_x + self.level_facade.platform_width + self.level_facade.ball_radius
            ):
                self.level_facade.ball_dy = -self.level_facade.ball_dy

    def update_bonus(self):
        for block in self.level_facade.blocks:
            block_x, block_y, block_color, block_hp = block

            if block_hp > 0:
                if (
                    block_x - self.level_facade.ball_radius <= self.level_facade.ball_x <= block_x + self.level_facade.block_width + self.level_facade.ball_radius
                    and block_y - self.level_facade.ball_radius <= self.level_facade.ball_y <= block_y + self.level_facade.block_height + self.level_facade.ball_radius
                ):
                    if block_color == (255, 255, 0):
                        self.score += 10
                    if block_color == (0, 255, 0):
                        self.bonus_active = True
                        self.bonus_start_time = pygame.time.get_ticks() / 1000
                        self.level_facade.blocks.remove(block)
                        self.score += 50
                        continue
                    elif self.bonus_active:
                        self.level_facade.blocks.remove(block)
                        self.score += 10
                        if block_color == (255, 255, 0):
                            self.score += 10
                    else:
                        block_hp -= 1
                        if block_hp == 0:
                            self.level_facade.blocks.remove(block)
                        self.level_facade.ball_dy = -self.level_facade.ball_dy
                        self.score += 10

    def draw_elements(self):
        self.screen.fill(self.BLACK)

        pygame.draw.rect(self.screen, self.WHITE, (self.level_facade.platform_x, self.level_facade.platform_y, self.level_facade.platform_width, self.level_facade.platform_height))
        pygame.draw.ellipse(self.screen, self.WHITE, (self.level_facade.platform_x - self.level_facade.ball_radius, self.level_facade.platform_y - self.level_facade.ball_radius, self.level_facade.ball_radius * 2, self.level_facade.ball_radius * 2))
        pygame.draw.ellipse(self.screen, self.WHITE, (self.level_facade.platform_x + self.level_facade.platform_width - self.level_facade.ball_radius, self.level_facade.platform_y - self.level_facade.ball_radius, self.level_facade.ball_radius * 2, self.level_facade.ball_radius * 2))

        pygame.draw.circle(self.screen, self.BLUE, (int(self.level_facade.ball_x), int(self.level_facade.ball_y)), self.level_facade.ball_radius)

        for block in self.level_facade.blocks:
            block_x, block_y, block_color, block_hp = block
            pygame.draw.rect(self.screen, self.BLACK, (block_x, block_y, self.level_facade.block_width, self.level_facade.block_height), 2)
            pygame.draw.rect(self.screen, block_color, (block_x + 2, block_y + 2, self.level_facade.block_width - 4, self.level_facade.block_height - 4))

        if self.bonus_active:
            bonus_elapsed_time = pygame.time.get_ticks() / 1000 - self.bonus_start_time
            bonus_remaining_time = max(0, self.bonus_timer - bonus_elapsed_time)
            font = pygame.font.Font(None, 36)
            text = font.render(f"Bonus: {int(bonus_remaining_time)}s", True, self.WHITE)
            self.screen.blit(text, (10, self.screen_height - 40))
            if bonus_elapsed_time >= self.bonus_timer:
                self.bonus_active = False

        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {self.score}", True, self.WHITE)
        level_text = font.render(f"Level: {self.level_facade.current_level + 1}", True, self.WHITE)
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(level_text, (10, 50))

        pygame.display.flip()

    def run(self):
        while not self.game_over:
            self.process_events()

            keys = pygame.key.get_pressed()
            self.update_platform(keys)
            self.update_ball()
            self.update_bonus()

            if self.level_facade.ball_y > self.screen_height:
                self.game_over = True

            if self.score >= self.level_facade.score_threshold:
                self.level_facade.current_level += 1
                if self.level_facade.current_level < len(self.level_facade.levels):
                    self.level_facade.setup_level()
                    self.score = 0
                else:
                    self.game_over = True

            self.draw_elements()

            self.clock.tick(60)

        if self.game_over:
            if self.score > max(self.high_scores):
                self.high_scores.append(self.score)
                self.high_scores.sort(reverse=True)
                self.high_scores = self.high_scores[:5]

            print("High Scores:")
            for i, high_score in enumerate(self.high_scores, 1):
                print(f"{i}. {high_score}")

            pygame.time.wait(2000)
            pygame.quit()
