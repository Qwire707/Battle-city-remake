import pygame
import os
import random

pygame.init()

# Constants
GAME_WIDTH = 600
PANEL_WIDTH = 200
SCREEN_WIDTH = GAME_WIDTH + PANEL_WIDTH
SCREEN_HEIGHT = 600
PLAYER_SPAWN_X = GAME_WIDTH - 95
PLAYER_SPAWN_Y = 25
RED_COLOR = (255, 0, 0)
BRICK_RED = (178, 34, 34)
WHITE_COLOR = (255, 255, 255)
GRAY = (70, 70, 70)
FPS = 60

# Global object list
game_objects = []

# Pygame setup
PATH = os.path.dirname(__file__) + os.path.sep
window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_icon(pygame.image.load('textures/leaves.png'))
pygame.display.set_caption("Battle City Remake")
clock = pygame.time.Clock()

lives = 3
paused = False

class SlidePanel:
    def __init__(self):
        self.font_large = pygame.font.SysFont("Courier New", 36, bold=True)
        self.font_small = pygame.font.SysFont("Courier New", 28)
        self.pause_btn = pygame.Rect(GAME_WIDTH + 40, 100, 120, 40)

    def draw(self, surface):
        pygame.draw.rect(surface, (30, 30, 30), (GAME_WIDTH, 0, PANEL_WIDTH, SCREEN_HEIGHT))
        pygame.draw.line(surface, WHITE_COLOR, (GAME_WIDTH, 0), (GAME_WIDTH, SCREEN_HEIGHT), 2)

        pygame.draw.rect(surface, GRAY, self.pause_btn)
        pygame.draw.rect(surface, WHITE_COLOR, self.pause_btn, 2)
        label = "RESUME" if paused else "PAUSE"
        pause_txt = self.font_small.render(label, True, WHITE_COLOR)
        surface.blit(pause_txt, pause_txt.get_rect(center=self.pause_btn.center))

        lives_txt = self.font_small.render(f"Lives: {lives}", True, WHITE_COLOR)

        #surface.blit(score_txt, (GAME_WIDTH + 30, 150))
        surface.blit(lives_txt, (GAME_WIDTH + 30, 190))

    def handle_event(self, event):
        global paused
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.pause_btn.collidepoint(event.pos):
                paused = not paused

# Block class
class Block:
    def __init__(self, px, py, size):
        game_objects.append(self)
        self.type = 'block'
        self.rect = pygame.Rect(px, py, size, size)
        self.hp = 1
        self.image = pygame.transform.scale(pygame.image.load('textures/brick_wall.png'), (size, size))

    def update(self):
        pass

    def draw(self):
        window.blit(self.image, self.rect.topleft)

    def damage(self, value):
        self.hp -= value
        if self.hp <= 0:
            game_objects.remove(self)


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
    def __init__(self, player_image, x, y, width, height, speed):
        super().__init__(player_image, x, y, width, height, speed)
        self.direction = 'UP'
    def update(self):
        oldX, oldY = self.rect.topleft
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
            self.direction = 'LEFT'
        if keys_pressed[pygame.K_d] and self.rect.x < SCREEN_WIDTH - self.width:
            self.rect.x += self.speed
            self.direction = 'RIGHT'
        if keys_pressed[pygame.K_w] and self.rect.y > 0:
            self.rect.y -= self.speed
            self.direction = 'UP'
        if keys_pressed[pygame.K_s] and self.rect.y < SCREEN_HEIGHT - self.height:
            self.rect.y += self.speed
            self.direction = "DOWN"
        
        for obj in game_objects:
            if obj != self and self.rect.colliderect(obj.rect):
                self.rect.topleft = oldX, oldY

    def fire(self):
        x, y = self.rect.centerx, self.rect.centery

        if self.direction == 'UP':
            y = self.rect.top
        elif self.direction == 'DOWN':
            y = self.rect.bottom
        elif self.direction == 'LEFT':
            x = self.rect.left
        elif self.direction == 'RIGHT':
            x = self.rect.right

        bullet = Bullet('textures/bullet.png', x, y, 15, 20, 10, self.direction)
        bullets.add(bullet)

    def respaewn(self):
        self.rect.x = PLAYER_SPAWN_X
        self.rect.y = PLAYER_SPAWN_Y

