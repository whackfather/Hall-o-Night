# Hall-o' Night
# Programmed by Roman Rodriguez

# Importing
import pygame
from pygame.locals import *
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
level = 1
advance = True
attacker = None

running = True
while running:
    # Level check
    if level == 1 and advance == True:
        from levelinterpret import *
        for i in levelsprites:
            all_sprites.add(i)
        for i in levelenviron:
            environ.add(i)
        for i in levelenemies:
            enemies.add(i)
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
                player.jump = False
            if event.key == K_k:
                weapon.sheathed = True
    
    # Enemy location update
    if level == 1:
        for enemy in levelenemies:
            enemy.update(player, enemy.home, enemy.beenhit, enemy.boundleft, enemy.boundright)
    elif level == 2:
        pass
    
    # Player, weapon, and enemy collision
    if pygame.sprite.groupcollide(weapons, enemies, False, False):
        hitenemy = pygame.sprite.spritecollideany(weapon, enemies)
        if hitenemy not in thejar:
            hitenemy.health -= 1
            hitenemy.beenhit = True
            thejar.add(hitenemy)
        if hitenemy.health == 0:
            hitenemy.kill()
    if pygame.sprite.spritecollideany(player, enemies):
        attacker = pygame.sprite.spritecollideany(player, enemies)
        if player not in playerjar:
            player.health -= 1
            levelhealth.remove(levelhealth[-1])
            player.beenhit = True
            playerjar.add(player)

    if player in playerjar and player.iframes > 0:
        player.iframes -= 1
        if player.iframes == 0:
            playerjar.empty()
            player.iframes = 15 
            player.beenhit = False
    if player.health == 0:
        player.kill()
        weapon.kill()
        running = False
    
    # Input reading
    pressed_keys = pygame.key.get_pressed()
    
    # Character location update
    player.update(pressed_keys, environ, player.beenhit, attacker, width, height)

    # Attack handling
    if pressed_keys[K_a] and pressed_keys[K_d]:
        pass
    elif pressed_keys[K_a] and not pressed_keys[K_d]:
        player.facing = 0
    elif pressed_keys[K_d] and not pressed_keys[K_a]:
        player.facing = 1
    
    if player.facing == 1:
        weapon.surf = weapon.original
        weapon.rect.left = player.rect.right
    elif player.facing == 0:
        if weapon.surf == weapon.original:
            weapon.surf = pygame.transform.flip(weapon.surf, True, False)
        weapon.rect.right = player.rect.left
    
    if pressed_keys[K_k]:
        if weapon.sheathed and not weapon.attacking:
            weapons.add(weapon)
            all_sprites.add(weapon)
            weapon.hitframes = 10
            weapon.sheathed = False
            weapon.attacking = True
    weapon.rect.centery = player.rect.centery
    weapon.hitframes -= 1
    if weapon.hitframes < 0:
        weapon.hitframes = 0
        all_sprites.remove(weapon)
        weapons.remove(weapon)
        weapon.attacking = False
        for i in enemies:
            i.beenhit = False
        thejar.empty()

    # Display sprites on screen
    screen.fill((30, 30, 30))
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)
    visualhp.empty()
    for i in levelhealth:
        visualhp.add(i)
    for hp in visualhp:
        screen.blit(hp.surf, hp.rect)
    pygame.display.flip()

    # Level advancement conditions
    if level == 1:
        if pygame.sprite.collide_rect(player, door) and str(enemies) == "<Group(0 sprites)>":
            level = 2
            advance = True
            all_sprites.empty()
            environ.empty()
            enemies.empty()
    
    clock.tick(60)

pygame.quit()
