# Level 1 Information

import pygame
from pygame.locals import *
from classes import *

# Screen size definition
size = width, height = 1280, 720

# The list 
level1sprites = []
levelhealth = []
level1environ = []
level1enemies = []

# Player health
hp1 = HealthPoints(); hp1.rect.center = (32, 32); levelhealth.append(hp1)
hp2 = HealthPoints(); hp2.rect.center = (hp1.rect.centerx * 2, hp1.rect.centery); levelhealth.append(hp2)
hp3 = HealthPoints(); hp3.rect.center = (hp1.rect.centerx * 3, hp1.rect.centery); levelhealth.append(hp3)
hp4 = HealthPoints(); hp4.rect.center = (hp1.rect.centerx * 4, hp1.rect.centery); levelhealth.append(hp4)
hp5 = HealthPoints(); hp5.rect.center = (hp1.rect.centerx * 5, hp1.rect.centery); levelhealth.append(hp5)

# Environment construction, labeled by platform number and sub platform number
# Subplatform number 1 is the leftmost piece, greatest subplatform number is the rightmost
plat1_1 = EnvObject(); plat1_1.rect.center = (width / 2, height - 90)
level1sprites.append(plat1_1); level1environ.append(plat1_1)
plat1_2 = EnvObject(); plat1_2.rect.topright = plat1_1.rect.topleft
level1sprites.append(plat1_2); level1environ.append(plat1_2)
plat1_3 = EnvObject(); plat1_3.rect.topleft = plat1_1.rect.topright
level1sprites.append(plat1_3); level1environ.append(plat1_3)

plat2_1 = EnvObject(); plat2_1.rect.bottomleft = (0, plat1_1.rect.top - 110) 
level1sprites.append(plat2_1); level1environ.append(plat2_1)
plat2_2 = EnvObject(); plat2_2.rect.topleft = plat2_1.rect.topright
level1sprites.append(plat2_2); level1environ.append(plat2_2)
plat2_3 = EnvObject(); plat2_3.rect.topleft = plat2_2.rect.topright
level1sprites.append(plat2_3); level1environ.append(plat2_3)
plat2_4 = EnvObject(); plat2_4.rect.topleft = plat2_3.rect.topright
level1sprites.append(plat2_4); level1environ.append(plat2_4)

plat3_1 = EnvObject(); plat3_1.rect.bottomleft = (plat2_4.rect.right + 35, plat2_2.rect.top - 110); 
level1sprites.append(plat3_1); level1environ.append(plat3_1)
plat3_2 = EnvObject(); plat3_2.rect.topleft = plat3_1.rect.topright
level1sprites.append(plat3_2); level1environ.append(plat3_2)
plat3_3 = EnvObject(); plat3_3.rect.topleft = plat3_2.rect.topright
level1sprites.append(plat3_3); level1environ.append(plat3_3)

plat4_2 = EnvObject(); plat4_2.rect.bottomright = (width - 95, 300)
level1sprites.append(plat4_2); level1environ.append(plat4_2)
plat4_1 = EnvObject(); plat4_1.rect.topright = plat4_2.rect.topleft
level1sprites.append(plat4_1); level1environ.append(plat4_1)

plat5_1 = EnvObject(); plat5_1.rect.center = ((plat4_1.rect.left + plat3_3.rect.right) / 2, (plat3_3.rect.top + plat4_1.rect.bottom) / 2)
level1sprites.append(plat5_1); level1environ.append(plat5_1)

# Level 1 Advance Location
door = AdvanceBox(); door.rect.centerx = plat4_1.rect.right; door.rect.bottom = plat4_1.rect.top
level1sprites.append(door)

# Player initialization
player = Player(); player.rect.bottomleft = (64, height); level1sprites.append(player)
weapon = Weapon(); weapon.rect.left = player.rect.right; level1sprites.append(weapon)

#Enemy placement
l1e1 = ContactEnemy(); l1e1.rect.centerx = plat1_1.rect.centerx; l1e1.rect.bottom = plat1_1.rect.top
l1e1.home = plat1_1; l1e1.boundleft = plat1_2.rect.left; l1e1.boundright = plat1_3.rect.right
level1sprites.append(l1e1); level1enemies.append(l1e1)

l1e2 = ContactEnemy(); l1e2.rect.centerx = plat2_1.rect.centerx; l1e2.rect.bottom = plat2_1.rect.top
l1e2.home = plat2_1; l1e2.boundleft = plat2_1.rect.left; l1e2.boundright = plat2_4.rect.right
level1sprites.append(l1e2); level1enemies.append(l1e2)

l1e3 = ContactEnemy(); l1e3.rect.centerx = plat3_3.rect.centerx; l1e3.rect.bottom = plat3_3.rect.top
l1e3.home = plat3_3; l1e3.boundleft = plat3_1.rect.left; l1e3.boundright = plat3_3.rect.right
level1sprites.append(l1e3); level1enemies.append(l1e3)
