import pygame
from pygame.sprite import Sprite


# 在 pygame 中，“精灵”（Sprite）指的是游戏中可以独立存在和控制的对象，
# 比如角色、子弹、敌人等。它通常封装了图像、位置、运动行为等数据，
# 并提供更新和绘制自身的方法。
# “精灵组”（Sprite Group）则是管理多个精灵的容器。
# 使用精灵组可以方便地更新、绘制和检测精灵之间的碰撞，而不必逐个管理每个精灵。

# Sprite只有一个精灵组属性
class Bullet(Sprite):
    """子弹类"""
    def __init__(self, ai_game):
        """在飞船的当前位置创建一个子弹对象"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = ai_game.settings.bullet_color
        # 子弹并非基于图像文件的，因此必须使用 pygame.Rect() 类从头开始创建一个矩形。
        # 在（0，0）处创建一个表示子弹的矩形
        self.rect = pygame.Rect(0,0,self.settings.bullet_width,self.settings.bullet_height)
        # 子弹的顶端和飞船的顶端居中对齐,设置初始位置
        self.rect.midtop = ai_game.ship.rect.midtop
        # y坐标的值不断变化,存储用浮点数表示的子弹位置
        self.y = float(self.rect.y)

    def update(self):
        """向上移动子弹"""
        self.y -= self.settings.bullet_speed
        self.rect.y = self.y

    def draw_bullet(self):
        """绘制子弹"""
        pygame.draw.rect(self.screen,self.color,self.rect)