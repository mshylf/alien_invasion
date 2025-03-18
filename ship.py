import pygame
# 在这个类中，我们将把飞船和屏幕作为矩形进行处理。

class Ship:
    """管理飞船的类"""
    # ai_game接收当前 AlienInvasion 实例的引用，即在ai文件中Ship(self)
    def __init__(self, ai_game):
        """初始化设置及其初始位置"""

        # 获取屏幕对象及其位置信息
        self.screen = ai_game.screen
        # 获取游戏主窗口（Surface 对象）的矩形区域，
        # 并将该矩形保存到 Ship 类的属性 self.screen_rect 中。
        # pygame.Rect 对象表示包含了屏幕的位置和尺寸信息，可以方便地用来对齐或定位飞船相对于屏幕的位置。
        self.screen_rect = ai_game.screen.get_rect()

        # 加载飞船图像并获取其外接矩形
        # 为self.image赋予加载图形的surface对象
        self.image = pygame.image.load('images/fight_plane.bmp')
        # 注：此处之后可以自定义
        self.rect = self.image.get_rect()

        # 新飞船初始位置为屏幕中央
        self.rect.midbottom = self.screen_rect.midbottom

        # 原点(0, 0)位于屏幕的左上角，当一个点向右下方移动时，它的坐标值将增大。
        # 在处理 rect 对象时，可使用矩形的四个角及中心的 x 坐标和 y 坐标，通过设置这些值来指定矩形的位置。
        # 如果要将游戏元素居中，可设置相应 rect 对象的属性 center、centerx 或 centery；
        # 要让游戏元素与屏幕边缘对齐，可设置属性 top、bottom、left 或 right。
        # 还有一些组合属性，如 midbottom、midtop、midleft 和 midright

    def blitme(self):
        """在指定位置画飞船"""
        self.screen.blit(self.image,self.rect)