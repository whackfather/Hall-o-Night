# All Game Classes

import pygame
from pygame.locals import *
import json

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

# HP sprites
class HealthPoints(pygame.sprite.Sprite):
    def __init__(self):
        super(HealthPoints, self).__init__()
        self.surf = pygame.image.load("sprites/healthpoint.png").convert()
        self.rect = self.surf.get_rect()

# Level advance box
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

    def update(self, player, beenhit, leftbound, rightbound):
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

# Loading the level data from .json
class Level():
    def __init__(self):
        self.sprites = []
        self.health = []
        self.environ = []
        self.enemies = []
        self.player = None
        self.weapon = None
        self.door = None
    
    def load(self, number):
        self.sprites.clear()
        self.health.clear()
        self.environ.clear()
        self.enemies.clear()
        
        info = open(f"jsonlevels/level{number}.json")
        data = json.load(info)
        info.close()

        for i in range(data["health"]):
            newhp = HealthPoints()
            newhp.rect.center = (32 * i + 32, 32)
            self.health.append(newhp)
        
        for plat in data["platforms"]:
            newplat = EnvObject()
            newplat.rect.centerx = int(plat["centerx"])
            newplat.rect.centery = int(plat["centery"])
            self.sprites.append(newplat); self.environ.append(newplat)
        
        if data["enemies"] != 0:
            for enemy in data["enemies"]:
                newenemy = ContactEnemy()
                newenemy.rect.centerx = int(enemy["centerx"])
                newenemy.rect.centery = int(enemy["centery"])
                newenemy.boundleft = int(enemy["leftbound"])
                newenemy.boundright = int(enemy["rightbound"])
                self.sprites.append(newenemy); self.enemies.append(newenemy)

        self.door = AdvanceBox()
        self.door.rect.centerx = int(data["door"]["centerx"])
        self.door.rect.centery = int(data["door"]["centery"])
        self.sprites.append(self.door)

        self.player = Player()
        self.player.rect.centerx = int(data["player"]["centerx"])
        self.player.rect.centery = int(data["player"]["centery"])

        self.weapon = Weapon()
        self.weapon.rect.centerx = int(data["weapon"]["centerx"])
        self.weapon.rect.centerx = int(data["weapon"]["centery"])
