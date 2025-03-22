import sys
import pygame
import button
from settings import Settings
from ship import Ship
from Middle_image_test import Middle_image
from bullet import Bullet
from alien import Alien
from time import sleep
from game_stats import GameStats
from button import Button
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

        # 创建一个用于存储游戏统计信息的实例
        self.stats = GameStats(self)
        # 初始化中属性是有顺序的
        # 因此，必须确保先定义好会被其他对象依赖的属性，再创建依赖这些属性的对象。
        # 不能放到self.screen定义前，在Ship中要使用这个对象
        self.ship = Ship(self)
        #self.middle_image = Middle_image(self)
        # 创建用于存储子弹的精灵组：
        self.buttles = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._create_fleet()

        # 设置时钟控制帧率,确保它在主循环每次通过后都进行计时（tick）。
        # 当这个循环的通过速度超过我们定义的帧率时，
        # Pygame 会计算需要暂停多长时间，以便游戏的运行速度保持一致。
        self.clock = pygame.time.Clock()
        # 设置游戏结束标志
        self.game_active = False
        # 创建play按钮
        self.play_button = Button(self,"Play")
        # 创建难度选择按钮
        self.easy_button = Button(self,'easy')
        self.hard_button = Button(self,'hard')


    def run_game(self):
        """开始游戏的主循环"""
        # while中是一个事件循环
        while True:
            # 获取事件信息
            self._check_events()
            # 当游戏处于活动状态时，更新飞船位置
            if self.game_active:
                # 根据移动标志计算更新飞船的位置
                self.ship.update()
                # 计算更新每颗子弹的位置，并删除已消失的子弹
                self._update_bullets()
                # 计算更新外星人的位置
                self._update_aliens()
                # 绘制图像并更新屏幕
                self._update_screen()
            else:
                # 绘制play按钮
                self._update_play_screen()
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

            # 响应鼠标点击
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # 获取点击位置元组
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
                

    def _check_play_button(self,mouse_pos):
        """在单机play时开始游戏"""
        # 使用rect的collidepoint方法检测鼠标是否在rectangle内
        # 若游戏开始点击该区域则游戏会重新开始，故添加条件
        if self.play_button.rect.collidepoint(mouse_pos) and not self.game_active:
            # 重置游戏的统计信息
            self.stats.reset_stats()
            self.settings.initialize_dynamic_settings()
            self.game_active = True

            self.buttles.empty()
            self.aliens.empty()

            self._create_fleet()
            self.ship.center_ship()

            # 隐藏光标
            pygame.mouse.set_visible(False)


        elif self.hard_button.rect.collidepoint(mouse_pos) and not self.game_active:
            # 选择困难模式
            # 重置游戏的统计信息

            self.stats.reset_stats()
            self.settings.speedup_scale = self.settings.choose_speed[1]
            self.settings.initialize_dynamic_settings()
            self.settings.increase_speed()
            self.game_active = True

            self.buttles.empty()
            self.aliens.empty()

            self._create_fleet()
            self.ship.center_ship()

            # 隐藏光标
            pygame.mouse.set_visible(False)

        elif self.easy_button.rect.collidepoint(mouse_pos) and not self.game_active:
            # 选择简单模式
            # 重置游戏的统计信息

            self.stats.reset_stats()
            self.settings.speedup_scale = self.settings.choose_speed[0]
            self.settings.initialize_dynamic_settings()
            self.settings.increase_speed()
            self.game_active = True

            self.buttles.empty()
            self.aliens.empty()

            self._create_fleet()
            self.ship.center_ship()

            # 隐藏光标
            pygame.mouse.set_visible(False)

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
        """
        更新子弹的位置，并删除已经消失的子弹
        碰撞检测
        """
        # 在对编组调用update() 时，编组会自动对其中的每个精灵调用 update()，
        # 因此 self.bullets.update() 将为 bullets 编组中的每颗子弹调用 bullet.update()。
        # 向上移动每颗子弹
        self.buttles.update()
        # 在for语句执行过程中，python不允许改变列表的长度
        # 因此使用.copy方法创建一个副本进行循环，修改原列表的值
        for bullet in self.buttles.copy():
            if bullet.rect.bottom <= 0:
                self.buttles.remove(bullet)
        
        self._check_bullet_alien_collisions()

    def _create_fleet(self):
        """创建一个船队"""
        # 一行中填满外星人，直到所有行填满为止

        new_alien = Alien(self)
        alien_width = new_alien.rect.width
        alien_height = new_alien.rect.height
        current_x = alien_width
        current_y = self.settings.alien_y_gap

        while current_y <= (self.settings.screen_hight - self.ship.rect.height - self.settings.alien_y_gap):
            # 绘制行防止超出屏幕边界，一半在外面
            while current_x <= (self.screen.get_width()-alien_width-self.settings.alien_x_gap):
                self._create_alien(current_x,current_y)
                current_x += (alien_width + self.settings.alien_x_gap)
            current_x = alien_width
            current_y += (alien_height + self.settings.alien_y_gap)

    def _update_aliens(self):
        """计算更新外星人"""
        self._check_fleet_edges()
        self.aliens.update()
        self._check_alien_ship_collisions()
        self._check_alien_bottom()


    def _check_fleet_edges(self):
        """检查船队是否触碰边界"""
        for aline in self.aliens.sprites():
            if aline._check_edges():
                self._chenge_fleet_direction()
                break

    def _chenge_fleet_direction(self):
        """将整个舰队向下移动，并改变左右移动方向标志"""
        self.settings.fleet_direction *= -1
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed

    def _create_alien(self,current_x,current_y):
        """将一个外星人放入一行中"""
        new_alien = Alien(self)
        new_alien.x = current_x
        new_alien.rect.x = current_x
        new_alien.rect.y = current_y
        self.aliens.add(new_alien)

    def _check_bullet_alien_collisions(self):
        """碰撞检测与响应"""
        # 检测是否有子弹击中了外星人
        # 若击中，则删除子弹与外星人
        # 将 self.bullets 中的所有子弹与 self.aliens 中的所有外星人进行比较，
        # 看它们是否重叠了在一起。每当有子弹和外星人的 rect 重叠时，
        # groupcollide() 就在返回的字典中添加一个键值对。
        # 两个值为 True 的实参告诉 Pygame 在发生碰撞时删除对应的子弹和外星人。
        collisions = pygame.sprite.groupcollide(self.buttles,self.aliens,True,True)

        # 外星人全部打完后再生成部分
        if not self.aliens:
            # 删除现有的子弹并重新创建船队
            self.buttles.empty()
            self._create_fleet()
            self.settings.increase_speed()

    def _check_alien_ship_collisions(self):
        """检查外星人与飞船之间的碰撞"""
        # spritecollideany() 函数接受两个实参：一个精灵和一个编组。
        # 它检查编组是否有成员与精灵发生了碰撞，并在找到与精灵发生碰撞的成员后停止遍历编组。
        # 这里，它遍历 aliens 编组，并返回找到的第一个与飞船发生碰撞的外星人。
        if pygame.sprite.spritecollideany(self.ship,self.aliens):
            self._ship_hit()

    def _check_alien_bottom(self):
        """检查是否有外星人到达底部"""
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.screen.get_rect().bottom:
                self._ship_hit()
                break

    def _ship_hit(self):
        """响应飞船与外星人碰撞"""
        if self.stats.ship_left > 0:
            self.stats.ship_left -= 1
            self.buttles.empty()
            self.aliens.empty()

            # 创建一个新的船队，并将飞船重新放在屏幕中央
            self._create_fleet()
            self.ship.center_ship()

            # 暂停
            sleep(0.5)
        else:
            self.game_active = False
            pygame.mouse.set_visible(True)

    def _update_ship_left(self):
        """左上角绘制剩余飞船数量"""
        image = self.settings.pic_proportional_scaling(self.settings.ship_image,50)
        rect = image.get_rect()
        rect.x = 10
        rect.y = 10
        for i in range(self.stats.ship_left):
            self.screen.blit(image,rect)
            rect.x += rect.width

    def _update_play_screen(self):
        """显示按钮"""
        self.screen.blit(self.settings.bg_image, (0, 0))
        self.play_button.draw_button()
        self._draw_choose_button()
        pygame.display.flip()

    def _draw_choose_button(self):
        """绘制选择按钮"""
        self.easy_button.rect.midbottom = self.screen.get_rect().midbottom
        self.easy_button.rect.y = 100
        self.hard_button.rect.center = self.screen.get_rect().center
        self.hard_button.rect.y = 200
        self.easy_button.msg_image_rect.center = self.easy_button.rect.center
        self.hard_button.msg_image_rect.center = self.hard_button.rect.center

        self.screen.fill(self.easy_button.button_color,self.easy_button.rect)
        self.screen.blit(self.easy_button.msg_image, self.easy_button.msg_image_rect)

        self.screen.fill(self.hard_button.button_color,self.hard_button.rect)
        self.screen.blit(self.hard_button.msg_image, self.hard_button.msg_image_rect)

    def _update_screen(self):
        """绘制图像更新屏幕内容"""
        # fill() 填充颜色，用于绘制 surface，只接受一个表示颜色的实参。
        # 每次循环时都重新绘制屏幕，是绘图操作(screen是整个窗口的Surface对象)
        #self.screen.fill(self.settings.bg_color)
        # 绘制背景图片
        self.screen.blit(self.settings.bg_image, (0, 0))

        # 绘制剩余飞船数量
        self._update_ship_left()

        # 绘制飞船
        self.ship.blitme()
        # 利用精灵组自带的draw方法绘制外星人
        self.aliens.draw(self.screen)

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