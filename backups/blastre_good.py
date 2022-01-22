import pygame, sys, math, time

from pygame.locals import *
from pygame import Color, Rect, Surface


class Player():
    def __init__(self):
        self.move = False
        self.f = 1.5
        self.x, self.y, self.speed, self.w, self.h = 290, 390, 120, 16 * n // self.f, 16 * n // self.f
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
        if self.mode == "red":
            pl = pygame.image.load("resours/Red_soul.png")
        elif self.mode == "blue":
            if self.gravity == "down":
                pl = pygame.image.load("resours/Blue_soul_down.png")
            elif self.gravity == "up":
                pl = pygame.image.load("resours/Blue_soul_up.png")
            elif self.gravity == "left":
                pl = pygame.image.load("resours/Blue_soul_left.png")
            elif self.gravity == "right":
                pl = pygame.image.load("resours/Blue_soul_right.png")
        pl = change_scale(pl, self.f, self.f)
        screen.blit(pl, (self.x, self.y))
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
        for i in all_platforms:
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
                if self.gravity == "right":
                    self.speedfall = -40
                else:
                    self.speedfall = 40
            else:
                self.speedfall = 0
            self.g = -self.start_g
        elif self.gravity == "up" or self.gravity == "left":
            if fast:
                if self.gravity == "left":
                    self.speedfall = 40
                else:
                    self.speedfall = -40
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
        f = False
        for i in at.bones:
            for j in i:
                if self.rect.colliderect(j.rect):
                    if j.color == "white":
                        f = True
                    if j.color == "blue" and (self.move or self.speedfall != 0):
                        f = True
                    if j.color == "orange" and self.move == False and self.speedfall == 0:
                        f = True
        if f:
            self.hp -= 1
            print(self.hp)


