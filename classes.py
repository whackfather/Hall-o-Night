# All Game Classes

import pygame
from pygame.locals import *
import json

# The Player
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load("sprites/smallerq.png").convert()
        self.original = self.surf
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

# Basic dirt floor
class EnvFloor(pygame.sprite.Sprite):
    def __init__(self):
        super(EnvFloor, self).__init__()
        self.surf = pygame.image.load("sprites/newground.png").convert()
        self.rect = self.surf.get_rect()

# Wall (idk what else to tell you)
class EnvWall(pygame.sprite.Sprite):
    def __init__(self):
        super(EnvWall, self).__init__()
        self.surf = pygame.image.load("sprites/wall.png").convert()
        self.rect = self.surf.get_rect()

# Floating brick platforms (not ground)
class EnvPlatform(pygame.sprite.Sprite):
    def __init__(self):
        super(EnvPlatform, self).__init__()
        self.surf = pygame.image.load("sprites/platform.png").convert()
        self.rect = self.surf.get_rect()

# Shorter version of platform
class EnvShortPlat(pygame.sprite.Sprite):
    def __init__(self):
        super(EnvShortPlat, self).__init__()
        self.surf = pygame.image.load("sprites/shortplat.png").convert()
        self.rect = self.surf.get_rect()

# Brute, remains on platform it starts on, deals damage by bodyslamming
class BruteEnemy(pygame.sprite.Sprite):
    def __init__(self):
        super(BruteEnemy, self).__init__()
        self.surf = pygame.image.load("sprites/diddy.png").convert()
        self.rect = self.surf.get_rect()
        self.spdx = 0
        self.health = 3
        self.beenhit = False
        self.home = None
        self.boundleft = None
        self.boundright = None

    def update(self, player:pygame.Rect, beenhit:bool, leftbound:int, rightbound:int) -> None:
        def stayonplat() -> None:
            if self.rect.right > rightbound:
                self.rect.right = rightbound
                self.spdx = 0
            elif self.rect.left < leftbound:
                self.rect.left = leftbound
                self.spdx = 0
        if pygame.sprite.collide_circle_ratio(3)(player, self):
            if player.rect.bottom > (self.rect.bottom + 20) or player.rect.bottom < (self.rect.top - 50):
                pass
            elif beenhit:
                knockback = 4
                if player.rect.right < self.rect.left:
                    self.rect.move_ip(knockback, 0)
                elif player.rect.left > self.rect.right:
                    self.rect.move_ip(-knockback, 0)
                stayonplat()
            else:
                if player.rect.centerx < self.rect.left:
                    self.spdx = -2
                elif player.rect.centerx > self.rect.right:
                    self.spdx = 2
                else:
                    self.spdx = 0
                self.rect.move_ip(self.spdx, 0)
                stayonplat()

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
    
    def load(self, number:int) -> None:
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
        
        if data["ground"] != 0:
            for ground in data["ground"]:
                newground = EnvFloor()
                newground.rect.centerx = int(ground["centerx"])
                newground.rect.centery = int(ground["centery"])
                self.sprites.append(newground); self.environ.append(newground)
        
        if data["walls"] != 0:
            for wall in data["walls"]:
                newwall = EnvWall()
                newwall.rect.centerx = int(wall["centerx"])
                newwall.rect.centery = int(wall["centery"])
                self.sprites.append(newwall); self.environ.append(newwall)

        if data["platforms"] != 0:
            for plat in data["platforms"]:
                newplat = EnvPlatform()
                newplat.rect.centerx = int(plat["centerx"])
                newplat.rect.centery = int(plat["centery"])
                self.sprites.append(newplat); self.environ.append(newplat)
        
        if data["shortplats"] != 0:
            for short in data["shortplats"]:
                newshort = EnvShortPlat()
                newshort.rect.centerx = int(short["centerx"])
                newshort.rect.centery = int(short["centery"])
                self.sprites.append(newshort); self.environ.append(newshort)
        
        if data["enemies"] != 0:
            for enemy in data["enemies"]:
                newenemy = BruteEnemy()
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
