import pygame as pg

from settings import (
    run_width,
    block_path,
)


class Tetris(object):

    def __init__(self):
        self.screen = pg.display.get_surface()
        # 块
        self.block = pg.image.load(block_path)
        # 速度
        self.speed = self.block.get_width()
        # 初始位置
        self.x = 240
        self.y = 0
        # 初始形态
        self.mode = 1

    def return_surface(self):
        return self.block

    def down(self):
        self.y += self.speed
        # 随从
        for obj in self.slave:
            obj.y += self.speed

    def left(self, appeared_lis=None):
        pass_flag = True
        # 判断和已有图形得向左的碰撞检测
        if appeared_lis:
            # 准备工作1
            main_obj_lis = [self]
            main_obj_lis.extend(self.slave)
            # 循环进行碰撞监测
            for main_obj in main_obj_lis:
                for appeared_obj in appeared_lis:
                    width = appeared_obj.return_surface().get_width()
                    if main_obj.y == appeared_obj.y and main_obj.x == appeared_obj.x + width:
                        pass_flag = False
                        break
        return pass_flag

    def right(self, appeared_lis=None):
        pass_flag = True
        # 判断和已有图形得向右的碰撞检测
        if appeared_lis:
            # 准备工作1
            main_obj_lis = [self]
            main_obj_lis.extend(self.slave)
            # 循环进行碰撞监测
            for main_obj in main_obj_lis:
                for appeared_obj in appeared_lis:
                    width = appeared_obj.return_surface().get_width()
                    if main_obj.y == appeared_obj.y and main_obj.x + width == appeared_obj.x:
                        pass_flag = False
                        break
        return pass_flag

    def draw(self, appeared_lis=None):
        # 判断和已有图形得碰撞
        if appeared_lis:
            # 准备工作1
            main_obj_lis = [self]
            main_obj_lis.extend(self.slave)
            # 准备工作2
            # 循环进行碰撞监测
            for main_obj in main_obj_lis:
                for appeared_obj in appeared_lis:
                    if main_obj.x == appeared_obj.x and main_obj.y + main_obj.return_surface().get_height() == appeared_obj.y:
                        return True
        # 下降
        self.down()
        # 自己
        self.screen.blit(self.block, (self.x, self.y))
        # 随从
        for obj in self.slave:
            self.screen.blit(self.block, (obj.x, obj.y))

    def draw_static(self):
        # 自己
        self.screen.blit(self.block, (self.x, self.y))
        # 随从
        for obj in self.slave:
            self.screen.blit(self.block, (obj.x, obj.y))


class TetrisOne(Tetris):
    """"
        口口
        口口
    """

    def __init__(self, x=None, y=None):
        super().__init__()
        if not x and not y:
            # 初始位置
            self.x -= self.block.get_width()
            self.y -= self.block.get_height() * 2
        else:
            # 提示下一个得
            self.x = x
            self.y = y
        # 跟随者
        self.slave = [
            TetrisSlave(self.x + self.block.get_width(), self.y),
            TetrisSlave(self.x, self.y + self.block.get_height()),
            TetrisSlave(self.x + self.block.get_width(), self.y + self.block.get_height()),
        ]

    def change(self):
        pass

    def left(self, appeared_lis=None):
        flag = super().left(appeared_lis)
        if not flag:
            return

        if self.x > 0:
            self.x -= self.speed
            # 随从
            for obj in self.slave:
                obj.x -= self.speed

    def right(self, appeared_lis=None):
        flag = super().right(appeared_lis)
        if not flag:
            return

        if self.x < run_width - self.block.get_width() * 2:
            self.x += self.speed
            # 随从
            for obj in self.slave:
                obj.x += self.speed


class TetrisTwo(Tetris):
    """
        口
        口
        口
        口
    """

    def __init__(self, x=None, y=None):
        super().__init__()
        # 初始位置
        if not x and not y:
            self.y -= self.block.get_height() * 4
        else:
            self.x = x
            self.y = y
        # 跟随者
        self.slave = [
            TetrisSlave(self.x, self.y + self.block.get_height()),
            TetrisSlave(self.x, self.y + self.block.get_height() * 2),
            TetrisSlave(self.x, self.y + self.block.get_height() * 3),
        ]

    def change(self):
        self.mode += 1
        if self.mode % 4 in [1, 3]:
            self.x += self.block.get_width() * 2
            self.y -= self.block.get_height() * 2
            for index in range(0, len(self.slave)):
                obj = self.slave[index]
                obj.x = self.x
                obj.y = self.y + self.block.get_height() * (index + 1)
        elif self.mode % 4 in [2, 0]:
            if self.x < self.block.get_width() * 4:
                self.x = 0
                self.y += self.block.get_width() * 2
            elif self.x > run_width - self.block.get_width() * 4:
                self.x = run_width - self.block.get_width() * 4
                self.y += self.block.get_width() * 2
            else:
                self.x -= self.block.get_width() * 2
                self.y += self.block.get_width() * 2
            for index in range(0, len(self.slave)):
                obj = self.slave[index]
                obj.x = self.x + self.block.get_width() * (index + 1)
                obj.y = self.y

    def left(self, appeared_lis=None):
        flag = super().left(appeared_lis)
        if not flag:
            return

        if self.x > 0:
            self.x -= self.speed
            # 随从
            for obj in self.slave:
                obj.x -= self.speed

    def right(self, appeared_lis=None):
        flag = super().right(appeared_lis)
        if not flag:
            return

        if self.mode % 4 in [1, 3]:
            screen_width = run_width - self.block.get_width()
        else:
            screen_width = run_width - self.block.get_width() * 4

        if self.x < screen_width:
            self.x += self.speed
            # 随从
            for obj in self.slave:
                obj.x += self.speed


