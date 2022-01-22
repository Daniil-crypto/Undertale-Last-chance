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
        self.start_g = 10
        if self.gravity == "down" or self.gravity == "right":
            self.g = -self.start_g
        elif self.gravity == "up" or self.gravity == "left":
            self.g = self.start_g
        self.hp = 92
        self.draw_player()

    def draw_player(self):
        pygame.draw.rect(screen, Color(self.color), (self.x, self.y, self.w, self.h))
        self.rect = Rect(self.x, self.y, self.w, self.h)


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
        if self.x < box.x + 5:
            self.x = box.x + 5
        if self.x > box.x + box.w - 5 - self.w:
            self.x = box.x + box.w - 5 - self.w
        if self.y < box.y + 5:
            self.y = box.y + 5
        if self.y > box.y + box.h - 5 - self.h:
            self.y = box.y + box.h - 5 - self.h

    def hit(self):
        for i in bones:
            if self.rect.colliderect(i.rect):
                self.hp -= 1
                print(self.hp)
        for i in bones1:
            if self.rect.colliderect(i.rect):
                self.hp -= 1
                print(self.hp)


class Atk():
    def __init__(self, col, type, x, y, w, h):
        self.x, self.y, self.h, self.w = x, y, h, w
        self.color = Color(col)
        self.type = type
        self.draw()

    def draw(self, sec=0):
        if self.type == 'bone':
            pygame.draw.rect(pole, self.color, (self.x, self.y, self.w, self.h))
            self.rect = Rect(self.x + box.x, self.y + box.y, self.w, self.h)
        if self.type == "blaster":
            pass

    def moving(self, speedx, speedy):
        self.x += speedx
        self.y += speedy
        self.draw()


class AtkList():
    def __init__(self):
        pass

    def atk1konf(self):
        for i in range(50):
            bones.append(Atk("white", "bone", 0 - i * 80, 100, 10, 100))
            bones1.append(Atk("white", "bone", 500 + i * 50, 0, 10, 100))

    def atk1(self):
        for i in bones:
            i.moving(3, 0)
        for i in bones1:
            i.moving(-3, 0)


class Box():
    def __init__(self, x, y, w, h):
        global pole
        self.x, self.y, self.w, self.h = x, y, w, h
        pole = pygame.Surface((self.w + 4, self.h + 4))
        self.start()

    def start(self):
        pole.fill(Color("black"))
        self.draw()

    def change_size(self, spw, sph):
        global pole
        self.x += spw
        self.y += sph
        self.w -= spw * 2
        self.h -= sph * 2
        pole = pygame.Surface((self.w + 4, self.h + 4))

    def draw(self):
        pygame.draw.rect(pole, Color("white"), (2, 2, self.w, self.h), 5)

    def surf(self):
        screen.blit(pole, (self.x, self.y))

    def change_pos(self, spw, sph):
        self.x += spw
        self.y += sph


def rot(image, angle):
    center = image.get_rect().center
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center = center)
    return rotated_image, new_rect


if __name__ == '__main__':
    secs = 0
    an = 0
    pygame.init()
    size = (600, 600)
    fps = 30
    wx1, wy1, w2, h2 = 100, 300, 400, 200
    wy2, wx2 = wy1 + h2, wx1 + w2
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(size)
    screen.fill(Color("black"))
    player = Player()
    at = AtkList()
    box = Box(wx1, wy1, w2, h2)
    g = 0.2
    bones = []
    bones1 = []
    pygame.display.flip()
    while 1:
        clock.tick(fps)
        secs += 1
        print(secs)
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

        if player.ret_type() == "blue":
            player.phizic(g)


        player.check_box1()
        an += 2
        screen.fill(Color("black"))
        box.start()
        box.surf()
        player.hit()
        player.draw_player()
        pygame.display.flip()
