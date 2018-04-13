import pygame
from pygame.locals import *
import time
import numpy as np
import random

button_1_image_up = 'play.jpg'
button_1_image_down = 'playing.jpg'
imageup = 'play.jpg'
imagedown = 'playing.jpg'
imagemine = "mine.jpg"
num_0, num_1, num_2, num_3, num_4, num_5, num_6, num_7, num_8 = "0.jpg", "1.png", "2.png", "3.png", "4.png", "5.png", "6.png", "7.png", "8.png"
background_image_filename = "back.jpg"
Open_image_filename = "back2.jpg"
flag_pic = "flag.jpg"
boom_pic = "boom.jpg"
imageover = "over.jpg"
imageover2 = "success.jpg"


n = 12  # 设置行数
num = 8  # 设置雷的数目

x_start, y_start = random.randint(0, n - 1), random.randint(0, n - 1)  # 初始化一个点


pygame.font.init()


class Button(object):
    """开始游戏界面"""

    def __init__(self, imageup, imagedown, position):
        self.imageup = pygame.image.load(imageup)
        self.imageup = pygame.transform.scale(self.imageup, (120, 70))
        self.imagedown = pygame.image.load(imagedown)
        self.imagedown = pygame.transform.scale(self.imagedown, (120, 70))
        self.position = position

    def isOver(self):
        for ev in pygame.event.get():
            flag = 0
            if ev.type == MOUSEBUTTONDOWN:
                point_x, point_y = pygame.mouse.get_pos()

                x1, y1 = 260, 200
                w, h = self.imageup.get_size()
                in_x1 = x1 - w < point_x < x1 + w
                in_y1 = y1 - h < point_y < y1 + h
                if in_x1 and in_y1:
                    flag = 1
                else:
                    flag = 0
                return flag
            elif ev.type == QUIT:
                exit(0)