class TetrisThree(Tetris):
    """"
        口
        口口口

          口口
          口
          口

        口口口
            口

          口
          口
        口口
    """

    def __init__(self, x=None, y=None):
        super().__init__()
        # 初始位置
        if not x and not y:
            self.x -= self.block.get_width()
            self.y -= self.block.get_height() * 2
        else:
            self.x = x
            self.y = y
        # 跟随者
        self.slave = [
            TetrisSlave(self.x, self.y + self.block.get_height()),
            TetrisSlave(self.x + self.block.get_width(), self.y + self.block.get_height()),
            TetrisSlave(self.x + self.block.get_width() * 2, self.y + self.block.get_height()),
        ]

    def change(self):
        self.mode += 1
        if self.mode % 4 == 1:
            self.y -= self.block.get_height() * 2
            for index in range(0, len(self.slave)):
                obj = self.slave[index]
                obj.x = self.x + self.block.get_width() * index
                obj.y = self.y + self.block.get_height()
        elif self.mode % 4 == 2:
            self.x += self.block.get_width() * 2
            for index in range(0, len(self.slave)):
                obj = self.slave[index]
                obj.x = self.x - self.block.get_width()
                obj.y = self.y + self.block.get_height() * index
        elif self.mode % 4 == 3:
            if self.x <= self.block.get_width():
                self.x = self.block.get_width() * 2
            self.y += self.block.get_height() * 2
            for index in range(0, len(self.slave)):
                obj = self.slave[index]
                obj.x = self.x - self.block.get_width() * index
                obj.y = self.y - self.block.get_height()
        elif self.mode % 4 == 0:
            self.x -= self.block.get_width() * 2
            for index in range(0, len(self.slave)):
                obj = self.slave[index]
                obj.x = self.x + self.block.get_width()
                obj.y = self.y - self.block.get_height() * index

    def left(self, appeared_lis=None):
        flag = super().left(appeared_lis)
        if not flag:
            return

        temp = 0
        if self.mode % 4 in [1, 4]:
            pass
        elif self.mode % 4 == 2:
            temp = self.block.get_width()
        elif self.mode % 4 == 0:
            temp = self.block.get_width() * 2

        left_value = temp

        if self.x > left_value:
            self.x -= self.speed
            # 随从
            for obj in self.slave:
                obj.x -= self.speed

    def right(self, appeared_lis=None):
        flag = super().right(appeared_lis)
        if not flag:
            return

        temp = run_width - self.block.get_width() * 3
        if self.mode % 4 == 1:
            pass
        elif self.mode % 4 in [2, 3]:
            temp = run_width - self.block.get_width()
        elif self.mode % 4 == 0:
            temp = run_width - self.block.get_width() * 2

        screen_width = temp

        if self.x < screen_width:
            self.x += self.speed
            # 随从
            for obj in self.slave:
                obj.x += self.speed


