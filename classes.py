# All game classes

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
        self.iframes = 15
        self.beenhit = False
        self.facing = 1

    def update(self, pressed_keys, environ, beenhit, attacker, width, height):
        def objectcollide():
            if pygame.sprite.spritecollideany(self, environ):
                obstacle = pygame.sprite.spritecollideany(self, environ)
                if self.rect.top < obstacle.rect.bottom and self.rect.bottom > obstacle.rect.bottom:
                    self.rect.top = obstacle.rect.bottom
                    self.speedy = 0
                elif self.rect.bottom > obstacle.rect.top and self.rect.top < obstacle.rect.bottom:
                    self.rect.bottom = obstacle.rect.top
                    self.speedy = 0
                    self.grounded = True
            if self.rect.top < 0:
                self.rect.top = 0
                self.speedy = 0
            if self.rect.bottom > height:
                self.rect.bottom = height
                self.speedy = 0
                self.grounded = True
            if self.rect.right > width:
                self.rect.right = width
            if self.rect.left < 0:
                self.rect.left = 0
        
        if beenhit:
            self.speedy += 1
            if self.speedy > 21:
                self.speedy = 21
            if self.rect.right < attacker.rect.centerx:
                self.rect.move_ip(-6, self.speedy)
            elif self.rect.left > attacker.rect.centerx:
                self.rect.move_ip(6, self.speedy)
            objectcollide()
        else:
            if pressed_keys[K_a]:
                if self.jump:
                    self.speedx = -6
                else:
                    self.speedx = -5
                self.rect.move_ip(self.speedx, 0)
                if pygame.sprite.spritecollideany(self, environ):
                    obstacle = pygame.sprite.spritecollideany(self, environ)
                    self.rect.left = obstacle.rect.right
                self.speedx = 0
            if pressed_keys[K_d]:
                if self.jump:
                    self.speedx = 6
                else:
                    self.speedx = 5
                self.rect.move_ip(self.speedx, 0)
                if pygame.sprite.spritecollideany(self, environ):
                    obstacle = pygame.sprite.spritecollideany(self, environ)
                    self.rect.right = obstacle.rect.left
                self.speedx = 0
            if pressed_keys[K_SPACE]:
                if self.jump == False and self.grounded == True and self.speedy == 0:
                    self.jump = True
                    self.grounded = False
                    self.speedy = -17
            self.rect.move_ip(0, self.speedy)
            self.speedy += 1
            if self.speedy > 21:
                self.speedy = 21
            objectcollide()

# HP sprites
class HealthPoints(pygame.sprite.Sprite):
    def __init__(self):
        super(HealthPoints, self).__init__()
        self.surf = pygame.image.load("sprites/healthpoint.png").convert()
        self.rect = self.surf.get_rect()

class AdvanceBox(pygame.sprite.Sprite):
    def __init__(self):
        super(AdvanceBox, self).__init__()
        self.surf = pygame.image.load("sprites/advance.png").convert()
        self.rect = self.surf.get_rect()
        self.collide = self.surf.get_rect()
        self.collide.width = 10

# Player Weapon
class Weapon(pygame.sprite.Sprite):
    def __init__(self):
        super(Weapon, self).__init__()
        self.surf = pygame.image.load("sprites/weaponright.png").convert()
        self.surf.set_colorkey((0, 0, 0))
        self.original = self.surf
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
        if pygame.sprite.collide_circle_ratio(3)(player, self):
            if player.rect.bottom > self.rect.bottom:
                pass
            elif beenhit:
                knockback = 4
                if player.rect.right < self.rect.left:
                    self.rect.move_ip(knockback, 0)
                elif player.rect.left > self.rect.right:
                    self.rect.move_ip(-knockback, 0)
                if self.rect.right > rightbound:
                    self.rect.right = rightbound
                    speedx = 0
                elif self.rect.left < leftbound:
                    self.rect.left = leftbound
                    speedx = 0
            else:
                if player.rect.centerx < self.rect.left:
                    speedx = -2
                elif player.rect.centerx > self.rect.right:
                    speedx = 2
                else:
                    speedx = 0
                self.rect.move_ip(speedx, 0)
                if self.rect.right > rightbound:
                    self.rect.right = rightbound
                    speedx = 0
                elif self.rect.left < leftbound:
                    self.rect.left = leftbound
                    speedx = 0
