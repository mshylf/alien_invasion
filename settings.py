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

        # 飞船设置
        self.ship_moving_speed = 5 

        # 子弹设置
        self.bullet_speed = 7.0
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60,60,60)
        # 屏幕上出现的总子弹数量
        self.bullet_allowed = 10

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