import pygame
from pygame.locals import *

width, height = 1280, 720

def playerupdate(pressed_keys, weapon, player, environ, beenhit, attacker):
    if beenhit:
        if player.rect.right < attacker.rect.centerx:
            player.rect.move_ip(-6, 0)
        elif player.rect.left > attacker.rect.centerx:
            player.rect.move_ip(6, 0)
    else:
        if pressed_keys[K_a]:
            if player.jump:
                player.speedx = -6
            else:
                player.speedx = -5
            player.rect.move_ip(player.speedx, 0)
            if pygame.sprite.spritecollideany(player, environ):
                obstacle = pygame.sprite.spritecollideany(player, environ)
                player.rect.left = obstacle.rect.right
            player.speedx = 0
        if pressed_keys[K_d]:
            if player.jump:
                player.speedx = 6
            else:
                player.speedx = 5
            player.rect.move_ip(player.speedx, 0)
            if pygame.sprite.spritecollideany(player, environ):
                obstacle = pygame.sprite.spritecollideany(player, environ)
                player.rect.right = obstacle.rect.left
            player.speedx = 0
        if pressed_keys[K_SPACE]:
            if player.jump == False and player.grounded == True and player.speedy == 0:
                player.jump = True
                player.grounded = False
                player.speedy = -17
        player.rect.move_ip(0, player.speedy)
        player.speedy += 1
        if player.speedy > 21:
            player.speedy = 21
        if pygame.sprite.spritecollideany(player, environ):
            obstacle = pygame.sprite.spritecollideany(player, environ)
            if player.rect.top < obstacle.rect.bottom and player.rect.bottom > obstacle.rect.bottom:
                player.rect.top = obstacle.rect.bottom
                player.speedy = 0
            elif player.rect.bottom > obstacle.rect.top and player.rect.top < obstacle.rect.bottom:
                player.rect.bottom = obstacle.rect.top
                player.speedy = 0
                player.grounded = True
        if player.rect.top < 0:
            player.rect.top = 0
            player.speedy = 0
        if player.rect.bottom > height:
            player.rect.bottom = height
            player.speedy = 0
            player.grounded = True
        if player.rect.right > width:
            player.rect.right = width
        if player.rect.left < 0:
            player.rect.left = 0
