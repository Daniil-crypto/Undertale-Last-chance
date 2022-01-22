import pygame, sys, math, time

from pygame.locals import *
from random import randint
from pygame import Color, Rect, Surface


class Player():
    def __init__(self):
        self.move = False
        self.f = 1.5
        self.x, self.y, self.speed, self.w, self.h = 290, 390, 120, 16 * n // self.f, 16 * n // self.f
        self.gravity = "down"
        self.mode = "blue"
        self.speedfall = 1
        self.jumping = False
        self.start_g = 10
        self.shake_flag = False
        if self.gravity == "down" or self.gravity == "right":
            self.g = -self.start_g
        elif self.gravity == "up" or self.gravity == "left":
            self.g = self.start_g
        self.hp = 92
        self.draw_player()

    def draw_player(self):
        global red_soul, blue_up, blue_down, blue_left, blue_right
        if self.mode == "red":
            self.pl = red_soul
        elif self.mode == "blue":
            if self.gravity == "down":
                self.pl = blue_down
            elif self.gravity == "up":
                self.pl = blue_up
            elif self.gravity == "left":
                self.pl = blue_left
            elif self.gravity == "right":
                self.pl = blue_right
        self.pl = change_scale(self.pl, self.f, self.f)
        screen.blit(self.pl, (self.x, self.y))
        self.rect = Rect(self.x, self.y, self.w, self.h)


    def movement(self, ksx=0, ksy=0, keyn="down"):
        global fps
        global g
        self.move = True
        if self.mode == "red":
            self.x, self.y = self.x + self.speed * ksx // fps, self.y + self.speed * ksy // fps
        elif self.mode == "blue":
            if self.gravity == "down" or self.gravity == "up":
                self.x += self.speed * ksx // fps
            elif self.gravity == "left" or self.gravity == "right":
                self.y += self.speed * ksy // fps
            if keyn == self.gravity and self.collision():
                self.jumping = True
                self.phizic(0)
            if self.jumping and keyn == self.gravity:
                self.phizic(self.g)
                self.speedfall = 0
                if self.g >= 0 and (self.gravity == "down" or self.gravity == "right"):
                    self.jumping = False
                    self.g = -self.start_g
                    return
                elif self.g <= 0 and (self.gravity == "up" or self.gravity == "left"):
                    self.jumping = False
                    self.g = self.start_g
                    return
                if self.gravity == "down" or self.gravity == "right":
                    self.g += 0.4
                elif self.gravity == "up" or self.gravity == "left":
                    self.g -= 0.4

    def phizic(self, g):
        if self.jumping:
            if self.gravity == "down" or self.gravity == "up":
                self.y += g
            elif self.gravity == "left" or self.gravity == "right":
                self.x += g
        elif self.collision() == False:
            if self.gravity == "down" or self.gravity == "left":
                self.speedfall += g
            elif self.gravity == "up" or self.gravity == "right":
                self.speedfall -= g
            if self.gravity == "down" or self.gravity == "up":
                self.y += self.speedfall
            elif self.gravity == "left" or self.gravity == "right":
                self.x -= self.speedfall
        else:
            self.speedfall = 0

    def collision(self, y=None):
        f = False
        if self.y > box.y + box.h - self.w - 6 and self.gravity == "down":
            f = True
        if self.y < box.y + 6 and self.gravity == "up":
            f = True
        if self.x > box.x + box.w - self.h - 6 and self.gravity == "right":
            f = True
        if self.x < box.x + 6 and self.gravity == "left":
            f = True
        for i in at.all_platforms:
            if self.gravity == "down":
                if (self.x + self.w >= i.x + box.x and self.x <= i.x + box.x + i.w and
                    self.y + self.h >= i.y + box.y and self.y + self.h <= i.y + box.y + i.h
                    and self.jumping == False):
                    f = True
                    if i.type == "green":
                        self.x += i.speedx
                        self.y += i.speedy
            if self.gravity == "up":
                if (self.x + self.w >= i.x + box.x and self.x <= i.x + box.x + i.w and
                    self.y >= i.y + box.y and self.y <= i.y + box.y + i.h
                    and self.jumping == False):
                    f = True
                    if i.type == "green":
                        self.x += i.speedx
                        self.y += i.speedy
            if self.gravity == "left":
                if (self.x + self.w >= i.x + box.x + i.w - 5 and self.x <= i.x + box.x + i.w and
                    self.y + self.h >= i.y + box.y and self.y <= i.y + box.y + i.h
                    and self.jumping == False):
                    f = True
                    if i.type == "green":
                        self.x += i.speedx
                        self.y += i.speedy
            if self.gravity == "right":
                if (self.x + self.w >= i.x + box.x and self.x <= i.x + box.x + 5 and
                    self.y + self.h >= i.y + box.y and self.y <= i.y + box.y + 5
                    and self.jumping == False):
                    f = True
                    if i.type == "green":
                        self.x += i.speedx
                        self.y += i.speedy
        return f

    def ret_type(self):
        return self.mode

    def jum(self, knum):
        if knum == self.gravity:
            player.jumping = False
            if self.gravity == "down" or self.gravity == "right":
                player.g = -self.start_g
            elif self.gravity == "left" or self.gravity == "up":
                player.g = self.start_g

    def change_gravity(self, new_g, fast=True):
        self.gravity = new_g
        self.jumping = False
        if self.gravity == "down" or self.gravity == "right":
            if fast:
                self.shake_flag = True
                if self.gravity == "right":
                    self.speedfall = -40
                else:
                    self.speedfall = 40
            else:
                self.speedfall = 0
            self.g = -self.start_g
        elif self.gravity == "up" or self.gravity == "left":
            if fast:
                self.shake_flag = True
                if self.gravity == "left":
                    self.speedfall = 40
                else:
                    self.speedfall = -40
            else:
                self.speedfall = 0
            self.g = self.start_g

    def check_box1(self):
        if self.x < box.x + 4:
            self.x = box.x + 4
        if self.x > box.x + box.w - 4 - self.w:
            self.x = box.x + box.w - 2 - self.w
        if self.y < box.y + 4:
            self.y = box.y + 4
        if self.y > box.y + box.h - 4 - self.h:
            self.y = box.y + box.h - 2 - self.h

    def hit(self):
        f = False
        for i in at.bones:
            for j in i:
                mask1 = pygame.mask.from_surface(self.pl)
                mask2 = pygame.mask.from_surface(j.bon)
                if mask1.overlap_area(mask2, (int(j.x + box.x - self.x + 4), int(j.y + box.y - self.y + 4))) > 0:
                    if j.color == "white":
                        f = True
                        self.hp -= 1
                    if j.color == "blue" and (self.move or self.speedfall != 0):
                        f = True
                        self.hp -= 1
                    if j.color == "orange" and self.move == False and self.speedfall == 0:
                        f = True
                        self.hp -= 1
        for i in at.blasters:
            if i.track1 != []:
                mask1 = pygame.mask.from_surface(self.pl)
                mask2 = pygame.mask.from_surface(i.track1)
                if mask1.overlap_area(mask2, (int(i.xxyy1[0] - self.x), int(i.xxyy1[1] - self.y))) > 0:
                    f = True
                    self.hp -= 2
        if self.collision() and self.shake_flag:
            at.shaker = shaker(2, screen)
            self.shake_flag = False
        if f:
            print(self.hp)


