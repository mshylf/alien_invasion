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
        # pygame.Rect 对象表示二维矩形区域，包含了屏幕的位置和尺寸信息，
        # 可以方便地用来对齐或定位飞船相对于屏幕的位置。
        self.screen_rect = ai_game.screen.get_rect()

        # 加载飞船图像并获取其外接矩形
        # 为self.image赋予加载图形的surface对象
        self.image = pygame.image.load('images/fight_plane.bmp')
        # 注：此处之后可以自定义

        # 设置使用主文件中的设置
        self.settings = ai_game.settings

        # 设置飞船大小
        self.image = self.settings.pic_proportional_scaling(self.image,100)

        self.rect = self.image.get_rect()

        # 新飞船初始位置为屏幕中央
        self.rect.midbottom = self.screen_rect.midbottom

        # 移动标志，只要为true就移动（按下连续移动）
        self.moving_right = False
        self.moving_left = False

        # 原点(0, 0)位于屏幕的左上角，当一个点向右下方移动时，它的坐标值将增大。
        # 在处理 rect 对象时，可使用矩形的四个角及中心的 x 坐标和 y 坐标，通过设置这些值来指定矩形的位置。
        # 如果要将游戏元素居中，可设置相应 rect 对象的属性 center、centerx 或 centery；
        # 要让游戏元素与屏幕边缘对齐，可设置属性 top、bottom、left 或 right。
        # 还有一些组合属性，如 midbottom、midtop、midleft 和 midright

    def update(self):
        """根据移动标志调整飞船的位置"""
        # 确定边界
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.rect.x += self.settings.ship_moving_speed
        if self.moving_left and self.rect.left > 0:
            self.rect.x -= self.settings.ship_moving_speed
        

    def blitme(self):
        """在指定位置画飞船"""
        self.screen.blit(self.image,self.rect)
