import pygame
import os
from random import randint

pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
RED_COLOR = (255, 0, 0)
BRICK_RED = (178, 34, 34)
WHITE_COLOR = (255, 255, 255)
GRAY = (70, 70, 70)
FPS = 60
tileSize = 40

# Pygame setup
PATH = os.path.dirname(__file__) + os.path.sep
window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_icon(pygame.image.load('leaves.png'))
pygame.display.set_caption("Battle City Remake")
clock = pygame.time.Clock()
game_objects = []

# Block class
class Block_1:
    def __init__(self, px, py, size):
        game_objects.append(self)
        self.type = 'block'
        self.rect = pygame.Rect(px, py, size, size)
        self.hp = 1
        self.image = pygame.transform.scale(pygame.image.load('brick_wall.png'), (size, size))

    def update(self):
        pass

    def draw(self):
        window.blit(self.image, self.rect.topleft)

    def damage(self, value):
        self.hp -= value
        if self.hp <= 0:
            game_objects.remove(self)

class Block_2:
    def __init__(self, px, py, size):
        game_objects.append(self)
        self.type = 'block'
        self.rect = pygame.Rect(px, py, size, size)
        self.hp = 1000
        self.image = pygame.transform.scale(pygame.image.load('steel_wall.png'), (size, size))

    def update(self):
        pass

    def draw(self):
        window.blit(self.image, self.rect.topleft)

    def damage(self, value):
        self.hp -= value
        if self.hp <= 0:
            game_objects.remove(self)

# Карта уровня
level_map = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
]

# Генерация карты
for row_idx, row in enumerate(level_map):
    for col_idx, val in enumerate(row):
        if val == 1:
            Block_1(col_idx * tileSize, row_idx * tileSize, tileSize)
        if val == 2:
            Block_2(col_idx * tileSize, row_idx * tileSize, tileSize)

        

# Sprite base class
class GameSprite(pygame.sprite.Sprite):
    def __init__(self, img, x, y, width, height, speed):
        super().__init__()
        self.width = width
        self.height = height
        self.image = pygame.transform.scale(pygame.image.load(img), (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

# Player tank class
class Tank(GameSprite):
    def update(self):
        oldX, oldY = self.rect.topleft
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys_pressed[pygame.K_d] and self.rect.x < SCREEN_WIDTH - self.width:
            self.rect.x += self.speed
        if keys_pressed[pygame.K_w] and self.rect.y > 0:
            self.rect.y -= self.speed
        if keys_pressed[pygame.K_s] and self.rect.y < SCREEN_HEIGHT - self.height:
            self.rect.y += self.speed
        
        for obj in game_objects:
            if obj != self and self.rect.colliderect(obj.rect):
                self.rect.topleft = oldX, oldY

    def fire(self):
        bullet = Bullet('TESTbullet.png', self.rect.centerx, self.rect.top, 15, 20, 10)
        bullets.add(bullet)

# Enemy tank class
class Enemy_Tank(GameSprite):
    direction = "right"
    directionn = "down"

    def update_r_l(self, start, end):
        if self.direction == "right":
            self.rect.x += self.speed
        elif self.direction == "left":
            self.rect.x -= self.speed

        if self.direction == "right" and self.rect.x >= end:
            self.direction = "left"
        elif self.direction == "left" and self.rect.x <= start:
            self.direction = "right"

    def update_u_d(self, start, end):
        if self.directionn == "down":
            self.rect.y += self.speed
        elif self.directionn == "up":
            self.rect.y -= self.speed

        if self.directionn == "down" and self.rect.y >= end:
            self.directionn = "up"
        elif self.directionn == "up" and self.rect.y <= start:
            self.directionn = "down"

# Bullet class
class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= 0:
            self.kill()
        for block in game_objects:
            if block.rect.colliderect(self.rect):
                block.damage(1)
                self.kill()
                break

bullets = pygame.sprite.Group()

# Initialize player tank
player_tank = Tank("TESTtank.png", SCREEN_WIDTH - 600, 470, 70, 70, 4)

# Level and menu system
class Level:
    def __init__(self, level_number: int):
        self.level_number = level_number

    def load_map(self, level_number: int):
        pass

    def update(self):
        pass

    def draw(self, screen):
        pass

class MainMenu:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.title_font = pygame.font.SysFont("Courier New", 72, bold=True)
        self.button_font = pygame.font.SysFont("Courier New", 36, bold=True)
        self.button_width = 240
        self.button_height = 60
        self.button_rect = pygame.Rect(
            SCREEN_WIDTH // 2 - self.button_width // 2,
            SCREEN_HEIGHT // 2 - self.button_height // 4,
            self.button_width,
            self.button_height
        )

    def draw_title(self):
        title_text = "BATTLE CITY REMAKE"
        title_surface = self.title_font.render(title_text, True, BRICK_RED)
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
        self.screen.blit(title_surface, title_rect)

    def draw_button(self):
        pygame.draw.rect(self.screen, GRAY, self.button_rect)
        pygame.draw.rect(self.screen, WHITE_COLOR, self.button_rect, 3)

        text_surface = self.button_font.render("PLAY GAME", True, WHITE_COLOR)
        text_rect = text_surface.get_rect(center=self.button_rect.center)
        self.screen.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.button_rect.collidepoint(event.pos):
                return "start_game"
        return None

class LevelSelectMenu:
    def __init__(self, screen):
        self.screen = screen
        self.title_font = pygame.font.SysFont("Courier New", 60, bold=True)
        self.button_font = pygame.font.SysFont("Courier New", 28, bold=True)
        self.level_buttons = []
        self.menu_button = pygame.Rect(20, 20, 120, 50)

        for i in range(3):
            rect = pygame.Rect(150 + i * 200, 250, 150, 150)
            self.level_buttons.append((i + 1, rect))

    def draw(self):
        self.screen.fill((0, 0, 0))
        title_surface = self.title_font.render("SELECT LEVEL", True, BRICK_RED)
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 100))
        self.screen.blit(title_surface, title_rect)

        for level_number, rect in self.level_buttons:
            pygame.draw.rect(self.screen, GRAY, rect)
            pygame.draw.rect(self.screen, WHITE_COLOR, rect, 3)
            text_surface = self.button_font.render(f"Level {level_number}", True, WHITE_COLOR)
            text_rect = text_surface.get_rect(center=rect.center)
            self.screen.blit(text_surface, text_rect)

        pygame.draw.rect(self.screen, BRICK_RED, self.menu_button)
        pygame.draw.rect(self.screen, WHITE_COLOR, self.menu_button, 3)
        menu_text = self.button_font.render("MENU", True, WHITE_COLOR)
        menu_text_rect = menu_text.get_rect(center=self.menu_button.center)
        self.screen.blit(menu_text, menu_text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.menu_button.collidepoint(event.pos):
                return "back_to_main"

            for level_number, rect in self.level_buttons:
                if rect.collidepoint(event.pos):
                    return f"start_level_{level_number}"
        return None

# Game state
in_main_menu = True
in_level_select_menu = False
current_level = None
menu = MainMenu(window)
level_select_menu = LevelSelectMenu(window)

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player_tank.fire()

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

    # Drawing
    if in_main_menu:
        window.fill((0, 0, 0))
        menu.draw_title()
        menu.draw_button()

    elif in_level_select_menu:
        level_select_menu.draw()

    else:
        window.fill((255, 255, 255))
        if current_level:
            current_level.update()
            current_level.draw(window)

        for obj in game_objects:
            obj.update()
            obj.draw()

        player_tank.update()
        player_tank.reset()

        bullets.update()
        bullets.draw(window)

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