class EnemyManager:
    def __init__(self):
        self.enemies = pygame.sprite.Group()
        self.spawn_delay = 1000
        self.last_spawn_time = pygame.time.get_ticks()
        self.max_enemies = 3

    def spawn_enemy(self):
        enemy = Enemy_Tank(random.randint(0, GAME_WIDTH - 60), 0)
        self.enemies.add(enemy)

    def update(self):
        now = pygame.time.get_ticks()
        if len(self.enemies) < self.max_enemies and now - self.last_spawn_time >= self.spawn_delay:
            self.spawn_enemy()
            self.last_spawn_time = now
        self.enemies.update()

        for enemy in self.enemies:
            if random.randint(0, 100) < 2:
                enemy.fire()

    def draw(self, screen):
        self.enemies.draw(screen)
# Enemy tank class
class Enemy_Tank(GameSprite):
    def __init__(self, x, y):
        super().__init__('textures/enemy.png', x, y, 60, 60, 2)
        self.directions = ["up", "down", "left", "right"]
        self.direction = random.choice(self.directions)
        self.change_direction_timer = pygame.time.get_ticks()

    def update(self):
        # Рух
        self.move()
        old_x, old_y = self.rect.topleft

        now = pygame.time.get_ticks()
        if now - self.change_direction_timer > 2000:
            self.direction = random.choice(self.directions)
            self.change_direction_timer = now

        if self.rect.colliderect(player_tank.rect):
            self.rect.topleft = old_x, old_y
            self.direction = random.choice(self.directions)

    def move(self):
        old_pos = self.rect.topleft

        if self.direction == "up":
            self.rect.y -= self.speed
        elif self.direction == "down":
            self.rect.y += self.speed
        elif self.direction == "left":
            self.rect.x -= self.speed
        elif self.direction == "right":
            self.rect.x += self.speed

        if self.rect.left < 0 or self.rect.right > GAME_WIDTH or self.rect.top < 0 or self.rect.bottom > SCREEN_HEIGHT:
            self.rect.topleft = old_pos
            self.direction = random.choice(self.directions)

        for obj in game_objects:
            if obj.type == 'block' and self.rect.colliderect(obj.rect):
                self.rect.topleft = old_pos
                self.direction = random.choice(self.directions)
                break

    def fire(self):
        bullet = EnemyBullet("textures/bullet.png", self.rect.centerx, self.rect.bottom, 15, 20, 5)
        enemy_bullets.add(bullet)

class EnemyBullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y >= SCREEN_HEIGHT:
            self.kill()

        if self.rect.colliderect(player_tank.rect):
            self.kill()
            global lives
            lives -= 1
            player_tank.respaewn()
# Bullet class
class Bullet(GameSprite):
    def __init__(self, bullet_image, x, y, width, height, speed, direction):
        super().__init__(bullet_image, x, y, width, height, speed)
        self.direction = direction

    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= 0:
            self.kill()

        if self.direction == 'UP':
            self.rect.y -= self.speed
        elif self.direction == 'DOWN':
            self.rect.y += self.speed
        elif self.direction == 'LEFT':
            self.rect.x -= self.speed
        elif self.direction == 'RIGHT':
            self.rect.x += self.speed

        if (self.rect.y < 0 or self.rect.y > SCREEN_HEIGHT or
                self.rect.x < 0 or self.rect.x > SCREEN_WIDTH):
            self.kill()

        for enemy in enemy_manager.enemies:
            if self.rect.colliderect(enemy.rect):
                self.kill()
                enemy.kill()
                score_manager.add_score(100)
                break
        # Collision with blocks
        for block in game_objects:
            if block.rect.colliderect(self.rect):
                block.damage(1)
                self.kill()
                break

        for enemy in enemy_manager.enemies:
            if self.rect.colliderect(enemy.rect):
                self.kill()
                enemy.kill()
                break

bullets = pygame.sprite.Group()
enemy_bullets = pygame.sprite.Group()

# Initialize player tank
player_tank = Tank("textures/player.png", PLAYER_SPAWN_X, PLAYER_SPAWN_Y,  70, 70, 4)

class ScoreManager:
    def __init__(self):
        self.score = 0
        self.font = pygame.font.SysFont("Courier New", 28, bold=True)

    def add_score(self, points):
        self.score += points

    def draw(self, screen):
        text = self.font.render(f"Score: {self.score}", True, WHITE_COLOR)
        screen.blit(text, (GAME_WIDTH + 30, 150))

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
panel = SlidePanel()
enemy_manager = EnemyManager()
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
    Block(x, y, 50)

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
        else:
            panel.handle_event(event)

    # Drawing
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

        for obj in game_objects:
            obj.update()
            obj.draw()

        player_tank.update()
        player_tank.reset()

        bullets.update()
        enemy_bullets.update()

        pygame.sprite.groupcollide(bullets, enemy_bullets, True, True)
        bullets.draw(window)
        enemy_bullets.draw(window)
        panel.draw(window)
        enemy_manager.update()
        enemy_manager.draw(window)
        score_manager.draw(window)

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