class Atk():
    def __init__(self, col, type, x, y, w, h, topl=False, an=90, f=1.5, shak=False, new123=False):
        global track, blast, blast_open
        self.po1 = track.get_rect()[3] // 2
        self.x, self.y, self.h, self.w = x, y, h, w
        self.color = col
        self.type = type
        self.topl = topl
        self.an = an
        self.sec = 0
        self.a = 0.5
        self.alpha = 250
        self.f = f
        self.x_y = (0, 0)
        self.x_yt = (0, 0)
        self.an1 = 0
        self.shak = shak
        self.new123 = new123
        self.track1 = []
        if type == "blaster":
            self.blast = change_scale(blast).convert()
            f0, f0, self.w, self.h = self.blast.get_rect()
            self.track = change_scale(track, self.f, 2.2).convert()
            self.track.set_colorkey((0, 0, 0))
        if type == "bone_s":
            self.bon = Surface((10, int(h)), pygame.SRCALPHA, 32)
            if self.color == "white":
                self.bon.blit(bone_up, (0, 0))
                self.bon.blit(self.change_scale(bone_middle, 1, (h - 12) / 6), (2, 6))
                self.bon.blit(bone_down, (0, h - 6))
                if self.an != 0:
                    self.bon = rot(self.bon, self.an)[0]
            if self.color == "orange":
                self.bon.blit(bone_up_orange, (0, 0))
                self.bon.blit(self.change_scale(bone_middle_orange, 1, (h - 12) / 6), (2, 6))
                self.bon.blit(bone_down_orange, (0, h - 6))
                if self.an != 0:
                    self.bon = rot(self.bon, self.an)[0]
            if self.color == "blue":
                self.bon.blit(bone_up_blue, (0, 0))
                self.bon.blit(self.change_scale(bone_middle_blue, 1, (h - 12) / 6), (2, 6))
                self.bon.blit(bone_down_blue, (0, h - 6))
                if self.an != 0:
                    self.bon = rot(self.bon, self.an)[0]
        self.draw()


    def change_scale(self, image, n1, n2):
        size = image.get_size()
        return pygame.transform.scale(image, (int(size[0] * n1), int(size[1] * n2)))


    def draw(self, sec=20, sec1=0, sec_end=30):
        global screen, n, bone_white
        self.sec += 1
        if self.type == 'bone':
            if self.an == 90 or self.an == 270:
                if self.color == "white":
                    self.bon = bone_white_rot
                if self.color == "blue":
                    self.bon = bone_blue_rot
                if self.color == "orange":
                    self.bon = bone_orange_rot
            else:
                if self.color == "white":
                    self.bon = bone_white
                if self.color == "blue":
                    self.bon = bone_blue
                if self.color == "orange":
                    self.bon = bone_orange
            self.bon = change_scale(self.bon, 2, self.f)

        if self.type == "bone" or self.type == "bone_s":
            if not(self.new123):
                pole.blit(self.bon, (self.x, self.y))

        if self.type == "blaster":
            #Очень замудрёная система выстрелов из бластеров
            if self.sec == 1:
                if self.topl:
                    self.blast1, self.x_y = self.rotate_to_player(self.blast)[0], (self.rotate_to_player(self.blast)[1][0] + self.x, self.rotate_to_player(self.blast)[1][1] + self.y)
                else:
                    self.blast1, self.x_y = rot(self.blast, self.an)[0], (rot(self.blast, self.an)[1][0] + self.x, rot(self.blast, self.an)[1][1] + self.y)
                    self.angle = self.an
                if self.angle == 0 or self.an == 0:
                    self.angle = 1 * 10 ** -6
                self.count = 0.18
                self.x_y = self.x_y[0] - self.pos1()[0], self.x_y[1] - self.pos1()[1] - 10
            if self.sec >= 1 and self.sec <= self.sec <= 10:
                self.x_y = self.x_y[0] + self.pos1()[0] * self.count, self.x_y[1] + self.pos1()[1] * self.count
                self.count -= 0.018
            if self.sec == sec - 1:
                self.blast = change_scale(blast, 1.1)
                self.blast1, self.x_y = rot(self.blast, self.angle)[0], (rot(self.blast, self.angle)[1][0] + self.x, rot(self.blast, self.angle)[1][1] + self.y)
            if self.sec == sec:
                if self.shak:
                    self.spis = shaker(1, screen)
                else:
                    self.spis = []
                self.alpha = 255
                self.track.set_alpha(self.alpha)
                self.blast = change_scale(blast_open).convert()
                self.blast1, self.x_y = rot(self.blast, self.angle)[0], (rot(self.blast, self.angle)[1][0] + self.x, rot(self.blast, self.angle)[1][1] + self.y)
                self.track1, self.x_yt = rot(self.track, self.angle, True, (self.w // 2, self.h // 2))[0], (rot(self.track, self.angle, True, (self.w // 2, self.h // 2))[1][0], rot(self.track, self.angle, True, (self.w // 2, self.h // 2))[1][1])
            if self.sec > sec + sec1:
                B = -(self.angle - 90)
                x, y = math.cos(math.radians(B)) * 300, math.sin(math.radians(B)) * 300
                self.moving(-x / fps * self.a, -y / fps * self.a, True)
                self.a += 0.005 * (sec + sec1 + sec_end)
                self.alpha -= 3
                self.track.set_alpha(self.alpha)
                if sec + sec1 + 3 >= self.sec:
                    self.track = change_scale(self.track, 1.8, 2)
                elif self.track.get_size()[0] * 2 // 2.4 > 0:
                    self.track = change_scale(self.track, 2.4, 2)
                else:
                    return True
                if self.sec % 6 == 0:
                    self.blast = change_scale(blast_open2).convert()
                if self.sec % 6 == 3:
                    self.blast = change_scale(blast_open3).convert()
                self.blast1, self.x_y = rot(self.blast, self.angle)[0], (rot(self.blast, self.angle)[1][0] + self.x, rot(self.blast, self.angle)[1][1] + self.y)
                self.track1, self.x_yt = rot(self.track, self.angle, True, (self.w // 2, self.h // 2))[0], (rot(self.track, self.angle, True, (self.w // 2, self.h // 2))[1][0], rot(self.track, self.angle, True, (self.w // 2, self.h // 2))[1][1])
                self.im = screen
                if self.spis != []:
                    x123, y123 = self.spis.pop(0), self.spis.pop(0)
                    screen.blit(self.im, (x123, y123))
                    screen.blit(self.track1, (self.pos()[0] + self.x + self.x_yt[0], self.pos()[1] + self.y + self.x_yt[1] + 200))
            if self.sec >= sec + sec1 + sec_end:
                return True
            if self.sec >= sec:
                self.xxyy1 = (self.pos()[0] + self.x + self.x_yt[0], self.pos()[1] + self.y + self.x_yt[1] + 200)
                screen.blit(self.track1, self.xxyy1)
            screen.blit(self.blast1, self.x_y)

    def moving(self, speedx, speedy, b=False):
        self.x += speedx
        self.y += speedy
        if b:
            self.x_y = speedx + self.x_y[0], speedy + self.x_y[1]

    def rotate_to_player(self, blast):
        self.angle = angle = math.degrees(math.atan2((player.x + player.w // 2) - (self.x + self.w // 2), (player.y + player.h // 2) - (self.y + self.h // 2)))
        image = pygame.transform.rotate(blast, angle)
        center = blast.get_rect().center
        rect = image.get_rect(center=center)
        return image, (rect[0] + 8, rect[1] + 8)

    def pos(self):
        a, b = 600, 600
        c = (a ** 2 + b ** 2 - 2 * a * b * math.cos(math.radians(self.angle))) ** 0.5
        if (2 * b * c) == 0:
            F = 0
        else: F = 90 - math.degrees(math.acos((a ** 2 - b ** 2 + c ** 2) / (2 * b * c)))
        if self.angle < 0:
            return (-math.cos(math.radians(F)) * c, -math.sin(math.radians(F)) * c)
        if 0 < self.angle < 90:
            return (math.cos(math.radians(F)) * c, -math.sin(math.radians(F)) * c)
        if 90 <= self.angle < 180:
            return (math.cos(math.radians(F)) * c, -math.sin(math.radians(F)) * c)
        return (math.cos(math.radians(F)) * c, math.sin(math.radians(F)) * c)

    def pos1(self):
        B = -(self.angle - 90)
        x, y = math.cos(math.radians(B)) * 300, math.sin(math.radians(B)) * 300
        return x * 0.9, y * 0.9


class Box():
    def __init__(self, x, y, w, h):
        global pole, pole1
        self.x, self.y, self.w, self.h = x, y, w, h
        pole1 = Surface((self.w + 4, self.h + 4))
        pole = Surface((self.w - 4, self.h - 4))
        self.start()

    def start(self):
        pole.fill(Color("black"))
        self.draw()

    def change_size(self, spw, sph):
        global pole, pole1
        self.x += spw
        self.y += sph
        self.w -= spw * 2
        self.h -= sph * 2
        pole1 = Surface((self.w + 4, self.h + 4))
        pole = Surface((self.w - 4, self.h - 4))
        self.draw()

    def draw(self):
        pygame.draw.rect(pole1, Color("white"), (2, 2, self.w, self.h), 5)

    def surf(self):
        screen.blit(pole1, (self.x, self.y))
        screen.blit(pole, (self.x + 4, self.y + 4))

    def change_pos(self, spw, sph):
        self.x += spw
        self.y += sph
        self.draw()


class Platform():
    def __init__(self, x, y, w, h, type):
        global pole
        self.speedx, self.speedy = 0, 0
        self.x, self.y, self.w, self.h = x, y, w, h
        self.type = type
        self.draw()

    def draw(self):
        pygame.draw.rect(pole, Color(self.type), (self.x, self.y, self.w, self.h))
        self.rect = Rect((self.x, self.y, self.w, self.h))

    def moving(self, spx, spy):
        self.speedx = spx
        self.speedy = spy
        self.x += spx
        self.y += spy
        self.draw()


class AtkList():
    def __init__(self):
        global screen
        global pole
        self.clear()

    def all_atks(self, sec):
        if sec <= 500:
            self.block2()
        #if sec == 500:
        #    self.clear()
        #    player.mode = "blue"
        #    self.flag_fill_screen = True
        #    self.fill_timer = 5
        #    box.change_size(10, 0)
        #    box.change_pos(-5, 0)
#
#        if 1700 >= sec >= 501:
#            self.block1()

    def block1(self):
        self.b1_sec += 1
        if self.b1_sec == 1:
            self.atk1()
        if self.b1_sec >= 1 and self.b1_sec < 150:
            self.bone_str[0].bone_strike(120, "down", 10, 32, 80, False)
        if self.b1_sec == 60:
            self.atk1()
        if self.b1_sec >= 60 and self.b1_sec < 150:
            self.bone_str[1].bone_strike(120, "left", 10, 8, 44, True)
        if self.b1_sec == 100:
            player.mode = "red"
            self.blasters.append(Atk("white", "blaster", 320, 200, 60, 60, False, 360))
            self.blasters.append(Atk("white", "blaster", 420, 280, 60, 60, False, -90))
        if self.b1_sec == 104:
            self.blasters.append(Atk("white", "blaster", 300, 200, 60, 60, False, 360))
            self.blasters.append(Atk("white", "blaster", 420, 300, 60, 60, False, -90))
        if self.b1_sec == 108:
            self.blasters.append(Atk("white", "blaster", 280, 200, 60, 60, False, 360))
            self.blasters.append(Atk("white", "blaster", 420, 320, 60, 60, False, -90))
        if self.b1_sec == 112:
            self.blasters.append(Atk("white", "blaster", 260, 200, 60, 60, False, 360))
            self.blasters.append(Atk("white", "blaster", 420, 340, 60, 60, False, -90))
        if self.b1_sec == 116:
            self.blasters.append(Atk("white", "blaster", 240, 200, 60, 60, False, 360))
            self.blasters.append(Atk("white", "blaster", 420, 360, 60, 60, False, -90))
        if self.b1_sec == 150:
            player.gravity = "down"
            player.mode = "blue"
            self.bones = []
            self.bone_str = []
        if self.b1_sec == 155:
            self.blasters.append(Atk("white", "blaster", 200, 200, 60, 60, False, 360, 1.5, True))
            self.blasters.append(Atk("white", "blaster", 320, 200, 60, 60, False, 360, 1.5, True))
            self.blasters.append(Atk("white", "blaster", 420, 280, 60, 60, False, -90))
            self.blasters.append(Atk("white", "blaster", 420, 400, 60, 60, False, -90))
            self.blasters.append(Atk("white", "blaster", 100, 280, 60, 60, False, 90))
            self.blasters.append(Atk("white", "blaster", 100, 400, 60, 60, False, 90))
        if self.b1_sec == 165:
            player.change_gravity("up", True)
        if 190 <= self.b1_sec <= 195:
            box.change_size(-15, 0)
            box.change_pos(8, 0)
        if self.b1_sec == 200:
            player.change_gravity("right", False)
            for i in range(250):
                self.bones1.append(Atk("white", "bone_s", 260, 250 + i * 15, 10, 120, False, 90))
            self.bones.append(self.bones1)
            self.bones1 = []
            for i in range(50):
                if i < 6:
                    self.bones1.append(Atk("white", "bone_s", -100 - 32 * i, 180 - i * 20, 10, 20 + i * 20, False, 0))
                    self.bones1.append(Atk("white", "bone_s", -100 - 32 * i, 0, 10, 120 - i * 20, False, 0))
                if 11 > i >= 6:
                    j = 11 - i
                    self.bones1.append(Atk("white", "bone_s", -100 - 32 * i, 180 - j * 20, 10, 20 + j * 20, False, 0))
                    self.bones1.append(Atk("white", "bone_s", -100 - 32 * i, 0, 10, 120 - j * 20, False, 0))
                if 16 > i >= 11:
                    j = i - 10
                    self.bones1.append(Atk("white", "bone_s", -140 - 32 * i, 180 - j * 20, 10, 20 + j * 20, False, 0))
                    self.bones1.append(Atk("white", "bone_s", -140 - 32 * i, 0, 10, 120 - j * 20, False, 0))
                if 21 > i >= 16:
                    j = 21 - i
                    self.bones1.append(Atk("white", "bone_s", -140 - 32 * i, 180 - j * 20, 10, 20 + j * 20, False, 0))
                    self.bones1.append(Atk("white", "bone_s", -140 - 32 * i, 0, 10, 120 - j * 20, False, 0))
            self.bones.append(self.bones1)
            self.bones1 = []
        if 580 > self.b1_sec > 200:
            for i in self.bones:
                for j in i:
                    if self.bones.index(i) == 0:
                        j.moving(0, -3)
                    if self.bones.index(i) == 1:
                        j.moving(3, 0)
        if self.b1_sec == 270:
            player.change_gravity("down", True)
        if 535 >= self.b1_sec >= 530:
            box.change_size(15, 0)
            box.change_pos(-8, 0)
        if 545 >= self.b1_sec >= 540:
            box.change_size(0, -15)
            box.change_pos(0, -8)
        if self.b1_sec == 550:
            self.bones = []
            player.change_gravity("up", True)
        if 800 >= self.b1_sec >= 580:
            if self.b1_sec % 20 == 0:
                self.blasters.append(Atk("white", "blaster", 195, 60, 60, 60, False, 360))
                self.blasters.append(Atk("white", "blaster", 330, 60, 60, 60, False, 360))
        if self.b1_sec == 580:
            for i in range(70):
                self.bones1.append(Atk("white", "bone_s", -50 - 15 * i, 50, 10, 400, False, 0))
            self.bones.append(self.bones1)
            self.bones1 = []
            for i in range(50):
                if i < 4:
                    self.bones1.append(Atk("white", "bone_s", 140 - i * 10, -100 - 20 * i, 10, 100 + i * 10, False, 90))
                    self.bones1.append(Atk("white", "bone_s", 0, -100 - 20 * i, 10, 100 - i * 10, False, 90))
                if 4 <= i < 8:
                    j = 8 - i
                    self.bones1.append(Atk("white", "bone_s", 140 - j * 10, -100 - 20 * i, 10, 100 + j * 10, False, 90))
                    self.bones1.append(Atk("white", "bone_s", 0, -100 - 20 * i, 10, 100 - j * 10, False, 90))
                if 8 <= i < 12:
                    j = i - 8
                    self.bones1.append(Atk("white", "bone_s", 140 - j * 10, -100 - 20 * i, 10, 100 + j * 10, False, 90))
                    self.bones1.append(Atk("white", "bone_s", 0, -100 - 20 * i, 10, 100 - j * 10, False, 90))
                if 12 <= i < 16:
                    j = 16 - i
                    self.bones1.append(Atk("white", "bone_s", 140 - j * 10, -100 - 20 * i, 10, 100 + j * 10, False, 90))
                    self.bones1.append(Atk("white", "bone_s", 0, -100 - 20 * i, 10, 100 - j * 10, False, 90))
                if 16 <= i < 20:
                    j = i - 16
                    self.bones1.append(Atk("white", "bone_s", 140 - j * 10, -100 - 20 * i, 10, 100 + j * 10, False, 90))
                    self.bones1.append(Atk("white", "bone_s", 0, -100 - 20 * i, 10, 100 - j * 10, False, 90))
                if 20 <= i < 24:
                    j = 24 - i
                    self.bones1.append(Atk("white", "bone_s", 140 - j * 10, -100 - 20 * i, 10, 100 + j * 10, False, 90))
                    self.bones1.append(Atk("white", "bone_s", 0, -100 - 20 * i, 10, 100 - j * 10, False, 90))
                if 24 <= i < 28:
                    j = i - 24
                    self.bones1.append(Atk("white", "bone_s", 140 - j * 10, -100 - 20 * i, 10, 100 + j * 10, False, 90))
                    self.bones1.append(Atk("white", "bone_s", 0, -100 - 20 * i, 10, 100 - j * 10, False, 90))
            self.bones.append(self.bones1)
            self.bones1 = []
        if 850 >= self.b1_sec >= 580:
            for i in self.bones:
                for j in i:
                    if self.bones.index(i) == 0:
                        j.moving(5, 0)
                    if self.bones.index(i) == 1:
                        j.moving(0, 5)
        if self.b1_sec == 850:
            self.bones = []
            player.mode = "red"
        if 850 <= self.b1_sec <= 855:
            box.change_size(0, 15)
            box.change_pos(0, 8)
        if 853 <= self.b1_sec <= 856:
            box.change_size(-25, 0)
        if 860 <= self.b1_sec <= 1000:
            self.atk2(self.b1_sec)
        if self.b1_sec == 1010:
            for i in range(4):
                self.blasters.append(Atk("white", "blaster", 100 + 105 * i, 200, 60, 60, False, 360))
        if self.b1_sec == 1034:
            for i in range(3):
                self.blasters.append(Atk("white", "blaster", 152 + 105 * i, 200, 60, 60, False, 360))
        if self.b1_sec == 1058:
            for i in range(4):
                self.blasters.append(Atk("white", "blaster", 100 + 105 * i, 200, 60, 60, False, 360))

    def block2(self):
        self.b2_sec += 1
        if self.b2_sec == 1:
            self.atk1()
        if self.b2_sec >= 1 and self.b1_sec <= 30:
            self.bone_str[0].bone_strike(80, "down", 1, 7, 15, True)
        if self.b2_sec == 20:
            for i in range(8):
                self.bones1.append(Atk("white", "bone_s", 5 + box.w + i * 25, 0, 10, 71 - i * 8, False, 0))
            self.bones.append(self.bones1)
            self.bones1 = []
            for i in range(8):
                self.bones1.append(Atk("white", "bone_s", -5 - i * 25, 125 + i * 8, 10, 71 - i * 8, False, 0))
            self.bones.append(self.bones1)
            self.bones1 = []
        if self.b2_sec == 23:
            player.change_gravity("down", True)
        if 20 <= self.b2_sec <= 72:
            for i in self.bones:
                for j in i:
                    if self.bones.index(i) == 1:
                        j.moving(-10, 0)
                    if self.bones.index(i) == 2:
                        j.moving(10, 0)
        if self.b2_sec == 40:
            player.change_gravity("up", True)
            self.blasters.append(Atk("white", "blaster", 100, 270, 60, 60, False, 90))
        if self.b2_sec == 44:
            player.change_gravity("right", True)
        if 48 >= self.b2_sec >= 42:
            box.change_pos(8, 0)
            box.change_size(-10, 0)
        if self.b2_sec == 59:
            player.change_gravity("down", True)
        if self.b2_sec == 60:
            for i in range(3):
                self.bones1.append(Atk("white", "bone_s", 5 - i * 25, 0, 10, 50 - i * 8, False, 0))
            self.bones.append(self.bones1)
            self.bones1 = []
            for i in range(3):
                self.bones1.append(Atk("white", "bone_s", 5 - i * 25, 150 + i * 8, 10, 50 - i * 8, False, 0))
            self.bones.append(self.bones1)
            self.bones1 = []
            self.all_platforms.append(Platform(-280, 120, 80, 10, "green"))
            for i in range(10):
                self.bones1.append(Atk("white", "bone_s", -180 - i * 25, 0, 10, 20, False, 0))
            self.bones.append(self.bones1)
            self.bones1 = []
            for i in range(25):
                self.bones1.append(Atk("white", "bone_s", -180 - i * 25, 170, 10, 20, False, 0))
            self.bones.append(self.bones1)
            self.bones1 = []
            for i in range(85):
                self.bones1.append(Atk("white", "bone_s", -180 - 25 * 25 - i * 25, 0, 10, 20, False, 0))
            self.bones.append(self.bones1)
            self.bones1 = []
            for i in range(11):
                if i % 2 == 1:
                    self.bones1.append(Atk("white", "bone_s", -180 - 25 * 25 - i * 150 - 200, 170, 10, 20, False, 0))
                else:
                    self.bones1.append(Atk("blue", "bone_s", -180 - 25 * 25 - i * 150 - 200, 40, 10, 160, False, 0))
            self.bones.append(self.bones1)
            self.bones1 = []
        if 60 <= self.b2_sec <= 329:
            for i in self.bones:
                for j in i:
                    if self.bones.index(i) in range(2, 10):
                        j.moving(self.speed_b2, 0)
        if self.b2_sec == 314:
            self.bones = []
        if 60 <= self.b2_sec <= 150:
            self.all_platforms[0].moving(self.speed_b2, 0)
        if self.b2_sec == 105:
            player.change_gravity("up", True)
        if self.b2_sec == 77:
            self.blasters.append(Atk("white", "blaster", 300, 150, 60, 60, False, 360))
        if self.b2_sec == 135:
            player.change_gravity("down", True)
        if self.b2_sec == 140:
            self.blasters.append(Atk("white", "blaster", 100, 450, 60, 60, False, 90)) # SMALL!!!
        if 300 <= self.b2_sec <= 305:
            box.change_size(10, 0)
        if 300 <= self.b2_sec <= 308:
            box.change_pos(-18, 0)
        if self.b2_sec == 300:
            self.blasters.append(Atk("white", "blaster", 500, 350, 60, 60, False, -90))
        if self.b2_sec == 300:
            player.change_gravity("left", True)
        if self.b2_sec == 315:
            player.mode = "red"
            for i in range(65):
                self.bones1.append(Atk("white", "bone_s", -30 - i * 25, 0, 10, 20, False, 0))
            self.bones.append(self.bones1)
            self.bones1 = []
            for i in range(65):
                self.bones1.append(Atk("white", "bone_s", -30 - i * 25, 180, 10, 20, False, 0))
            self.bones.append(self.bones1)
            self.bones1 = []
            for i in range(6):
                self.bones1.append(Atk("white", "bone_s", -500 - i * 250, 100, 10, 100, False, 0))
            self.bones.append(self.bones1)
            self.bones1 = []
            for i in range(6):
                self.bones1.append(Atk("white", "bone_s", 500 + i * 250, 0, 10, 100, False, 0))
            self.bones.append(self.bones1)
            self.bones1 = []
        if 315 <= self.b2_sec <= 500:
            for i in self.bones:
                for j in i:
                    if self.bones.index(i) in range(0, 3):
                        j.moving(self.speed_b2, 0)
                    if self.bones.index(i) == 3:
                        j.moving(-self.speed_b2, 0)
        if self.b2_sec == 420:
            self.blasters.append(Atk("white", "blaster", 400, 290, 60, 60, False, -90))
            self.blasters.append(Atk("white", "blaster", 400, 410, 60, 60, False, -90))
        if 380 <= self.b2_sec <= 418:
            box.change_pos(3, 0)



    def atk1(self):
        self.bone_str.append(Atk_comb())

    def atk2(self, sec):
        if sec % 15 == 0:
            self.blasters.append(Atk("white", "blaster", randint(0, 600), randint(0, 600), 60, 60, True))

    def atkx(self, sec):
        for i in range(50):
            colo = randint(0, 2)
            if colo == 0:
                self.bones1.append(Atk("blue", "bone_s", -10 - i * 50, 100, 10, 200, False, 90, 1.05))
            if colo == 1:
                self.bones1.append(Atk("orange", "bone_s", -10 - i * 50, 100, 10, 200, False, 90, 1.05))
            if colo == 2:
                self.bones1.append(Atk("white", "bone_s", -10 - i * 50, 110, 10, 100, False, 0, 1.2))
            self.bones.append(self.bones1)
            self.bones1 = []

    def draw_blasters(self):
        ind = []
        for i in at.blasters:
            if i.draw() == True:
                ind.append(at.blasters.index(i))

        for i in reversed(ind):
            del at.blasters[i]

    def draw_bones(self):
        for i in at.bones:
            for j in i:
                pole.blit(j.bon, (j.x, j.y))
        for i in self.bone_str:
            for j in i.bone:
                pole.blit(j.bon, (j.x, j.y))

    def rotate_screen(self):
        screen.blit(rot(screen, sec)[0], rot(screen, sec)[1])

    def draw_shake(self):
        if self.shaker != []:
            x123, y123 = self.shaker.pop(0), self.shaker.pop(0)
            screen.blit(screen, (x123, y123))

    def clear(self):
        self.bones = []
        self.bones1 = []
        self.blasters = []
        self.bone_str = []
        self.all_platforms = []
        self.b1_sec = 0
        self.b2_sec = 0
        self.speed_b2 = 12
        self.shaker = []
        self.flag_fill_screen = False
        self.fill_timer = 0

    def draw_fill(self):
        if self.fill_timer > 0:
            screen.fill(Color("black"))
            self.fill_timer -= 1


class Atk_comb():
    def __init__(self):
        global pole
        self.sec = 0
        self.bone = []
        self.ya = True

    def bone_strike(self, height, side, sec, sec2, sec3, push=True):
        self.sec += 1
        if self.sec == 1:
            if side == "down" or side == "up":
                self.atk = Surface((box.w, height))
            if side == "left" or side == "right":
                self.atk = Surface((height, box.h))
            player.change_gravity(side, push)
        if sec <= self.sec < sec + sec2:
            if side == "down" or side == "up":
                if self.sec % 6 == 0:
                    pygame.draw.rect(self.atk, Color("red"), (1, 0, box.w, height - 4), 2)
                elif self.sec % 6 == 3:
                    pygame.draw.rect(self.atk, Color("yellow"), (1, 0, box.w - 7, height - 4), 2)
            if side == "left" or side == "right":
                if self.sec % 6 == 0:
                    pygame.draw.rect(self.atk, Color("red"), (0, 1, height - 4, box.h - 7), 2)
                elif self.sec % 6 == 3:
                    pygame.draw.rect(self.atk, Color("yellow"), (0, 1, height - 4, box.h - 7), 2)
        if self.sec == sec + sec2:
            if side == "down":
                for i in range(box.w // 10):
                    self.bone.append(Atk("white", "bone_s", i * 12, box.h, 10, height, False, 0))
            if side == "up":
                for i in range(box.w // 10):
                    self.bone.append(Atk("white", "bone_s", i * 12, 0 - height, 10, height, False, 180))
            if side == "left":
                for i in range(box.h // 10):
                    self.bone.append(Atk("white", "bone_s", 0 - height, i * 12, 10, height, False, 270))
            if side == "right":
                for i in range(box.h // 10):
                    self.bone.append(Atk("white", "bone_s", box.w, i * 12, 10, height, False, 90))
            at.bones.append(self.bone)
        if self.sec > sec + sec2 and self.sec <= sec + sec2 + 5:
            self.ya = False
            if side == "down":
                for i in self.bone:
                    i.moving(0, -(height / 5 - 0.5))
            if side == "up":
                for i in self.bone:
                    i.moving(0, (height / 5 - 1.5))
            if side == "left":
                for i in self.bone:
                    i.moving((height / 5 - 1.5), 0)
            if side == "right":
                for i in self.bone:
                    i.moving(-(height / 5 - 0.5), 0)
        if self.sec > sec + sec2 + sec3 - 5 and self.sec <= sec + sec2 + sec3:
            self.ya = False
            if side == "down":
                for i in self.bone:
                    i.moving(0, (height / 5 - 0.5))
            if side == "up":
                for i in self.bone:
                    i.moving(0, -(height / 5 - 1.5))
            if side == "left":
                for i in self.bone:
                    i.moving(-(height / 5 - 1.5), 0)
            if side == "right":
                for i in self.bone:
                    i.moving((height / 5 - 0.5), 0)

        if self.ya:
            if side == "up":
                pole.blit(self.atk, (0, 1))
            if side == "down":
                pole.blit(self.atk, (0, box.h - height - 2))
            if side == "left":
                pole.blit(self.atk, (1, 1))
            if side == "right":
                pole.blit(self.atk, (box.w - height - 2, 0))


def shaker(power, image):
    x, y = image.get_rect()[0], image.get_rect()[1]
    return [x + 2 * power, y + 2 * power, x - 2 * power, y - 2 * power, x + 2 * power, y - 2 * power, x + 1 * power, y + 1 * power, x, y]

def rot(image, angle, track=False, cor=None):
    center = image.get_rect().center
    if track:
        center = (cor[0], cor[1] + 400)
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center = center)
    return rotated_image, (new_rect[0], new_rect[1])

def change_scale(image, f1=1, f2=1, t=False):
    global n, screen
    size = image.get_size()
    if image == blue_up or image == blue_down or image == blue_up or image == blue_right or image == blue_left:
        bigger_img = pygame.transform.scale(image, (int(size[0] * n // f1), int(size[1] * n // f2)))
    else:
        bigger_img = pygame.transform.scale(image, (int(size[0] * n // f1), int(size[1] * n // f2))).convert()
    return bigger_img

def set_color(img, color):
    for x in range(img.get_width()):
        for y in range(img.get_height()):
            color.a = img.get_at((x, y)).a
            img.set_at((x, y), color)


if __name__ == '__main__':
    n = 2
    g = 0.2
    sec = 0
    fps = 30
    size = (600, 600)
    wx1, wy1, w2, h2 = 200, 300, 200, 200
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(size)
    screen.fill(Color("black"))

    track = pygame.image.load("resours/Track.png").convert()
    blast = pygame.image.load("resours/Blaster1.png").convert()
    blast_open = pygame.image.load("resours/Blaster_open1.png").convert()
    blast_open2 = pygame.image.load("resours/Blaster_open2.png").convert()
    blast_open3 = pygame.image.load("resours/Blaster_open3.png").convert()
    red_soul = pygame.image.load("resours/Red_soul.png").convert()
    blue_down = pygame.image.load("resours/Blue_soul_down.png")
    blue_up = pygame.image.load("resours/Blue_soul_up.png")
    blue_left = pygame.image.load("resours/Blue_soul_left.png")
    blue_right = pygame.image.load("resours/Blue_soul_right.png")

    ## Большие кости ##
    bone_white = pygame.image.load("resours/Bone_big.png")
    bone_white_rot = pygame.image.load("resours/Bone_rot_big.png")
    bone_blue = pygame.image.load("resours/Bone_blue.png")
    bone_blue_rot = pygame.image.load("resours/Bone_blue_rot.png")
    bone_orange = pygame.image.load("resours/Bone_orange.png")
    bone_orange_rot = pygame.image.load("resours/Bone_orange_rot.png")

    ## Разделённые кости ##
    bone_up = pygame.image.load("resours/Bone_up.png").convert()
    bone_middle = pygame.image.load("resours/Bone_middle.png").convert()
    bone_down = pygame.image.load("resours/Bone_down.png").convert()
    bone_up_orange = pygame.image.load("resours/Bone_up_orange.png").convert()
    bone_middle_orange = pygame.image.load("resours/Bone_middle_orange.png").convert()
    bone_down_orange = pygame.image.load("resours/Bone_down_orange.png").convert()
    bone_up_blue = pygame.image.load("resours/Bone_up_blue.png").convert()
    bone_middle_blue = pygame.image.load("resours/Bone_middle_blue.png").convert()
    bone_down_blue = pygame.image.load("resours/Bone_down_blue.png").convert()

    player = Player()
    at = AtkList()
    box = Box(wx1, wy1, w2, h2)
    pygame.display.flip()

    while 1:
        clock.tick(fps)
        pygame.display.set_caption(f"Fps {clock.get_fps()}")
        sec += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
###########
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    player.change_gravity("up")
                if event.key == pygame.K_a:
                    player.change_gravity("left")
                if event.key == pygame.K_s:
                    player.change_gravity("down")
                if event.key == pygame.K_d:
                    player.change_gravity("right")
##########
        press = pygame.key.get_pressed()
        if press[pygame.K_LEFT]:
            player.movement(-1, 0, "right")
        elif not(press[pygame.K_LEFT]):
            player.jum("right")
        if press[pygame.K_RIGHT]:
            player.movement(1.2, 0, "left")
        elif not(press[pygame.K_RIGHT]):
            player.jum("left")
        if press[pygame.K_DOWN]:
            player.movement(0, 1.2, "up")
        elif not(press[pygame.K_DOWN]):
            player.jum("up")
        if press[pygame.K_UP]:
            player.movement(0, -1, "down")
        elif not(press[pygame.K_UP]):
            player.jum("down")

        if (not(press[pygame.K_LEFT]) and not(press[pygame.K_RIGHT]) and
            not(press[pygame.K_DOWN]) and not(press[pygame.K_UP])):
            player.move = False
        if press[pygame.K_UP] and press[pygame.K_DOWN]:
            player.move = False
        if press[pygame.K_RIGHT] and press[pygame.K_LEFT]:
            player.move = False

        if player.ret_type() == "blue":
            player.phizic(g)

        player.check_box1()
        screen.fill(Color("black"))
        box.start()
        at.all_atks(sec)
        at.draw_bones()
        box.surf()
        at.draw_blasters()

        player.hit()
        player.draw_player()
        at.draw_shake()
        at.draw_fill()

        pygame.display.flip()
