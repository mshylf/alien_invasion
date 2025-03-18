import pygame
# 在项目规模增大时，这还让游戏的外观和行为修改起来更加容易：
# 在settings.py 中修改一些相关的值即可，无须查找散布在项目中的各种设置。
class Settings:
    """存储游戏中所有设置的类"""
    def __init__(self):
        """初始化设置"""
        # 屏幕设置
        self.screen_width = 1200
        self.screen_hight = 800
        self.bg_color = (135, 206, 235)
        #self.bg_image = pygame.image.load('images/bk_image.jpg')
    