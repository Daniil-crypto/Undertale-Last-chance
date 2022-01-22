import pygame, sys, math, time, os

from pygame.locals import *
from random import randint
from pygame import Color, Rect, Surface


class Player():
    def __init__(self):
        global hit_s, hit1_s, blim_s
        self.move = False
        self.f = 1.5
        self.x, self.y, self.speed, self.w, self.h = 290, 390, 120, 16 * n // self.f, 16 * n // self.f
        self.gravity = "down"
        self.mode = "red"
        self.speedfall = 1
        self.jumping = False
        self.start_g = 10
        self.shake_flag = False
        self.new_side = 0
        self.new_sides = []
        self.sec_d = 0
        self.all_part = []
        if self.gravity == "down" or self.gravity == "right":
            self.g = -self.start_g
        elif self.gravity == "up" or self.gravity == "left":
            self.g = self.start_g
        self.hp = 92
        self.krhp = 92
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
                    sans.hand_right_bool = True
                else:
                    self.speedfall = 40
                    sans.hand_down_bool = True
            else:
                self.speedfall = 0
            self.g = -self.start_g
        elif self.gravity == "up" or self.gravity == "left":
            if fast:
                self.shake_flag = True
                if self.gravity == "left":
                    self.speedfall = 40
                    sans.hand_right_bool = True
                else:
                    self.speedfall = -40
                    sans.hand_up_bool = True
            else:
                self.speedfall = 0
            self.g = self.start_g
        self.new_sides.append(0)

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
            hit1_s.stop()
            hit1_s.play()

        if f:
            hit_s.stop()
            hit_s.play()

        if self.hp <= 0:
            self.hp = 0

    def change_color(self, sound=True):
        for i in range(len(self.new_sides)):
            if self.new_sides[i] == 0:
                self.new_sides[i] = 1
                if sound:
                    blim_s.play()
            if self.new_sides[i] < 25:
                player1 = change_scale(self.pl, 1 / (self.new_sides[i] * 0.1), 1 / (self.new_sides[i] * 0.1)).convert_alpha()
                player1.set_colorkey((0, 0, 0))
                player1.fill((255, 0, 255, 255 - self.new_sides[i] * 10.666), special_flags=pygame.BLEND_RGBA_MULT) ###
                x, y = self.x - player1.get_rect()[2] // 2 + 9, self.y - player1.get_rect()[3] // 2 + 9

                screen.blit(player1, (x, y))
            self.new_sides[i] += 1

    def check_death(self):
        global sec, at, broken_soul, red_soul, break1_s, break2_s, GO, death, file, f1
        if self.hp <= 0:
            sec = -2
            self.sec_d += 1
            if self.sec_d == 1:
                pygame.mixer.stop()
                pygame.mixer.music.stop()
                at = AtkList()
                self.pl = change_scale(red_soul, self.f, self.f)
                self.alpha = 0
            if 1 <= self.sec_d:
                screen.fill(Color("black"))
                death_count = f1.render(f" - {death}", False, Color("red"))
                if self.sec_d >= 100:
                    death_count.set_alpha(755 - self.sec_d * 5)
                screen.blit(death_count, (self.x + 25, self.y))
            if self.sec_d == 120:
                pygame.mixer.music.load("music/game_over.mp3")
                pygame.mixer.music.play(-1)

            if self.sec_d > 120:
                self.alpha += 5
                if self.alpha >= 255:
                    self.alpha = 255

                GO.set_alpha(self.alpha)
                screen.blit(GO, (50, 0))
            if self.sec_d < 70:
                screen.blit(self.pl, (self.x, self.y))
            if self.sec_d == 30:
                self.pl = change_scale(broken_soul, self.f, self.f)
                self.x -= 3
                break1_s.play()
            if self.sec_d == 70:
                death += 1
                file[0] = str(death)
                open("resours\data.txt", "w").write("\n".join(file))
                break2_s.play()
                for i in range(6):
                    self.all_part.append(Particle([self.x, self.y]))
            if 400 > self.sec_d > 70:
                for i in self.all_part:
                    i.move()
            return True
        return False