class Atk():
    def __init__(self, col, type, x, y, w, h, topl=True, an=90, f=1.5):
        self.x, self.y, self.h, self.w = x, y, h, w
        self.color = col
        self.type = type
        self.topl = topl
        self.an = an
        self.sec = 0
        self.a = 0.5
        self.f = f
        if type == "blaster":
            self.blast = change_scale(pygame.image.load("resours/Blaster1.png"))
            f0, f0, self.w, self.h = self.blast.get_rect()
            self.blast1 = Surface((self.h + 20, self.w * 2 + 20), pygame.SRCALPHA, 32).convert_alpha()
            self.track = change_scale(pygame.image.load("resours/Track.png").convert(), self.f)
            self.track01 = change_scale(pygame.image.load("resours/Track.png").convert(), self.f * 0.8)
            self.track02 = change_scale(pygame.image.load("resours/Track.png").convert(), self.f * 0.6)
            self.track1 = Surface((4000, 4000), pygame.SRCALPHA, 32).convert_alpha()
            self.track2 = Surface((4000, 4000), pygame.SRCALPHA, 32).convert_alpha()
            self.track3 = Surface((4000, 4000), pygame.SRCALPHA, 32).convert_alpha()
            self.track.set_colorkey((0, 0, 0))
        self.draw()

    def draw(self, sec=20, sec1=0, sec_end=30):
        global screen
        global n
        self.sec += 1
        if self.type == 'bone':
            if self.col == "white":
                bon = pygame.image.load("resours/Bone_big.png")
            pole.blit(bon, (self.x, self.y))
            self.rect = Rect(self.x + box.x, self.y + box.y, self.w, self.h)

        if self.type == "blaster":
            if self.sec == 1:
                if self.topl:
                    self.blast1.blit(self.rotate_to_player(self.blast)[0], self.rotate_to_player(self.blast)[1])
                else:
                    self.blast1.blit(rot(self.blast, self.an)[0], rot(self.blast, self.an)[1])
                    self.angle = self.an
            if self.sec == sec:
                self.blast = change_scale(pygame.image.load("resours/Blaster_open1.png"))
                self.blast1.blit(rot(self.blast, self.angle)[0], rot(self.blast, self.angle)[1])
                self.track1.blit(rot(self.track, self.angle, True, (self.w // 2, self.h // 2))[0], rot(self.track, self.angle, True, (self.w // 2, self.h // 2))[1])
                self.track01.blit(rot(self.track2, self.angle, True, (self.w // 2, self.h // 2))[0], rot(self.track2, self.angle, True, (self.w // 2, self.h // 2))[1])
                self.track02.blit(rot(self.track3, self.angle, True, (self.w // 2, self.h // 2))[0], rot(self.track3, self.angle, True, (self.w // 2, self.h // 2))[1])
            if self.sec > sec + sec1:
                B = -(self.angle - 90)
                x, y = math.cos(math.radians(B)) * 300, math.sin(math.radians(B)) * 300
                self.moving(-x / fps * self.a, -y / fps * self.a)
                self.a += 0.0027 * (sec + sec1 + sec_end)
            if self.sec >= sec + sec1 + sec_end:
                self.stop()
                return
            screen.blit(self.track1, (self.x - 2000 + self.pos()[0] + self.pos1()[0], self.y - 1800 + self.pos()[1] + self.pos1()[1],))
            print(self.x, self.y + 300)
            screen.blit(self.blast1, (self.x, self.y))

    def moving(self, speedx, speedy):
        self.x += speedx
        self.y += speedy

    def rotate_to_player(self, blast):
        self.angle = angle = math.degrees(math.atan2((player.x + player.w // 2) - (self.x + self.w // 2), (player.y + player.h // 2) - (self.y + self.h // 2)))
        image = pygame.transform.rotate(blast, angle)
        center = blast.get_rect().center
        rect = image.get_rect(center=center)
        return image, (rect[0] + 8, rect[1] + 8)

    def pos(self):
        a, b = 600, 600
        c = (a ** 2 + b ** 2 - 2 * a * b * math.cos(math.radians(self.angle))) ** 0.5
        F = 90 - math.degrees(math.acos((a ** 2 - b ** 2 + c ** 2) / (2 * b * c)))
        if self.angle < 0:
            return (-math.cos(math.radians(F)) * c, -math.sin(math.radians(F)) * c)
        if 0 < self.angle < 90:
            return (math.cos(math.radians(F)) * c, -math.sin(math.radians(F)) * c)
        if 90 <= self.angle < 180:
            return (math.cos(math.radians(F)) * c, -math.sin(math.radians(F)) * c)
        return (math.cos(math.radians(F)) * c, math.sin(math.radians(F)) * c)

    def stop(self):
        pass

    def pos1(self):
        B = -(self.angle - 90)
        x, y = math.cos(math.radians(B)) * 300, math.sin(math.radians(B)) * 300
        return x * 0.9, y * 0.9


class AtkList():
    def __init__(self):
        self.bones = []
        self.bones1 = []

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

def rot(image, angle, track=False, cor=None):
    center = image.get_rect().center
    if track:
        center = (cor[0] + 2000, cor[1] + 2400)
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center = center)
    return rotated_image, (new_rect[0] + 8, new_rect[1] + 8)

def change_scale(image, f1=1, f2=1):
    global n, screen
    size = image.get_size()
    bigger_img = pygame.transform.scale(image, (int(size[0] * n // f1), int(size[1] * n // f1)))
    return bigger_img


if __name__ == '__main__':
    n = 2
    all_platforms = []
    secs = 0
    an = 1
    pygame.init()
    size = (600, 600)
    fps = 30
    wx1, wy1, w2, h2 = 200, 300, 200, 200
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(size)
    screen.fill(Color("black"))
    player = Player()
    at = AtkList()
    box = Box(wx1, wy1, w2, h2)
    g = 0.2
    blas = Atk("white", "blaster", 300, 360, 42, 57, False, -15)
    pygame.display.flip()
    while 1:
        clock.tick(fps)
        secs += 1
        #print(secs)
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
        an += 5
        screen.fill(Color("black"))
        box.start()
        box.surf()
        player.hit()
        blas.draw()
        player.draw_player()
        pygame.display.flip()
