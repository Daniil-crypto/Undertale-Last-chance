import pygame, sys, math, time

from pygame.locals import *
from pygame import Color, Rect, Surface


class Player():
    def __init__(self):
        self.x, self.y, self.speed, self.w, self.h = 290, 390, 120, 20, 20
        self.gravity = "up"
        self.mode = "blue"
        self.color = "blue"
        self.speedfall = 1
        self.jumping = False
        self.start_g = 15
        if self.gravity == "down" or self.gravity == "right":
            self.g = -self.start_g
        elif self.gravity == "up" or self.gravity == "left":
            self.g = self.start_g
        self.hp = 92
        self.draw_player()

    def draw_player(self):
        pygame.draw.rect(screen, Color(self.color), (self.x, self.y, self.w, self.h))
        self.rect = Rect(self.x, self.y, self.w, self.h)

    def box_check(self, wx1, wx2, wy1, wy2, f):
        global fps
        xev, yev = False, False
        if self.x > wx1 + self.speed / fps and f == 1:
            xev = True
        if self.x < wx2 - self.w - self.speed / fps and f == 2:
            xev = True
        if self.y < wy2 - self.w - 6 and f == 3:
            yev = True
        if self.y > wy1 + self.speed / fps and f == 4:
            yev = True
        return xev, yev

    def movement(self, ksx=0, ksy=0, keyn="down"):
        global fps
        global g
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
                print(self.g)
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
        global wy2, wy1
        f = False
        if self.y > wy2 - self.w - 6 and self.gravity == "down":
            f = True
        if self.y < wy1 + 6 and self.gravity == "up":
            f = True
        if self.x > wx2 - self.h - 6 and self.gravity == "right":
            f = True
        if self.x < wx1 + 6 and self.gravity == "left":
            f = True
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

    def change_gravity(self, new_g, fast=False):
        self.gravity = new_g
        self.jumping = False
        if self.gravity == "down" or self.gravity == "right":
            if fast:
                if self.gravity == "right":
                    self.speedfall = -30
                else:
                    self.speedfall = 30
            else:
                self.speedfall = 0
            self.g = -self.start_g
        elif self.gravity == "up" or self.gravity == "left":
            if fast:
                if self.gravity == "left":
                    self.speedfall = 30
                else:
                    self.speedfall = -30
            else:
                self.speedfall = 0
            self.g = self.start_g

    def check_box1(self):
        if self.x < wx1 + 5:
            self.x = wx1 + 5
        if self.x > wx2 - 5 - self.w:
            self.x = wx2 - 5 - self.w
        if self.y < wy1 + 5:
            self.y = wy1 + 5
        if self.y > wy2 - 5 - self.h:
            self.y = wy2 - 5 - self.h



class Atk():
    def __init__(self, col, type, x, y, w, h):
        self.x, self.y, self.h, self.w = x, y, h, w
        self.color = Color(col)
        self.type = type
        self.draw()

    def draw(self):
        if self.type == 'bone':
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.w, self.h))
            self.rect = Rect(self.x, self.y, self.w, self.h)

    def moving(self, speedx, speedy):
        self.x += speedx
        self.y += speedy
        self.draw()


class AtkList():
    def __init__(self):
        pass

    def atk1konf(self):
        for i in range(50):
            bones.append(Atk("white", "bone", 100 - i * 50, 400, 10, 100))
            bones1.append(Atk("white", "bone", 500 + i * 80, 300, 10, 100))

if __name__ == '__main__':
    pygame.init()
    size = (600, 600)
    fps = 30
    wx1, wy1, w2, h2 = 100, 300, 400, 200
    wy2, wx2 = wy1 + h2, wx1 + w2
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(size)
    screen.fill(Color("black"))
    player = Player()
    g = 0.2
    bones = []
    bones1 = []
    pygame.display.flip()
    while 1:
        clock.tick(fps)
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
            if player.box_check(wx1, wx2, wy1, wy2, 1)[0]:
                player.movement(-1, 0, "right")
        elif not(press[pygame.K_LEFT]):
            player.jum("right")
        if press[pygame.K_RIGHT]:
            if player.box_check(wx1, wx2, wy1, wy2, 2)[0]:
                player.movement(1.2, 0, "left")
        elif not(press[pygame.K_RIGHT]):
            player.jum("left")
        if press[pygame.K_DOWN]:
            if player.box_check(wx1, wx2, wy1, wy2, 3)[1]:
                player.movement(0, 1.2, "up")
        elif not(press[pygame.K_DOWN]):
            player.jum("up")
        if press[pygame.K_UP]:
            if player.box_check(wx1, wx2, wy1, wy2, 4)[1]:
                player.movement(0, -1, "down")
        elif not(press[pygame.K_UP]):
            player.jum("down")

        if player.ret_type() == "blue":
            player.phizic(g)

        player.check_box1()

        screen.fill(Color("black"))
        pygame.draw.rect(screen, Color("white"), (wx1, wy1, w2, h2), 5)
        player.draw_player()
        pygame.display.flip()
