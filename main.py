# Hall-o' Night
# Programmed by Roman Rodriguez

# Importing
import pygame
from pygame.locals import *
from classes import *
from time import sleep

# Initializing pygame and screen
pygame.init()
size = width, height = 1280, 720
screen = pygame.display.set_mode(size)

# Group management
all_sprites = pygame.sprite.Group()
visualhp = pygame.sprite.Group()
environ = pygame.sprite.Group()
weapons = pygame.sprite.Group()
enemies = pygame.sprite.Group()
thejar = pygame.sprite.Group()
playerjar = pygame.sprite.Group()

# Game clock for framerate (might need work later)
clock = pygame.time.Clock()

# Stuff that needed defining 
attacker = None
lvlnum = 1
level = Level()
def loader(lvlnum, all_sprites, environ, enemies):
    level.load(lvlnum)
    for i in level.sprites:
        all_sprites.add(i)
    for i in level.environ:
        environ.add(i)
    for i in level.enemies:
        enemies.add(i)
advance = True

# Game loop
running = True
while running:
    # Level check
    if lvlnum == 1 and advance == True:
        loader(lvlnum, all_sprites, environ, enemies)
        advance = False
    elif lvlnum == 2 and advance == True:
        loader(lvlnum, all_sprites, environ, enemies)
        advance = False
    
    # Event handling
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        if event.type == KEYUP:
            if event.key == K_SPACE:
                level.player.jump = False
            if event.key == K_k:
                level.weapon.sheathed = True
    
    # Enemy location update
    if lvlnum == 1:
        for enemy in level.enemies:
            enemy.update(level.player, enemy.beenhit, enemy.boundleft, enemy.boundright)
    elif lvlnum == 2:
        for enemy in level.enemies:
            enemy.update(level.player, enemy.beenhit, enemy.boundleft, enemy.boundright)
    
    # Player, weapon, and enemy collision
    if pygame.sprite.groupcollide(weapons, enemies, False, False):
        hitenemy = pygame.sprite.spritecollideany(level.weapon, enemies)
        if hitenemy not in thejar:
            hitenemy.health -= 1
            hitenemy.beenhit = True
            thejar.add(hitenemy)
        if hitenemy.health == 0:
            hitenemy.kill()
    if pygame.sprite.spritecollideany(level.player, enemies):
        attacker = pygame.sprite.spritecollideany(level.player, enemies)
        if level.player not in playerjar:
            level.player.health -= 1
            level.health.remove(level.health[-1])
            level.player.beenhit = True
            playerjar.add(level.player)

    if level.player in playerjar and level.player.iframes > 0:
        level.player.iframes -= 1
        if level.player.iframes == 0:
            playerjar.empty()
            level.player.iframes = 15 
            level.player.beenhit = False
    if level.player.health == 0:
        level.player.kill()
        level.weapon.kill()
        running = False
    
    # Input reading
    pressed_keys = pygame.key.get_pressed()
    
    # Character location update
    def objectcollide():
            if pygame.sprite.spritecollideany(level.player, environ):
                obstacle = pygame.sprite.spritecollideany(level.player, environ)
                if level.player.rect.top < obstacle.rect.bottom and level.player.rect.bottom > obstacle.rect.bottom:
                    level.player.rect.top = obstacle.rect.bottom
                    level.player.speedy = 0
                elif level.player.rect.bottom > obstacle.rect.top and level.player.rect.top < obstacle.rect.bottom:
                    level.player.rect.bottom = obstacle.rect.top
                    level.player.speedy = 0
                    level.player.grounded = True
            if level.player.rect.top < 0:
                level.player.rect.top = 0
                level.player.speedy = 0
            if level.player.rect.bottom > height:
                level.player.rect.bottom = height
                level.player.speedy = 0
                level.player.grounded = True
            if level.player.rect.right > width:
                level.player.rect.right = width
            if level.player.rect.left < 0:
                level.player.rect.left = 0
        
    if level.player.beenhit:
        level.player.speedy += 1
        if level.player.speedy > 21:
            level.player.speedy = 21
        if level.player.rect.right < attacker.rect.centerx:
            level.player.rect.move_ip(0, level.player.speedy)
            for any in all_sprites:
                any.rect.move_ip(6, 0)
            for enemy in enemies:
                enemy.boundleft += 6
                enemy.boundright += 6
        elif level.player.rect.left > attacker.rect.centerx:
            level.player.rect.move_ip(0, level.player.speedy)
            for any in all_sprites:
                any.rect.move_ip(-6, 0)
            for enemy in enemies:
                enemy.boundleft -= 6
                enemy.boundright -= 6
        objectcollide()
    else:
        if pressed_keys[K_a]:
            if level.player.jump:
                level.player.speedx = 6
                for enemy in enemies:
                    enemy.boundleft += 6
                    enemy.boundright += 6
            else:
                level.player.speedx = 5
                for enemy in enemies:
                    enemy.boundleft += 5
                    enemy.boundright += 5
            for any in all_sprites:
                any.rect.move_ip(level.player.speedx, 0)
            if pygame.sprite.spritecollideany(level.player, environ):
                obstacle = pygame.sprite.spritecollideany(level.player, environ)
                level.player.rect.left = obstacle.rect.right
                for any in all_sprites:
                    any.rect.move_ip(-level.player.speedx, 0)
                for enemy in enemies:
                    enemy.boundleft -= level.player.speedx
                    enemy.boundright -= level.player.speedx
            level.player.speedx = 0
        if pressed_keys[K_d]:
            if level.player.jump:
                level.player.speedx = -6
                for enemy in enemies:
                    enemy.boundleft -= 6
                    enemy.boundright -= 6
            else:
                level.player.speedx = -5
                for enemy in enemies:
                    enemy.boundleft -= 5
                    enemy.boundright -= 5
            for any in all_sprites:
                any.rect.move_ip(level.player.speedx, 0)
            if pygame.sprite.spritecollideany(level.player, environ):
                obstacle = pygame.sprite.spritecollideany(level.player, environ)
                level.player.rect.right = obstacle.rect.left
                for any in all_sprites:
                    any.rect.move_ip(-level.player.speedx, 0)
                for enemy in enemies:
                    enemy.boundleft -= level.player.speedx
                    enemy.boundright -= level.player.speedx
            level.player.speedx = 0
        if pressed_keys[K_SPACE]:
            if level.player.jump == False and level.player.grounded == True and level.player.speedy == 0:
                level.player.jump = True
                level.player.grounded = False
                level.player.speedy = -17
        level.player.rect.move_ip(0, level.player.speedy)
        level.player.speedy += 1
        if level.player.speedy > 21:
            level.player.speedy = 21
        objectcollide()

    # Attack handling
    if pressed_keys[K_a] and pressed_keys[K_d]:
        pass
    elif pressed_keys[K_a] and not pressed_keys[K_d]:
        level.player.facing = 0
    elif pressed_keys[K_d] and not pressed_keys[K_a]:
        level.player.facing = 1
    
    if level.player.facing == 1:
        level.weapon.surf = level.weapon.original
        level.weapon.rect.left = level.player.rect.right
    elif level.player.facing == 0:
        if level.weapon.surf == level.weapon.original:
            level.weapon.surf = pygame.transform.flip(level.weapon.surf, True, False)
        level.weapon.rect.right = level.player.rect.left
    
    if pressed_keys[K_k]:
        if level.weapon.sheathed and not level.weapon.attacking:
            weapons.add(level.weapon)
            all_sprites.add(level.weapon)
            level.weapon.hitframes = 20
            level.weapon.sheathed = False
            level.weapon.attacking = True
    level.weapon.rect.centery = level.player.rect.centery
    level.weapon.hitframes -= 1
    if level.weapon.hitframes < 0:
        level.weapon.hitframes = 0
        level.weapon.attacking = False
    elif level.weapon.hitframes <= 7:
        all_sprites.remove(level.weapon)
        weapons.remove(level.weapon)
        thejar.empty()
    elif level.weapon.hitframes <= 10:
        for i in enemies:
            i.beenhit = False

    if level.player.rect.centerx != width / 2:
        level.player.rect.centerx = width / 2
    
    # Display sprites on screen
    screen.fill((30, 30, 30))
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)
    screen.blit(level.player.surf, level.player.rect)

    visualhp.empty()
    for i in level.health:
        visualhp.add(i)
    for hp in visualhp:
        screen.blit(hp.surf, hp.rect)
    pygame.display.flip()

    # Level advancement conditions
    if lvlnum == 1:
        if pygame.sprite.collide_rect(level.player, level.door) and str(enemies) == "<Group(0 sprites)>":
            lvlnum = 2
            advance = True
            all_sprites.empty()
            environ.empty()
            enemies.empty()
    
    clock.tick(60)

pygame.quit()
