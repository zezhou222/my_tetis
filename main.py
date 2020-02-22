import pygame as pg
from random import randint

from settings import (
    width,
    height,
    frame_num,
    background_path,
    speed_frame_num
)

from tetris import *


class Main(object):

    def __init__(self):
        self.exit_flag = False

        pg.init()
        pg.display.init()

        self.screen = pg.display.set_mode(size=(width, height))

        self.clock_obj = pg.time.Clock()
        # 图形的选择
        self.lib = [TetrisOne, TetrisTwo, TetrisThree, TetrisFour, TetrisFive]
        # 图形对象
        self.tetris_obj = Tetris()
        self.tetris_obj.first = self.lib[randint(0, len(self.lib)-1)]()
        self.tetris_obj.second = self.lib[randint(0, len(self.lib)-1)]
        self.tetris_obj.second_help = self.tetris_obj.second(x=run_width + 100, y=150)
        self.tetris_obj.second = self.tetris_obj.second()
        # 已出列表
        self.appeared_lis = []
        # 分数
        self.score = 0
        # 背景图
        self.background = pg.image.load(background_path)

    def add_appeared_lis(self):
        # 添加至已出现列表中
        temp = [self.tetris_obj.first]
        temp.extend(self.tetris_obj.first.slave)
        for obj in temp:
            self.appeared_lis.append(GeneralTetris(obj.x, obj.y))
        # 第二个上位
        self.tetris_obj.first = self.tetris_obj.second
        self.tetris_obj.second = self.lib[randint(0, len(self.lib) - 1)]
        # 提示得
        self.tetris_obj.second_help = self.tetris_obj.second(x=run_width + 100, y=150)
        self.tetris_obj.second = self.tetris_obj.second()

    def draw(self):
        # 背景图
        self.screen.blit(self.background, (0, 0))
        # 当前图形
        flag = self.tetris_obj.first.draw(self.appeared_lis)
        if flag:
            self.add_appeared_lis()
        # 以出现的图形
        for obj in self.appeared_lis:
            obj.draw()
        # 下个图形提示信息
        self.tetris_obj.second_help.draw_static()
        # 分数
        font = pg.font.SysFont("font1", size=30)
        text = font.render("Score: %s" % int(self.score), 1, (0, 0, 0))
        self.screen.blit(text, (3, 3))
        # 下降到最低停止
        lis = [self.tetris_obj.first]
        lis.extend(self.tetris_obj.first.slave)
        for obj in lis:
            if obj.y >= height - obj.block.get_height():
                self.add_appeared_lis()
                # 跳出，很重要。
                break
        # 刷新页面
        pg.display.flip()
        # 检测全屏是否有同行都有小方块得，进行消除行操作(仅对以出的图形)
        if not self.appeared_lis:
            return
        block_height = self.tetris_obj.block.get_height()
        row_num = run_width / block_height
        # 倒序检查
        for y in range(height-block_height, 0, -block_height):
            temp_row_count = 0
            for obj in self.appeared_lis:
                # 同行方块加起来
                if obj.y == y:
                    temp_row_count += 1
            # 同行方块数据和最大方块数相等，那么当前行的方块进行销毁，并且之上的方块进行下移
            if temp_row_count == row_num:
                del_obj = []
                # 记录删除的对象
                for obj in self.appeared_lis:
                    if obj.y == y:
                        del_obj.append(obj)
                # 在已出现的图形中移除
                for obj in del_obj:
                    self.appeared_lis.remove(obj)
                    del obj
                # 之上的方块下移
                for obj in self.appeared_lis:
                    if obj.y < y:
                        obj.down()
                # 加分
                self.score += row_num * 10
        # 判断已出图形，超出屏幕，重新开始
        for obj in self.appeared_lis:
            if obj.y == 0:
                self.__init__()
                break

    def run(self):
        frame = frame_num
        speed_down_flag = False
        while not self.exit_flag:
            # 一秒多少帧
            self.clock_obj.tick(frame)

            # 监听事件
            for event in pg.event.get():
                # 退出事件
                if event.type == pg.QUIT:
                    self.exit_flag = True
                elif event.type == pg.KEYDOWN:
                    # 上变换当前图形
                    if event.key == pg.K_UP:
                        self.tetris_obj.first.change()

            # 持续监测按键
            if pg.key.get_pressed()[pg.K_LEFT] and not speed_down_flag:
                self.tetris_obj.first.left(self.appeared_lis)
            elif pg.key.get_pressed()[pg.K_RIGHT] and not speed_down_flag:
                self.tetris_obj.first.right(self.appeared_lis)
            elif pg.key.get_pressed()[pg.K_DOWN]:
                # 提高帧率，加速下落
                frame = speed_frame_num
                # 快速下落标志
                speed_down_flag = True
            else:
                # 重置
                frame = frame_num
                speed_down_flag = False

            self.draw()


if __name__ == '__main__':
    Main().run()