class Map(object):
    def __init__(self):
        # 加载图像
        self.mine = self.convert_image_55(imagemine)
        self.num_0 = self.convert_image_55(num_0)
        self.num_1 = self.convert_image_55(num_1)
        self.num_2 = self.convert_image_55(num_2)
        self.num_3 = self.convert_image_55(num_3)
        self.num_4 = self.convert_image_55(num_4)
        self.num_5 = self.convert_image_55(num_5)
        self.num_6 = self.convert_image_55(num_6)
        self.num_7 = self.convert_image_55(num_7)
        self.num_8 = self.convert_image_55(num_8)
        self.num_flag = self.convert_image_55(flag_pic)
        self.num_boom = self.convert_image_55(boom_pic)

        # 记录
        self.go_to_next = 0  # 两种选择方法的flag
        self.mine_map = np.zeros((n, n))  # 地图
        self.pos_x = x_start
        self.pos_y = y_start
        self.neighbors = []  # 存储八领域
        self.members = []  # 存储数字
        self.searched = []  # 存储拓展点
        self.next = []  # 存储继续进行的点
        self.next_B = []
        self.flag_loc = []  # 存储旗子的点
        self.mine_pos = []  # 存储地雷的点
        # 画背景
        self.screen = pygame.display.set_mode((100 + n * 55, n * 55), 0, 32)
        self.background = pygame.image.load(
            background_image_filename).convert()
        self.background = pygame.transform.scale(
            self.background, (100 + n * 55, n * 55))
        self.screen.blit(self.background, (0, 0))

        self.mines_loc()
        self.display_lines()
        self.display_mines()

    def mine_num(self, x, y):
        neighbor_mine_num = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                else:
                    if x + i >= 0 and x + i < n:
                        # print("1111111111111111")
                        if y + j >= 0 and y + j < n:
                            #print(i, j)
                            if self.mine_map[x + i][y + j] == 9:
                                neighbor_mine_num += 1
        return neighbor_mine_num

    def mines_loc(self):
        """随机布雷"""
        for i in range(num):
            while True:
                x = random.randint(0, n - 1)
                y = random.randint(0, n - 1)
                if self.mine_map[x][y] == 0:
                    self.mine_map[x][y] = 9   # 让雷等于9
                    self.mine_pos.append((x, y))
                    break

    def sweep(self, x, y):
        print("entrying sweep DIEDAI", (x, y))
        # print(self.members)
        if self.mine_num(x, y) > 0 and self.mine_map[x][y] != 9:
            if (x, y) not in self.members:
                self.members.append((x, y))
                # 记录所有带数字的点
            return
        if self.mine_map[x][y] != 9:
            self.searched.append((x, y))
        # 记录已经递归后的点
        # 标记过的地雷位置不考虑
        if x - 1 >= 0 and (x - 1, y) not in self.searched:
            self.sweep(x - 1, y)
        if x + 1 < n and (x + 1, y) not in self.searched:
            self.sweep(x + 1, y)
        if y - 1 >= 0 and (x, y - 1) not in self.searched:
            self.sweep(x, y - 1)
        if y + 1 < n and (x, y + 1) not in self.searched:
            self.sweep(x, y + 1)

    def draw_num(self):
        """画数字"""
        print("Entrying draw_num")
        for (self.pos_x, self.pos_y) in self.members:
            self.num_of_mine(self.pos_x, self.pos_y)
        for (self.pos_x, self.pos_y) in self.searched:
            self.num_of_mine(self.pos_x, self.pos_y)
        pygame.display.update()
        time.sleep(2)

    def draw_mine_flag(self):
        print("Entrying draw_mine_flag")
        print("self.flag_loc", self.flag_loc)
        for (self.pos_x, self.pos_y) in self.flag_loc:
            self.screen.blit(self.num_flag, (55 * self.pos_y, 55 * self.pos_x))

    def num_of_mine(self, x, y):
        """搜寻数字旁边的地雷并绘图"""
        #print("Entrying  num_of_mine")
        n = self.mine_num(x, y)
        if n == 0:
            self.screen.blit(self.num_0, (55 * y, 55 * x))
        if n == 1:
            self.screen.blit(self.num_1, (55 * y, 55 * x))
        if n == 2:
            self.screen.blit(self.num_2, (55 * y, 55 * x))
        if n == 3:
            self.screen.blit(self.num_3, (55 * y, 55 * x))
        if n == 4:
            self.screen.blit(self.num_4, (55 * y, 55 * x))
        if n == 5:
            self.screen.blit(self.num_5, (55 * y, 55 * x))
        if n == 6:
            self.screen.blit(self.num_6, (55 * y, 55 * x))
        if n == 7:
            self.screen.blit(self.num_7, (55 * y, 55 * x))
        if n == 8:
            self.screen.blit(self.num_8, (55 * y, 55 * x))
        return n

    def display_lines(self):
        for i in range(1, n + 1):
            pygame.draw.line(self.screen, (255, 255, 255),
                             (55 * i, 0), (55 * i, n * 55), 2)
            pygame.draw.line(self.screen, (255, 255, 255),
                             (0, 55 * i), (n * 55, 55 * i), 2)
        pygame.display.update()
        # time.sleep(2)

    def display_mines(self):
        if np.argwhere(self.mine_map == 9) != []:
            mine_loc = np.argwhere(self.mine_map == 9)
            # print(mine_loc)
            for i in mine_loc:
                mine_loc_y, mine_loc_x = i
                screen.blit(self.mine, (55 * mine_loc_x, 55 * mine_loc_y))
        pygame.display.update()
        time.sleep(2)

    def convert_image_55(self, image):
        """将图片转化为小格子"""
        self.image = image
        self.image = pygame.image.load(self.image)
        self.image = pygame .transform.scale(self.image, (55, 55))
        return self.image

    def isboom(self, x, y):
        screen.blit(self.num_boom, (55 * y, 55 * x))
        pygame.display.update()
        time.sleep(2)

    def find_neighbers(self, x, y):

        self.neighbors.clear()
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                else:
                    if x + i >= 0 and x + i < n:
                        # print("1111111111111111")
                        if y + j >= 0 and y + j < n:
                            self.neighbors.append((x + i, y + j))
        return self.neighbors

    def find_mine(self):
        """找出一定是mine的点"""
        print("Entrying find_mine")
        for (x, y) in self.members:
            unsloved = list(set(self.find_neighbers(
                x, y)) - set(self.searched) - set(self.members) - set(self.flag_loc))
            flaged = list(set(self.find_neighbers(x, y)) -
                          set(self.searched) - set(self.members))
            if self.mine_num(x, y) - len(set(flaged) & set(self.flag_loc)) >= len(unsloved):
                for (x1, y1) in unsloved:
                    self.flag_loc.append((x1, y1))
                    print("flag_loc22222222222", self.flag_loc)
                    self.screen.blit(self.num_flag, ((55 * y1, 55 * x1)))

    def solved(self):
        """记录已经完成的点的数量"""
        n = 0
        for pos in self.flag_loc:
            if pos in self.mine_pos:
                n += 1
        return n

    def ChooseWithBigProbability(self):
        """
        概率选择函数
        算法思想：
            当遇到无法肯定有雷或无雷的情况时，找出还没有被访问过的位置
            找出这些位置八邻域内已被标明地雷数的位置的地雷数的和，并用
            和除以8，将这些位置和其对应的概率存入容器并按概率从大到小的
            顺序排序，如果概率最大的位置的概率大于等于0.75，那么将该位置
            标注为地雷，如果概率小于0.75，那么找出还未访问过且不在下一步
            计划的位置容器的位置，随机选择一个位置，如果踩到雷游戏结束，
            如果该位置周围没有地雷，则调用Ergodic()遍历，如果周围有地雷
            那么标注该位置的地雷数
        """
        print("Entrying ChooseWithBigProbability")
        noSeen = []
        # 待排雷数量
        unsloved_mine_num = num - self.solved()
        # 找出还未遍历过的位置
        for i in range(n):
            for j in range(n):
                if (i, j) not in self.searched + self.flag_loc + self.members:
                    s = list(set(self.find_neighbers(i, j))
                             & set(self.members))
                    numerator = 0
                    for s1 in s:
                        numerator += self.mine_num(s1[0], s1[1])
                    # 计算概率
                    noSeen.append([(i, j), numerator / 8])
        sorted(noSeen, key=lambda proba: proba[1], reverse=True)
        if noSeen != []:
            if noSeen[0][1] >= 0.65:
                pos = noSeen[0][0]
                self.flag_loc.append(pos)
            else:
                nos = [p[0] for p in noSeen]
                s = list(set(nos) - set(self.next))
                index = 0
                pos = (-1, -1)
                if len(s) > 1:
                    index = random.randint(0, len(s) - 1)
                    pos = s[index]
                elif len(s) == 1:
                    pos = s[0]
                elif s == []:
                    pos = noSeen[0][0]
                if self.mine_map[pos[0]][pos[1]] == 9:
                    self.isboom(pos[0], pos[1])
                    time.sleep(2)
                    exit()
                elif self.mine_num(pos[0], pos[1]) in range(1, 9):
                    self.members.append((pos[0], pos[1]))
                elif self.mine_num(pos[0], pos[1]) == 0:
                    self.sweep(pos[0], pos[1])
        noSeen.clear()
        self.go_to_next = 0

    def find_next(self):
        """
        找到下一步需要点开的点
        """
        print("Entrying find_next")
        self.next.clear()  # 清空下一步的点
        for (x, y) in self.members:
            for (x1, y1) in self.find_neighbers(x, y):
                if (x1, y1) not in self.searched + self.next + self.members:
                    self.next.append((x1, y1))
                    # print("find_next:",self.next)
        if self.next_B == self.next:
            print("self.go_to_next22222222222222222222222222222222222")
            self.go_to_next = 1
        self.next_B = self.next

    def NoMines(self):
        """
        找出能确定没有地雷的位置
        算法思想：
            对于每个已被标明周围地雷数的位置，找出该位置八邻域内剩下
            未访问过的位置，查看当前位置周围的地雷是否被全部标记了，
            如果已经全部被标记，那么该位置八邻域内剩下未访问过的位置
            ，如果位置周围的地雷数为0，那么用Ergodic()函数遍历，如果
            位置周围地雷数不为0，那么标明该位置的地雷数
        """
        print("Entrying NoMines")
        for (x, y) in self.members:
            s = list(set(self.find_neighbers(x, y)) -
                     set(self.searched) - set(self.members) - set(self.flag_loc))
            if self.mine_num(x, y) == len(set(self.find_neighbers(x, y)) & set(self.flag_loc)):
                for (x1, y1) in s:
                    if self.mine_map[x1][y1] == 9:
                        self.flag_loc.append((x1, y1))
                        continue
                    if self.mine_num(x1, y1) == 0:
                        self.searched.append((x1, y1))
                        print("DIEDAI FORM NO")
                        self.sweep(x1, y1)
                        self.screen.blit(self.num_0, (55 * y, 55 * x))
                        continue
                    if self.mine_num(x1, y1) > 0 and self.mine_num(x1, y1) != 9:
                        self.num_of_mine(x1, y1)
                        self.members.append((x1, y1))

    def win(self):
        screen = pygame.display.set_mode((55 * n + 100, 55 * n), 0, 32)
        overground = pygame.image.load(imageover2).convert()
        overground = pygame.transform.scale(overground, (55 * n + 100, 55 * n))
        screen.blit(overground, (0, 0))
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
        pygame.display.update()
        time.sleep(5)
        exit()
        # print('Game Over')

    def solve(self):
        flag = 1
        if self.mine_map[x_start][y_start] == 9:
            self.isboom(x_start, x_start)
            pygame.display.update()
            flag = 2
            print("You boom in", (x_start, y_start))
        while (flag == 1):
            print("1111111111111111111111111111111111111111111111111111111")
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit(0)
            if flag == 1:
                if self.solved() == num:
                    print("YOU win!!!!!!!!!!!!!!")
                    time.sleep(6)
                    self.win()
                print("2222222222222222222222222222")
                self.sweep(self.pos_x, self.pos_y)
                self.draw_num()
                self.draw_mine_flag()  # 画旧旗子
                self.find_mine()  # 画新旗子
                self.find_next()
                self.NoMines()

                if self.go_to_next == 1:
                    self.ChooseWithBigProbability()
                pygame.display.update()

        return flag


if __name__ == '__main__':
    pygame.display.init()
    while True:
        screen = pygame.display.set_mode((650, 550), 0, 32)
        openground = pygame.image.load(Open_image_filename).convert()
        openground = pygame.transform.scale(openground, (650, 550))
        screen.blit(openground, (0, 0))
        image = pygame.image.load(imageup)
        image = pygame.transform.scale(image, (120, 70))
        screen.blit(image, (260, 200))
        run_flag = Button(button_1_image_up, button_1_image_down, (260, 200))
        myflag = run_flag.isOver()
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
        pygame.display.update()

        while myflag == 1:
            mine_sweep = Map()
            myflag = mine_sweep.solve()

        while myflag == 2:
            screen = pygame.display.set_mode((650, 550), 0, 32)
            openground = pygame.image.load(imageover).convert()
            openground = pygame.transform.scale(openground, (650, 550))
            screen.blit(openground, (0, 0))
            for event in pygame.event.get():
                if event.type == QUIT:
                    exit()
            pygame.display.update()
            # print('Game Over')

        pygame.display.update()