class Particle():
    def __init__(self, pos):
        global soul_part1, screen, soul_parts
        self.step, self.sec = 0, 0
        self.im = soul_part1
        self.speed_x, self.speed_y = randint(-5, 5), randint(-15, 2)
        self.g = 0.2
        self.x, self.y = pos

    def move(self):
        if self.sec % 5 == 0:
            self.step += 1
            if self.step == len(soul_parts):
                self.step = 0
            self.im = soul_parts[self.step]
        self.sec += 1
        self.speed_y += self.g
        self.x += self.speed_x
        self.y += self.speed_y
        screen.blit(self.im, (self.x, self.y))



class Atk():
    def __init__(self, col, type, x, y, w, h, topl=False, an=90, f=1.5, shak=False, new123=False):
        global track, blast, blast_open, blaster_end_s, blaster_start_s
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
            blaster_start_s.play()
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
                blaster_start_s.stop()
                blaster_end_s.play()
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
        self.change()
        self.start()

    def start(self):
        global pole1
        self.change()
        pole1.fill(Color("black"))
        self.draw()

    def change_size(self, spw, sph):
        global pole, pole1
        self.x += spw
        self.y += sph
        self.w -= spw * 2
        self.h -= sph * 2
        self.draw()

    def draw(self):
        pygame.draw.rect(pole1, Color("white"), (2, 2, self.w, self.h), 5)

    def surf(self):
        screen.blit(pole1, (self.x, self.y))
        screen.blit(pole, (self.x + 4, self.y + 4))
        self.draw()

    def change_pos(self, spw, sph):
        self.x += spw
        self.y += sph
        self.draw()

    def change(self):
        global pole1, pole
        pole1 = Surface((self.w + 4, self.h + 4))
        pole = Surface((self.w - 4, self.h - 4))



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
        global screen, pole, sans, bam, tors_1, tors_2, face, face_eye, face_ser, legs
        self.clear()

    def all_atks(self, sec):
        self.c_h_bool = False
        if sec == -1:
            return
        if 0 < sec < 255:
            screen.set_alpha(sec)
        if sec == 430:
            sans.face = face_ser
            at.change = True
            bam.play()
        if sec == 445:
            at.change = False
            bam.play()
        if 240 <= sec < 420:
            if sec % 60 == 20:
                player.new_sides.append(0)
                player.change_color(False)
        if sec == 230:
            diologs.txt, diologs.time, diologs.txt1 = "it's a beautiful day\noutside.", 0, ""
        if 230 <= sec < 295:
            diologs.draw_all(340, 150)
        if sec == 295:
            diologs.txt, diologs.time, diologs.txt1, diologs.txt2 = "birds are sining.\nflowers are blooming...", 0, "", ""
            diologs.next, diologs.stop = False, False
        if 295 <= sec < 370:
            diologs.draw_all(340, 150)
        if sec == 380:
            diologs.txt, diologs.time, diologs.txt1, diologs.txt2 = "on days like this.\nkids like you...", 0, "", ""
            diologs.next, diologs.stop = False, False
        if 370 <= sec < 430:
            diologs.draw_all(340, 150)
        if sec == 445:
            diologs.txt, diologs.time, diologs.txt1, diologs.txt2 = "SHOOLD BE BOORNING\nIN HELL.", 0, "", ""
            diologs.next, diologs.stop = False, False
        if 445 <= sec < 498:
            diologs.draw_all(340, 150, False)
        if 455 <= sec < 480:
            self.c_h = (sec - 455) * 40
            self.c_h_bool = True
            self.c_x, self.c_y = -(sec - 455) * 40 / 2, -(sec - 455) * 40 / 2 + (sec - 455) * 10
        if sec == 500:
            sans.mov = True
        if 480 <= sec <= 505:
            self.c_h = -(sec - 505) * 40
            self.c_h_bool = True
            self.c_x, self.c_y = (sec - 505) * 40 / 2, (sec - 505) * 40 / 2 + -(sec - 505) * 10
        if 500 <= sec <= 1000:
            self.block2()
        if sec == 1030:
            sans.face = face_ser
            sans.tors = tors_2
            sans.x_t -= 18
            sans.y_t += 2

    def block1(self):
        self.b1_sec += 1
        if self.b1_sec == 1:
            at.blok = True
            player.mode = "blue"
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
            player.mode = "blue"
            self.blok = True
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
            sans.x -= 30
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
        if self.b2_sec == 300:
            sans.face = face[3]
        if 300 <= self.b2_sec <= 305:
            box.change_size(10, 0)
            sans.x += 65
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
            self.blasters.append(Atk("white", "blaster", 400, 290, 60, 60, False, -90, 1.5, True))
            self.blasters.append(Atk("white", "blaster", 400, 410, 60, 60, False, -90, 1.5, True))
        if 380 <= self.b2_sec <= 418:
            box.change_pos(3, 0)
            box.w -= 20 / 38
        if 410 <= self.b2_sec <= 418:
            sans.x -= 20
        if self.b2_sec == 410:
            sans.face = face[1]



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
        self.blok = False
        self.change = False

    def draw_fill(self):
        if self.fill_timer > 0:
            screen.fill(Color("black"))
            self.fill_timer -= 1

    def change_screen_scale(self):
        global screen
        if self.c_h_bool:
            screen_n = pygame.transform.scale(screen, (600 + self.c_h, 600 + self.c_h))
            screen.fill(Color("black"))
            screen.blit(screen_n, (self.c_x, self.c_y))


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
    bigger_img = pygame.transform.scale(image, (int(size[0] * n // f1), int(size[1] * n // f2))).convert()
    return bigger_img


def restart():
    global n, g, name, sec, fps, size, wx1, wy1, w2, h2, screen, player, at, box, sans, diologs
    n = 2
    g = 0.2
    name = "CHARA"
    sec = 0
    fps = 29
    size = (600, 600)
    wx1, wy1, w2, h2 = 200, 300, 200, 200
    screen.fill(Color("black"))
    player = Player()
    at = AtkList()
    sans = Sans()
    box = Box(wx1, wy1, w2, h2)
    diologs = Diologs()
    pygame.mixer.music.load("music/megalovania.mp3")
    pygame.mixer.music.play(-1)
    pygame.display.flip()

def change_screen():
    global scr, screen, screen1, size
    if scr == "small":
        scr = "full"
        screen1 = pygame.display.set_mode((1920, 1080), pygame.NOFRAME)
    elif scr == "full":
        scr = "small"
        screen1 = pygame.display.set_mode(size)


class Sans():
    def __init__(self):
        global tors_1, tors_2, face, face_eye, face_ser, legs, screen, hand_down
        self.sans = Surface((200, 200), pygame.SRCALPHA, 32)
        self.x, self.y = 215, 140
        self.x_f, self.y_f = 50, 13
        self.x_t, self.y_t = 28, 61
        self.x_l, self.y_l = 40, 110
        self.face = face[4]
        self.tors = tors_1
        self.mov = False
        self.face_move = [12, 12, 13, 13]
        self.face_move2 = [11, 15, 20, 15, 11]
        self.body_move = []
        self.time = 0
        self.hand_time = 0
        self.hand_down_bool = False
        self.hand_up_bool = False
        self.hand_right_bool = False

    def draw(self):
        self.sans = Surface((200, 200), pygame.SRCALPHA, 32)
        if self.hand_down_bool == True:
            self.hand_down()
            self.sans.blit(self.body, (25, 15))
        elif self.hand_up_bool == True:
            self.hand_up()
            self.sans.blit(self.body, (25, 15))
        elif self.hand_right_bool == True:
            self.hand_right()
            self.sans.blit(self.body, (15, 60))
        else:
            self.sans.blit(self.tors, (self.x_t, self.y_t))
            self.sans.blit(legs, (self.x_l, self.y_l))
        self.sans.blit(self.face, (self.x_f, self.y_f))
        screen.blit(self.sans, (self.x, self.y))

    def move_body(self):
        if self.mov:
            self.time += 1
            if self.time % 5 == 0:
                self.y_f = self.face_move[self.time % 4]
                if self.time % 40 < 20:
                    self.x_t -= 1
                    self.x_f -= 1
                else:
                    self.x_t += 1
                    self.x_f += 1
                if self.time % 2 == 0:
                    if self.time % 20 < 10:
                        self.y_t -= 1
                        self.y_f -= 0.5
                    else:
                        self.y_t += 1
                        self.y_f += 0.5
        else:
            self.x_f, self.y_f = 50, 13
            self.x_t, self.y_t = 28, 61
            self.x_l, self.y_l = 40, 110

    def hand_down(self):
        if self.hand_time < 5:
            self.body = hand_down[self.hand_time]
            self.y_f = self.face_move2[self.hand_time]
            self.hand_time += 1
        else:
            self.hand_time = 0
            self.hand_down_bool = False

    def hand_up(self):
        if self.hand_time < 5:
            self.body = hand_up[self.hand_time]
            self.y_f = self.face_move2[self.hand_time]
            self.hand_time += 1
        else:
            self.hand_time = 0
            self.hand_up_bool = False

    def hand_right(self):
        if self.hand_time < 5:
            self.body = hand_right[self.hand_time]
            self.x_f = self.face_move2[self.hand_time] + 35
            self.hand_time += 1
        else:
            self.hand_time = 0
            self.hand_right_bool = False
            self.x_f = 48



class Diologs():
    def __init__(self):
        global screen, dio1, f3, s_voice
        self.time, self.txt, self.txt2, self.txt1 = 0, "", "", ""
        self.next, self.stop = False, False

    def draw_all(self, x, y, voice=True):
        screen.blit(dio1, (x, y))

        if "\n" == self.txt[self.time]:
            self.next = True
            t = f3.render(self.txt1, True, Color("black"))
            screen.blit(t, (x + 35, y + 15))
            self.time += 1
            if voice:
                s_voice.stop()
                s_voice.play()
            return
        t = f3.render(self.txt1, True, Color("black"))
        if self.next:
            if not(self.stop):
                self.txt2 += self.txt[self.time]
                if voice:
                    s_voice.stop()
                    s_voice.play()
            t1 = f3.render(self.txt2, True, Color("black"))
            screen.blit(t1, (x + 35, y + 35))
        if not(self.next) and not(self.stop):
            self.txt1 += self.txt[self.time]
            if voice:
                s_voice.stop()
                s_voice.play()
        screen.blit(t, (x + 35, y + 15))
        if self.time < len(self.txt) - 1:
            self.time += 1
        else:
            self.stop = True





if __name__ == '__main__':
    run = True
    os.environ['SDL_VIDEO_CENTERED'] = '0'
    scr = "small"
    n = 2
    g = 0.2
    name = "CHARA"
    sec = 0
    fps = 29
    size = (600, 600)
    wx1, wy1, w2, h2 = 200, 300, 200, 200
    pygame.mixer.pre_init(44100, -16, 2, 2048)
    pygame.mixer.init()
    pygame.init()
    clock = pygame.time.Clock()
    screen1 = pygame.display.set_mode(size)
    screen = Surface(size)
    screen.fill(Color("black"))

    f1 = pygame.font.Font("resours/abcd.ttf", 15)
    f2 = pygame.font.Font("resours/sans.ttf", 15)
    f3 = pygame.font.Font("resours/sans.ttf", 16)

    track = pygame.image.load("resours/Track.png").convert()
    blast = pygame.image.load("resours/Blaster1.png").convert()
    blast_open = pygame.image.load("resours/Blaster_open1.png").convert()
    blast_open2 = pygame.image.load("resours/Blaster_open2.png").convert()
    blast_open3 = pygame.image.load("resours/Blaster_open3.png").convert()
    red_soul = pygame.image.load("resours/Red_soul.png").convert()
    blue_down = pygame.image.load("resours/Blue_soul_down.png").convert()
    blue_up = pygame.image.load("resours/Blue_soul_up.png").convert()
    blue_left = pygame.image.load("resours/Blue_soul_left.png").convert()
    blue_right = pygame.image.load("resours/Blue_soul_right.png").convert()

    ## Большие кости ##
    bone_white = pygame.image.load("resours/Bone_big.png").convert()
    bone_white_rot = pygame.image.load("resours/Bone_rot_big.png").convert()
    bone_blue = pygame.image.load("resours/Bone_blue.png").convert()
    bone_blue_rot = pygame.image.load("resours/Bone_blue_rot.png").convert()
    bone_orange = pygame.image.load("resours/Bone_orange.png").convert()
    bone_orange_rot = pygame.image.load("resours/Bone_orange_rot.png").convert()

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

    ## Кнопки ##
    fight = pygame.image.load("resours/Fight.png").convert()
    act = pygame.image.load("resours/Act.png").convert()
    item = pygame.image.load("resours/Item.png").convert()
    mercy = pygame.image.load("resours/Mercy.png").convert()

    ## Сломанная душа ##
    broken_soul = pygame.image.load("resours/broken_soul.png").convert()
    soul_part1 = pygame.image.load("resours/soul_part1.png").convert()
    soul_part2 = pygame.image.load("resours/soul_part2.png").convert()
    soul_part3 = pygame.image.load("resours/soul_part3.png").convert()
    soul_parts = [soul_part1, soul_part2, soul_part3]

    ## Диологовые окна ##
    dio1 = pygame.image.load("resours/diolog_1.png").convert()

    ## Конец игры ##
    GO = change_scale(pygame.image.load("resours/game_over.jpg").convert_alpha(), 5, 5)
    GO.set_colorkey(Color("black"))

    ## Звуки ##
    hit_s = pygame.mixer.Sound('sounds/hit.wav')
    hit1_s = pygame.mixer.Sound('sounds/hit1.wav')
    blaster_start_s = pygame.mixer.Sound('sounds/blaster_start.ogg')
    blaster_end_s = pygame.mixer.Sound('sounds/blaster_end.ogg')
    blim_s = pygame.mixer.Sound('sounds/bong.wav')
    break1_s = pygame.mixer.Sound('sounds/break1.wav')
    break2_s = pygame.mixer.Sound('sounds/break2.wav')
    bam = pygame.mixer.Sound('sounds/bam.wav')
    s_voice = pygame.mixer.Sound('sounds/sans_txt.wav')

    ## Музыка ##
    pygame.mixer.music.load("music/megalovania.mp3")
    pygame.mixer.music.play(-1)

    ## ----------- SANS ----------- ##
    ## legs ##
    legs = change_scale(pygame.image.load("resours/sans/legs.png").convert())

    ## tors ##
    tors_1 = change_scale(pygame.image.load("resours/sans/tors_1.png").convert())
    tors_2 = change_scale(pygame.image.load("resours/sans/tors_2.png").convert())

    ## face ##
    face_1 = change_scale(pygame.image.load("resours/sans/face_1.png").convert())
    face_2 = change_scale(pygame.image.load("resours/sans/Face_2.png").convert())
    face_3 = change_scale(pygame.image.load("resours/sans/Face_3.png").convert())
    face_4 = change_scale(pygame.image.load("resours/sans/Face_4.png").convert())
    face_5 = change_scale(pygame.image.load("resours/sans/Face_5.png").convert())
    face_eye_1 = change_scale(pygame.image.load("resours/sans/Face_eye_blue.png").convert())
    face_eye_2 = change_scale(pygame.image.load("resours/sans/Face_eye_yellow.png").convert())
    face_ser = change_scale(pygame.image.load("resours/sans/Face_seriose.png").convert())
    face, face_eye = [face_1, face_2, face_3, face_4, face_5], [face_eye_1, face_eye_2]

    ## hand_down ##
    h_down_1 = change_scale(pygame.image.load("resours/sans/hand_down_1.png").convert())
    h_down_2 = change_scale(pygame.image.load("resours/sans/hand_down_2.png").convert())
    h_down_3 = change_scale(pygame.image.load("resours/sans/hand_down_3.png").convert())
    h_down_4 = change_scale(pygame.image.load("resours/sans/hand_down_4.png").convert())
    h_down_5 = change_scale(pygame.image.load("resours/sans/hand_down_5.png").convert())
    hand_down = [h_down_1, h_down_2, h_down_3, h_down_4, h_down_5]

    ## hand_up ##
    h_up_1 = change_scale(pygame.image.load("resours/sans/hand_up_1.png").convert())
    h_up_2 = change_scale(pygame.image.load("resours/sans/hand_up_2.png").convert())
    h_up_3 = change_scale(pygame.image.load("resours/sans/hand_up_3.png").convert())
    h_up_4 = change_scale(pygame.image.load("resours/sans/hand_up_4.png").convert())
    h_up_5 = change_scale(pygame.image.load("resours/sans/hand_up_5.png").convert())
    hand_up = [h_up_1, h_up_2, h_up_3, h_up_4, h_up_5]

    ## hand_right ##
    h_right_1 = change_scale(pygame.image.load("resours/sans/hand_right_1.png").convert())
    h_right_2 = change_scale(pygame.image.load("resours/sans/hand_right_2.png").convert())
    h_right_3 = change_scale(pygame.image.load("resours/sans/hand_right_3.png").convert())
    h_right_4 = change_scale(pygame.image.load("resours/sans/hand_right_4.png").convert())
    h_right_5 = change_scale(pygame.image.load("resours/sans/hand_right_5.png").convert())
    hand_right = [h_right_1, h_right_2, h_right_3, h_right_4, h_right_5]

    ## ----------------------------- ##
    sans = Sans()

    ## Значения ##
    file = open("resours/data.txt").read().split("\n")
    death = int(file[0])



    player = Player()
    at = AtkList()
    box = Box(wx1, wy1, w2, h2)
    diologs = Diologs()
    pygame.display.flip()

    while run:
        clock.tick(fps)
        pygame.display.set_caption(f"Fps {clock.get_fps()}")
        sec += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if player.check_death():
                if player.sec_d > 200:
                    if event.type == pygame.KEYDOWN:
                        restart()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F4:
                    print("full_screen")
                    change_screen()
                if event.key == pygame.K_ESCAPE:
                    run = False
                if event.key == pygame.K_DELETE:
                    restart()
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
        if player.check_death() == False:
            if at.blok:
                press = pygame.key.get_pressed()
                if press[pygame.K_LEFT]:
                    player.movement(-1, 0, "right")
                elif not(press[pygame.K_LEFT]):
                    player.jum("right")
                if press[pygame.K_RIGHT]:
                    player.movement(1.3, 0, "left")
                elif not(press[pygame.K_RIGHT]):
                    player.jum("left")
                if press[pygame.K_DOWN]:
                    player.movement(0, 1.3, "up")
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

            screen.blit(fight, (30, 550))
            screen.blit(act, (175, 550))
            screen.blit(item, (315, 550))
            screen.blit(mercy, (460, 550))
            pygame.draw.rect(screen, Color("red"), (260, 515, 120, 20))
            pygame.draw.rect(screen, Color("yellow"), (260, 515, 120 / 92 * player.hp, 20))

            name_t = f1.render(name, True, Color("white"))
            screen.blit(name_t, (30, 515))

            LV_t = f1.render("LV 19", True, Color("white"))
            screen.blit(LV_t, (130, 515))

            HP_t = f2.render("HP", True, Color("white"))
            screen.blit(HP_t, (230, 517))

            hp_kolv_t = f1.render(f"{player.hp} / 92", True, Color("white"))
            screen.blit(hp_kolv_t, (400, 515))


            sans.draw()
            sans.move_body()
            box.start()
            at.all_atks(sec)
            at.draw_bones()
            box.surf()
            at.draw_blasters()

            player.hit()
            player.draw_player()
            player.change_color()
            at.draw_shake()
            at.draw_fill()
            if at.change == True:
                screen.fill(Color("black"))
            at.change_screen_scale()
        if scr == "full":
            screen2 = pygame.transform.scale(screen, (1080, 1080))
            screen1.blit(screen2, (420, 0))
        if scr == "small":
            screen1.blit(screen, (0, 0))


        pygame.display.flip()

pygame.quit()
exit()
