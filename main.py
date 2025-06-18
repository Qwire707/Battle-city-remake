import pygame
import os
import random

from settings import *
from menu import SlidePanel, MainMenu, LevelSelectMenu, EndGameScreen
from objects import Block1, Block2, Block3, Tank, EnemyManager, Bullet, EnemyBullet, ScoreManager, SuperEnemyManager, SuperEnemyTank, game_objects
from levels import Level

lives = 3
score = 0
paused = False
game_over = False
you_win = False
end_screen = None
bullets = pygame.sprite.Group()
enemy_bullets = pygame.sprite.Group()

pygame.init()
pygame.mixer.init()

pygame.mixer.music.load('sounds/batle city music.mp3')
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

bullet_sound = pygame.mixer.Sound('sounds/bullet_sound.wav')

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
player_tank = Tank("textures/player.png", PLAYER_SPAWN_X, PLAYER_SPAWN_Y, 40, 40, 4)
enemy_manager = EnemyManager(player_tank, enemy_bullets)
score_manager = ScoreManager()
super_enemy_manager = SuperEnemyManager(player_tank, enemy_bullets)

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
                bullet_sound.play()

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
            bullets.update(enemy_manager, score_manager, super_enemy_manager)
            enemy_bullets.update()

            if current_level and current_level.base:
                base_hits = pygame.sprite.spritecollide(current_level.base, enemy_bullets, True)
                if base_hits:
                    game_over = True
                    end_screen = EndGameScreen(window, "GAME OVER", score_manager.score)

            enemy_manager.update()
        else:

            for obj in game_objects:
                obj.draw(window)

        player_tank.reset(window)

        pygame.sprite.groupcollide(bullets, enemy_bullets, True, True)
        bullets.draw(window)
        enemy_bullets.draw(window)
        panel.draw(window, paused, player_tank)
        score_manager.draw(window)

        if score_manager.score < 1000:
            enemy_manager.update()
            enemy_manager.draw(window)
        else:
            super_enemy_manager.update()
            super_enemy_manager.draw(window)

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

            resume_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 20, 200, 60)
            pygame.draw.rect(window, GRAY, resume_button)
            pygame.draw.rect(window, WHITE_COLOR, resume_button, 3)

            button_font = pygame.font.SysFont("Courier New", 36)
            text_surface = button_font.render("RESUME", True, WHITE_COLOR)
            text_rect = text_surface.get_rect(center=resume_button.center)
            window.blit(text_surface, text_rect)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if resume_button.collidepoint(event.pos):
                        paused = False

            pygame.display.update()
            clock.tick(FPS)
            continue

        for obj in game_objects:
            obj.update()
            obj.draw(window)

        player_tank.update()
        player_tank.reset(window)

        bullets.update(enemy_manager, score_manager, super_enemy_manager)

        pygame.sprite.groupcollide(bullets, enemy_bullets, True, True)

        bullets.draw(window)
        enemy_bullets.draw(window)
        panel.draw(window, paused, player_tank)
        score_manager.draw(window)

        if player_tank.lives <= 0 and not game_over:
            game_over = True
            end_screen = EndGameScreen(window, "GAME OVER", score_manager.score)

        if score_manager.score >= WIN_SCORE and not you_win:
            you_win = True
            end_screen = EndGameScreen(window, "YOU WIN!", score_manager.score)

        if game_over or you_win:
            window.fill((30, 30, 30))
            end_screen.draw()
            pygame.display.update()

            waiting_for_input = True
            while waiting_for_input:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        waiting_for_input = False
                    result = end_screen.handle_event(event)
                    if result == "retry":
                        player_tank.lives = 3
                        score_manager.reset()
                        player_tank.reset_position()
                        enemy_manager.reset()
                        super_enemy_manager.reset()
                        bullets.empty()
                        enemy_bullets.empty()
                        game_over = False
                        you_win = False
                        current_level.reset()
                        end_screen = None
                        waiting_for_input = False
                    elif result == "exit":
                        game_over = False
                        you_win = False
                        in_level_select_menu = True
                        current_level = None
                        bullets.empty()
                        game_objects.clear()
                        end_screen = None
                        waiting_for_input = False

                clock.tick(FPS)
            continue


    pygame.display.update()
    clock.tick(FPS)

pygame.quit()