import pygame, sys, math, time

from pygame.locals import *
from pygame import Color, Rect, Surface


class Player():
    def __init__(self):
        self.x, self.y, self.speed, self.w, self.h = 290, 390, 120, 20, 20
        self.gravity = "down"
        self.mode = "blue"
        self.color = "blue"
        self.speedfall = 1
        self.jumping = False
        self.g = -10
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
        if self.y < wy2 - self.w - 5 and f == 3:
            yev = True
        if self.y > wy1 + self.speed / fps and f == 4:
            yev = True
        return xev, yev

    def movement(self, ksx=0, ksy=0, keynum=""):
        global fps
        global g
        if self.mode == "red":
            self.x, self.y = self.x + self.speed * ksx // fps, self.y + self.speed * ksy // fps
        elif self.mode == "blue":
            if self.gravity == "down" or self.gravity == "up":
                self.x += self.speed * ksx // fps
            elif self.gravity == "left" or self.gravity == "right":
                self.y += self.speed * ksy // fps
            if jump == True and self.collision():
                self.jumping = True
                self.phizic(-1)
            if self.jumping and jump:
                self.phizic(self.g)
                self.speedfall = 0
                if self.g >= 0:
                    self.jumping = False
                    self.g = -10
                    return
                self.g += 0.4

    def phizic(self, g):
        if self.jumping:
            self.y += g
        elif self.collision() == False:
            self.speedfall += g
            self.y += self.speedfall
        else:
            self.speedfall = 0

    def collision(self, y=None):
        global wy2
        f = False
        if self.y > wy2 - self.w - 6:
            f = True
        return f

    def ret_type(self):
        return self.mode


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
    g = 0.2
    player = Player()
    bones = []
    bones1 = []
    pygame.display.flip()
    while 1:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
        press = pygame.key.get_pressed()
        if press[pygame.K_LEFT]:
            if player.box_check(wx1, wx2, wy1, wy2, 1)[0]:
                player.movement(-1, 0, 1)
        if press[pygame.K_RIGHT]:
            if player.box_check(wx1, wx2, wy1, wy2, 2)[0]:
                player.movement(1.2, 0, 2)
        if press[pygame.K_DOWN]:
            if player.box_check(wx1, wx2, wy1, wy2, 3)[1]:
                player.movement(0, 1.2, 3)
        if press[pygame.K_UP]:
            if player.box_check(wx1, wx2, wy1, wy2, 4)[1]:
                player.movement(0, -1, 4)
        elif not(press[pygame.K_UP]):
            player.jumping = False
            player.g = -10

        if player.ret_type() == "blue":
            player.phizic(g)

        screen.fill(Color("black"))
        pygame.draw.rect(screen, Color("white"), (wx1, wy1, w2, h2), 5)
        player.draw_player()
        pygame.display.flip()
