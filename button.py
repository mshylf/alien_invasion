import pygame.font
# 由于pygame中没有内置的按钮类，因此我们需要创建一个Button类，用于创建按钮。
# 创建一个带标签的实心矩形，可以使用这些代码来创建任意居中的按钮
class Button:
    """创建一个按钮类"""
    def __init__(self,ai_game,msg):
        """初始化按钮属性"""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        self.settings = ai_game.settings

        # 设置按钮的尺寸及其他属性
        self.width,self.height = 200,50
        self.button_color = (0,135,0)
        self.text_color = (255,255,255)
        self.font = pygame.font.SysFont(None,48)

        # 创建按钮的rect对象，并使其居中
        self.rect = pygame.Rect(0,0,self.width,self.height)
        self.rect.center = self.screen_rect.center

        self._prep_msg(msg)
        
    def _prep_msg(self,msg):
        """将msg渲染为图像，并使其在按钮中居中"""
        # font.render() 方法还接受一个布尔实参，该实参指定是否开启反锯齿功能（反锯齿让文本的边缘更平滑）
        self.msg_image = self.font.render(msg,True,self.text_color,self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        """绘制一个用颜色填充的按钮，再绘制文本"""
        # 调用 screen.fill() 来绘制表示按钮的矩形，
        # 再调用 screen.blit() 来向它传递一幅图像以及与该图像相关联的 rect，从而在屏幕上绘制文本图像。
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)