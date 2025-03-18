import pygame
class Middle_image:
    """将一张图片放到屏幕中央"""
    def __init__(self,ai_game):
        """初始化对象，位置"""
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect() 

        # 加载图片
        self.image = pygame.image.load('images/python.bmp')
        self.image_rect = self.image.get_rect()

        # 获取图片的原始宽度和高度
        original_width = self.image.get_width()
        original_height = self.image.get_height()

        # 设置目标宽度，并根据宽高比计算目标高度
        target_width = 200  # 目标宽度
        scale_factor = target_width / original_width  # 缩放比例
        target_height = int(original_height * scale_factor)  # 等比例计算高度

        # 调整图片大小
        self.image = pygame.transform.scale(self.image, (target_width, target_height))

        # 获取调整大小后的图片的矩形
        self.image_rect = self.image.get_rect()

        # 设置图片位置
        self.image_rect.center = self.screen_rect.center
    
    def blitme(self):
        """打印当前图像"""
        self.screen.blit(self.image,self.image_rect)