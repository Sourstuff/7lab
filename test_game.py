import unittest
from level_facade import LevelFacade

class TestGame(unittest.TestCase):

    def setUp(self):
  
        self.level_facade = LevelFacade("C:/Users/User/Desktop/арканоид/levels")

    def test_load_level(self):
      
        level = self.level_facade.load_level("C:/Users/User/Desktop/арканоид/levels/level_1.txt")
        self.assertEqual(len(level), 10)  

        level = [["R", "Y", "G"], ["G", "R", "Y"]]
        self.level_facade.block_width = 70
        self.level_facade.block_height = 20
        blocks = self.level_facade.create_blocks_from_level(level)
        self.assertEqual(len(blocks), 6)  
    def test_setup_level(self):
        self.level_facade.setup_level()
        self.assertEqual(len(self.level_facade.blocks), self.level_facade.blocks_count)
        self.assertEqual(self.level_facade.score_threshold, 200)  

 

if __name__ == '__main__':
    unittest.main()
