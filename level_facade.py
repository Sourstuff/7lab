import os

class LevelFacade:
    def __init__(self, current_dir):
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
        self.block_width = 70  
        self.block_height = 20 
        self.platform_width = 100
        self.platform_height = 20
        self.platform_x = (800 - self.platform_width) // 2
        self.platform_y = 600 - self.platform_height - 10
        self.ball_radius = 10
        self.ball_x = 800 // 2
        self.ball_y = 600 // 2
        self.ball_dx = 0
        self.ball_dy = 0

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
                x = col * (self.block_width + 5)  
                y = row * (self.block_height + 5)  
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

