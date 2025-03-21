import pygame
from pygame.sprite import Sprite

# 定义单个外星人类,使用精灵组
class Alien(Sprite):
    """外星人类"""
    def __init__(self,ai_game):
        """初始化属性"""
        super().__init__()
        self.settings = ai_game.settings
        self.screen = ai_game.screen 
        self.image = self.settings.pic_proportional_scaling(self.settings.alien_image,self.settings.alien_width)
        self.rect = self.image.get_rect()
        # 最开始在左上角
        self.rect.x = 0
        self.rect.y = self.rect.height

        self.x = float(self.rect.x)
    
    def update(self):
        """移动外星人"""
        self.x += self.settings.alien_moving_speed * self.settings.fleet_direction
        self.rect.x = self.x
    


    def _check_edges(self):
        """检测是否达到边界,若到边界则返回True"""
        screen_rect = self.screen.get_rect()
        return (self.rect.right >= screen_rect.right) or (self.rect.left <= 0)