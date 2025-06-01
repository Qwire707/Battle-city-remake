import pygame
import os
import random

from settings import *
from menu import SlidePanel, MainMenu, LevelSelectMenu
from objects import Block1, Block2, Block3, Tank, EnemyManager, Bullet, EnemyBullet, ScoreManager, game_objects
from levels import Level

lives = 3
paused = False
bullets = pygame.sprite.Group()
enemy_bullets = pygame.sprite.Group()

pygame.init()

window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_icon(pygame.image.load('textures/leaves.png'))
pygame.display.set_caption("Battle City Remake")
clock = pygame.time.Clock()

in_main_menu = True
in_level_select_menu = False
current_level = None
menu = MainMenu(window)
level_select_menu = LevelSelectMenu(window)
panel = SlidePanel()
player_tank = Tank("textures/player.png", PLAYER_SPAWN_X, PLAYER_SPAWN_Y, 70, 70, 4)
enemy_manager = EnemyManager(player_tank, enemy_bullets)
score_manager = ScoreManager()

for _ in range(10):
    while True:
        x = random.randint(0, SCREEN_WIDTH // 50 - 1) * 50
        y = random.randint(0, SCREEN_HEIGHT // 50 - 1) * 50
        rect = pygame.Rect(x, y, 50, 50)
        fined = False
        for obj in game_objects:
            if rect.colliderect(obj.rect):
                fined = True
        if not fined:
            break
    Block1(x, y, 50)

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player_tank.fire(bullets)

        if in_main_menu:
            result = menu.handle_event(event)
            if result == "start_game":
                in_main_menu = False
                in_level_select_menu = True

        elif in_level_select_menu:
            result = level_select_menu.handle_event(event)
            if result == "back_to_main":
                in_level_select_menu = False
                in_main_menu = True
            elif result and result.startswith("start_level_"):
                level_number = int(result.split("_")[-1])
                current_level = Level(level_number)
                in_level_select_menu = False
        else:
            paused = panel.handle_event(event, paused)

    if in_main_menu:
        window.fill((0, 0, 0))
        menu.draw_title()
        menu.draw_button()

    elif in_level_select_menu:
        level_select_menu.draw()

    else:
        window.fill((0, 0, 0))
        if current_level:
            current_level.update()
            current_level.draw(window)

        # Add pause text
        if not paused:
            for obj in game_objects:
                obj.update()
                obj.draw(window)

            player_tank.update()
            bullets.update()
            enemy_bullets.update()
            enemy_manager.update()
        else:

            for obj in game_objects:
                obj.draw(window)

        player_tank.reset(window)

        pygame.sprite.groupcollide(bullets, enemy_bullets, True, True)
        bullets.draw(window)
        enemy_bullets.draw(window)
        enemy_manager.draw(window)
        panel.draw(window, paused, lives)
        score_manager.draw(window)

        # Add pause text
        if paused:
            overlay = pygame.Surface((GAME_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(180)
            overlay.fill((0, 0, 0))
            window.blit(overlay, (0, 0))

            pause_font = pygame.font.SysFont("Courier New", 72, bold=True)
            pause_text = pause_font.render("PAUSED", True, WHITE_COLOR)
            pause_rect = pause_text.get_rect(center=(GAME_WIDTH // 2, SCREEN_HEIGHT // 2))
            window.blit(pause_text, pause_rect)

        for obj in game_objects:
            obj.update()
            obj.draw(window)

        player_tank.update()
        player_tank.reset(window)

        bullets.update(enemy_manager, score_manager)
        bullets.update()

        pygame.sprite.groupcollide(bullets, enemy_bullets, True, True)

        bullets.draw(window)
        enemy_bullets.draw(window)
        panel.draw(window, paused, lives)
        enemy_manager.update()
        enemy_manager.draw(window)
        score_manager.draw(window)

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()