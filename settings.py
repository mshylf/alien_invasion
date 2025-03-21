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
        self.bg_image = pygame.image.load('images/bk_image.jpg')
        self.bg_image = self.pic_proportional_scaling(self.bg_image,self.screen_width)

        # 飞船图片加载
        self.ship_image = pygame.image.load('images/space-shuttle-2818717.png')
        # 飞船设置
        self.ship_moving_speed = 5 
        # 飞船总命数
        self.ship_limit = 1

        # 子弹设置
        self.bullet_speed = 7.0
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (255, 255, 0)
        # 屏幕上出现的总子弹数量
        self.bullet_allowed = 10

        # 外星人图片加载
        self.alien_image = pygame.image.load('images/ufo-4778062_1920.png')
        # 外星人飞船宽度设置
        self.alien_width = 130
        # 外星人x间隔设置
        self.alien_x_gap = self.alien_width*0.5
        self.alien_y_gap = 100
        self.alien_moving_speed = 2
        # 外星人向下的速度
        self.fleet_drop_speed = 100
        # fleet_direction为1表示向右移动，为-1表示向左移动
        self.fleet_direction = 1

        # 按钮设置

    def pic_proportional_scaling(self,image,target_width):
        """按给定的宽经行等比缩放"""
        # 获取图片的原始宽度和高度
        original_width = image.get_width()
        original_height = image.get_height()

        # 设置目标宽度，并根据宽高比计算目标高度
        # 目标宽度
        scale_factor = target_width / original_width  # 缩放比例
        target_height = int(original_height * scale_factor)  # 等比例计算高度

        # 调整图片大小
        image = pygame.transform.scale(image, (target_width, target_height))
        return image