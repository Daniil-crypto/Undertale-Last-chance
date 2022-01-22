import pygame, math
from pygame import Color, Rect, Surface


def change_scale(image, f=1):
    global n, screen
    size = image.get_size()
    bigger_img = pygame.transform.scale(image, (int(size[0] * n // f), int(size[1] * n // f)))
    return bigger_img

def rotate_to_player(blast, track=False):
    angle = math.degrees(math.atan2(player.x - self.x, player.y - self.y))
    image = pygame.transform.rotate(blast, angle)
    center = blast.get_rect().center
    rect = image.get_rect(center=center)
    return image, (rect[0] + 8, rect[1] + 8)


pygame.init()
n = 2
screen = pygame.display.set_mode((600, 600))
screen.fill(Color("black"))
clock = pygame.time.Clock()
blast = change_scale(pygame.image.load("Blaster1.png"))
blast1 = Surface((200 + 20, 100 * 2 + 20), pygame.SRCALPHA, 32).convert_alpha()
track = change_scale(pygame.image.load("Track.png"))
track1 = Surface((4000, 4000), pygame.SRCALPHA, 32).convert_alpha()
track.set_colorkey((0, 0, 0))

while True:
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    blast1.blit(rotate_to_player(blast)[0], rotate_to_player(blast)[1])
    track1.blit(rot(track, 3)[0], (rot(track, 5)[1][0] + 2000, rot(track, 5)[1][1] + 2000))
    screen.blit(track1, (200 - 2000, 100 - 2000))
    screen.blit(blast1, (200, 100))
    pygame.display.flip()
