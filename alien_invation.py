import sys
import pygame
from settings import Settings
from ship import Ship
from Middle_image_test import Middle_image
from bullet import Bullet
# 使用pygame图形界面，sys中的工具退出游戏
# Pygame 之所以高效，是因为它让你能够把所有的游戏元素当作矩形（rect 对象）来处理，即便它们的形状并非矩形也一样。

class AlienInvasion:
    """管理游戏资源和行为的类"""

    def __init__(self):
        """初始化游戏并创建游戏资源"""
        # 初始化背景
        pygame.init()

        # 将各种引入类实例化，并赋值给控制函数的属性
        self.settings = Settings()

        # 在 Pygame 中，surface 是屏幕的一部分，用于显示游戏元素。
        # 调用 pygame.display.set_mode()创建一个显示窗口的surface
        # 将这个显示窗口赋给属性 self.screen，让这个类的所有方法都能够使用它。
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_hight))
        # 设置窗口标题
        pygame.display.set_caption("Alien Invasion")

        # 初始化中属性是有顺序的
        # 因此，必须确保先定义好会被其他对象依赖的属性，再创建依赖这些属性的对象。
        # 不能放到self.screen定义前，在Ship中要使用这个对象
        self.ship = Ship(self)
        #self.middle_image = Middle_image(self)
        # 创建用于存储子弹的编组：
        self.buttles = pygame.sprite.Group()

        # 设置时钟控制帧率,确保它在主循环每次通过后都进行计时（tick）。
        # 当这个循环的通过速度超过我们定义的帧率时，
        # Pygame 会计算需要暂停多长时间，以便游戏的运行速度保持一致。
        self.clock = pygame.time.Clock()

    def run_game(self):
        """开始游戏的主循环"""
        # while中是一个事件循环
        while True:
            # 获取事件信息
            self._check_events()
            # 根据移动标志计算更新飞船的位置
            self.ship.update()
            # 计算更新每颗子弹的位置，并删除已消失的子弹
            self._update_bullets()
            # 绘制图像并更新屏幕
            self._update_screen()
            # tick() 方法接受一个参数：游戏的帧率。
            # 方法会让循环暂停足够的时间，以使得循环总次数不超过 60 FPS（每秒 60 帧）
            self.clock.tick(60)
    
    # 约定以'_'开头的方法为辅助方法，一般只在类内调用
    def _check_events(self):
        """响应按键和鼠标事件"""
        # 侦听键盘和鼠标事件
        # pygame.event.get() 函数来访问 Pygame 检测到的事件。
        # 这个函数返回一个列表，其中包含它在上一次调用后发生的所有事件。
        for event in pygame.event.get():
            # 当玩家单击游戏窗口的关闭按钮时，
            # 将检测到 pygame.QUIT 事件，进而调用 sys.exit() 来退出游戏
            if event.type == pygame.QUIT:
                sys.exit()

            # 按下键盘
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)

            # 抬起按键            
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        """
        响应按下键盘事件
        """
        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
            self.ship.moving_left = True
        # 左shift+q退出，检查shife是否处于激活状态
        elif event.key ==  pygame.K_q and (event.mod & pygame.KMOD_LSHIFT):
            sys.exit()
        # 按空格发射子弹
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        """
        响应抬起键盘事件
        """
        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
            self.ship.moving_left = False

    # 按下空格后调用发射子弹
    def _fire_bullet(self):
        """创建一颗子弹，并将其加入编组bullets"""
        # 每个编组中的子弹都是一个Bullet类的实例
        # 将其加入编组后即为发射，在run函数中刷新位置

        # 限制屏幕中总子弹数量
        if len(self.buttles) < self.settings.bullet_allowed:
            new_bullet = Bullet(self)
            self.buttles.add(new_bullet)

    def _update_bullets(self):
        """更新子弹的位置，并删除已经消失的子弹"""
        # 在对编组调用update() 时，编组会自动对其中的每个精灵调用 update()，
        # 因此 self.bullets.update() 将为 bullets 编组中的每颗子弹调用 bullet.update()。
        # 向上移动每颗子弹
        self.buttles.update()
        # 在for语句执行过程中，python不允许改变列表的长度
        # 因此使用.copy方法创建一个副本进行循环，修改原列表的值
        for bullet in self.buttles.copy():
            if bullet.rect.bottom <= 0:
                self.buttles.remove(bullet)
       

    def _update_screen(self):
        """绘制图像更新屏幕内容"""
        # 绘制背景图片
        #self.screen.blit(self.settings.bg_image, (0, 0))

        # fill() 填充颜色，用于绘制 surface，只接受一个表示颜色的实参。
        # 每次循环时都重新绘制屏幕，是绘图操作(screen是整个窗口的Surface对象)
        self.screen.fill(self.settings.bg_color)

        # 绘制飞船
        self.ship.blitme()

        # 绘制子弹组
        # sprites()将精灵组的精灵转化为列表
        for bullet in self.buttles.sprites():
            bullet.draw_bullet()
        
        #self.middle_image.blitme()

        # 刷新整个显示窗口（Surface）的内容，会将绘制完成的所有画面一次性更新到屏幕上。
        # 每次执行 while 循环时都绘制一个空屏幕，并擦去旧屏幕，使得只有新的空屏幕可见
        pygame.display.flip()

if __name__ == '__main__':
    # 创建游戏实例并运行游戏
    ai = AlienInvasion()
    ai.run_game()