class TetrisFour(Tetris):
    """
       口
       口口
         口

        口口
      口口

       口
       口口
         口

        口口
      口口

    """

    def __init__(self, x=None, y=None):
        super().__init__()
        if not x and not y:
            # 初始位置
            self.y -= self.block.get_height() * 3
        else:
            self.x = x
            self.y = y
        # 跟随者
        self.slave = [
            TetrisSlave(self.x, self.y + self.block.get_height()),
            TetrisSlave(self.x + self.block.get_width(), self.y + self.block.get_height()),
            TetrisSlave(self.x + self.block.get_width(), self.y + self.block.get_height() * 2),
        ]

    def change(self):
        self.mode += 1
        if self.mode % 4 in [1, 3]:
            self.x -= self.block.get_width()
            self.y -= self.block.get_height()
            self.slave[1].x = self.x + self.block.get_width()
            self.slave[1].y = self.y + self.block.get_height()
            self.slave[2].x = self.x + self.block.get_width()
        elif self.mode % 4 in [2, 0]:
            if self.x < self.block.get_width():
                self.x = self.block.get_width() * 2
                self.y += self.block.get_height()
                self.slave[0].x = self.x - self.block.get_width()
                self.slave[1].y = self.y + self.block.get_height()
                self.slave[2].x = 0
            else:
                self.x += self.block.get_width()
                self.y += self.block.get_height()
                self.slave[1].x = self.x - self.block.get_width()
                self.slave[1].y = self.y + self.block.get_height()
                self.slave[2].x = self.x - self.block.get_width() * 2

    def left(self, appeared_lis=None):
        flag = super().left(appeared_lis)
        if not flag:
            return

        temp = 0
        if self.mode % 4 in [2, 0]:
            temp = self.block.get_width() * 2

        left_value = temp

        if self.x > left_value:
            self.x -= self.speed
            # 随从
            for obj in self.slave:
                obj.x -= self.speed

    def right(self, appeared_lis=None):
        flag = super().right(appeared_lis)
        if not flag:
            return

        temp = run_width - self.block.get_width() * 2
        if self.mode % 4 in [2, 0]:
            temp = run_width - self.block.get_width()

        screen_width = temp

        if self.x < screen_width:
            self.x += self.speed
            # 随从
            for obj in self.slave:
                obj.x += self.speed


class TetrisFive(Tetris):
    """
          口
        口口口

          口
          口口
          口

        口口口
          口

          口
        口口
          口
    """

    def __init__(self, x=None, y=None):
        super().__init__()
        if not x and not y:
            # 初始位置
            self.y -= self.block.get_height() * 2
        else:
            self.x = x
            self.y = y
        # 跟随者
        self.slave = [
            TetrisSlave(self.x - self.block.get_width(), self.y + self.block.get_height()),
            TetrisSlave(self.x, self.y + self.block.get_height()),
            TetrisSlave(self.x + self.block.get_width(), self.y + self.block.get_height()),
        ]

    def change(self):
        self.mode += 1
        if self.mode % 4 == 1:
            if self.x >= run_width - self.block.get_width():
                self.x = run_width - self.block.get_width() * 2
            else:
                self.x += self.block.get_width()
            self.y -= self.block.get_height()
            for index in range(0, len(self.slave)):
                obj = self.slave[index]
                obj.x = self.x - self.block.get_width() + self.block.get_width() * index
                obj.y = self.y + self.block.get_height()
        elif self.mode % 4 == 2:
            self.x += self.block.get_width()
            self.y += self.block.get_height()
            for index in range(0, len(self.slave)):
                obj = self.slave[index]
                obj.x = self.x - self.block.get_width()
                obj.y = self.y - self.block.get_height() + self.block.get_height() * index
        elif self.mode % 4 == 3:
            if self.x < self.block.get_width() * 2:
                self.x = self.block.get_width()
            else:
                self.x -= self.block.get_width()
            self.y += self.block.get_height()
            for index in range(0, len(self.slave)):
                obj = self.slave[index]
                obj.x = self.x - self.block.get_width() + self.block.get_width() * index
                obj.y = self.y - self.block.get_height()
        elif self.mode % 4 == 0:
            self.x -= self.block.get_width()
            self.y -= self.block.get_height()
            for index in range(0, len(self.slave)):
                obj = self.slave[index]
                obj.x = self.x + self.block.get_width()
                obj.y = self.y - self.block.get_height() + self.block.get_height() * index

    def left(self, appeared_lis=None):
        flag = super().left(appeared_lis)
        if not flag:
            return

        temp = self.block.get_width()
        if self.mode % 4 == 0:
            temp = 0

        left_value = temp

        if self.x > left_value:
            self.x -= self.speed
            # 随从
            for obj in self.slave:
                obj.x -= self.speed

    def right(self, appeared_lis=None):
        flag = super().right(appeared_lis)
        if not flag:
            return

        temp = run_width - self.block.get_width() * 2
        if self.mode % 4 == 2:
            temp = run_width - self.block.get_width()

        screen_width = temp

        if self.x < screen_width:
            self.x += self.speed
            # 随从
            for obj in self.slave:
                obj.x += self.speed


class TetrisSlave(object):

    def __init__(self, x, y):
        # 初始位置
        self.x = x
        self.y = y
        # 块
        self.block = pg.image.load(block_path)

    def return_surface(self):
        return self.block


class GeneralTetris(object):

    def __init__(self, x, y):
        # 初始位置
        self.x = x
        self.y = y
        # 块
        self.block = pg.image.load(block_path)

        self.screen = pg.display.get_surface()

    def return_surface(self):
        return self.block

    def down(self):
        self.y += self.block.get_height()

    def draw(self):
        # 渲染自己
        self.screen.blit(self.block, (self.x, self.y))

