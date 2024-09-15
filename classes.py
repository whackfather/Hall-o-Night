import pygame
from pygame.locals import *

# The Player
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load("sprites/32x64.png").convert()
        self.rect = self.surf.get_rect()
        self.jump = False
        self.grounded = True
        self.speedx = 0
        self.speedy = 0
        self.health = 5
        self.iframes = 30
        self.beenhit = False
        self.facing = 1

class HealthPoints(pygame.sprite.Sprite):
    def __init__(self):
        super(HealthPoints, self).__init__()
        self.surf = pygame.image.load("sprites/healthpoint.png").convert()
        self.rect = self.surf.get_rect()

# Player Weapon
class Weapon(pygame.sprite.Sprite):
    def __init__(self):
        super(Weapon, self).__init__()
        self.surf = pygame.image.load("sprites/weapon.png").convert()
        self.surf.set_colorkey((0, 0, 0))
        self.rect = self.surf.get_rect()
        self.sheathed = True
        self.hitframes = 0
        self.attacking = False

# Basic long platform
class EnvObject(pygame.sprite.Sprite):
    def __init__(self):
        super(EnvObject, self).__init__()
        self.surf = pygame.image.load("sprites/platform.png").convert()
        self.rect = self.surf.get_rect()

# Basic enemy
# Remains on platform it starts on, deals damage by bodyslamming
class ContactEnemy(pygame.sprite.Sprite):
    def __init__(self):
        super(ContactEnemy, self).__init__()
        self.surf = pygame.image.load("sprites/enemy1.png").convert()
        self.rect = self.surf.get_rect()
        self.spdx = 0
        self.health = 3
        self.beenhit = False
        self.home = None
        self.boundleft = None
        self.boundright = None

    def update(self, player, obst, beenhit, leftbound, rightbound):
        if pygame.sprite.collide_circle_ratio(4)(player, self):
            if player.rect.bottom > self.rect.bottom:
                pass
            elif beenhit:
                knockback = 4
                if player.rect.right < self.rect.left:
                    self.rect.move_ip(knockback, 0)
                elif player.rect.left > self.rect.right:
                    self.rect.move_ip(-knockback, 0)
                if self.rect.right > obst.rect.right or self.rect.left < obst.rect.left:
                    if self.rect.right > obst.rect.right:
                        self.rect.right = obst.rect.right
                    elif self.rect.left < obst.rect.left:
                        self.rect.left = obst.rect.left
                    speedx = 0
            else:
                if player.rect.centerx < self.rect.left:
                    speedx = -2
                elif player.rect.centerx > self.rect.right:
                    speedx = 2
                else:
                    speedx = 0
                self.rect.move_ip(speedx, 0)
                if self.rect.right > rightbound or self.rect.left < leftbound:
                    if self.rect.right > rightbound:
                        self.rect.right = rightbound
                    elif self.rect.left < leftbound:
                        self.rect.left = leftbound
                    speedx = 0
