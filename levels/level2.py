# Level 2 Information

import pygame
from pygame.locals import *
from classes import *

# Screen size definiton
size = width, height = 1280, 720

# Sprite lists
level2sprites = []
levelhealth = []
level2environ = []
level2enemies = []

# Player health
hp1 = HealthPoints(); hp1.rect.center = (32, 32); levelhealth.append(hp1)
hp2 = HealthPoints(); hp2.rect.center = (hp1.rect.centerx * 2, hp1.rect.centery); levelhealth.append(hp2)
hp3 = HealthPoints(); hp3.rect.center = (hp1.rect.centerx * 3, hp1.rect.centery); levelhealth.append(hp3)
hp4 = HealthPoints(); hp4.rect.center = (hp1.rect.centerx * 4, hp1.rect.centery); levelhealth.append(hp4)
hp5 = HealthPoints(); hp5.rect.center = (hp1.rect.centerx * 5, hp1.rect.centery); levelhealth.append(hp5)

# Environment construction
plat1 = EnvObject(); plat1.rect.centerx = width / 2; plat1.rect.bottom = height
level2sprites.append(plat1); level2environ.append(plat1)

# Player initialization
player = Player(); player.rect.bottomleft = (32, height); level2sprites.append(player)
weapon = Weapon(); weapon.rect.left = player.rect.right; level2sprites.append(weapon)
