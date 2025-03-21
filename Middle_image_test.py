import pygame
from settings import Settings
class Middle_image:
    """将一张图片放到屏幕中央"""
    def __init__(self,ai_game):
        """初始化对象，位置"""
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect() 

        # 加载图片
        self.image = pygame.image.load('images/小女孩拿喇叭.bmp')
        self.image_rect = self.image.get_rect()

        self.image = Settings().pic_proportional_scaling(self.image,800)

        # 获取调整大小后的图片的矩形
        self.image_rect = self.image.get_rect()

        # 设置图片位置
        self.image_rect.center = self.screen_rect.center
    
    def blitme(self):
        """打印当前图像"""
        self.screen.blit(self.image,self.image_rect)