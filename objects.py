import pygame
import random

from settings import *

game_objects = []
decorations = []


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

    def reset(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))


class Block1:
    def __init__(self, px, py, size):
        game_objects.append(self)
        self.type = 'block'
        self.rect = pygame.Rect(px, py, size, size)
        self.hp = 1
        self.image = pygame.transform.scale(pygame.image.load('textures/brick_wall.png'), (size, size))

    def update(self):
        pass

    def draw(self, window):
        window.blit(self.image, self.rect.topleft)

    def damage(self, value):
        self.hp -= value
        if self.hp <= 0:
            game_objects.remove(self)


class Block2:
    def __init__(self, px, py, size):
        game_objects.append(self)
        self.type = 'block'
        self.rect = pygame.Rect(px, py, size, size)
        self.hp = 1000
        self.image = pygame.transform.scale(pygame.image.load('textures/steel_wall.png'), (size, size))

    def update(self):
        pass

    def draw(self, window):
        window.blit(self.image, self.rect.topleft)

    def damage(self, value):
        self.hp -= value
        if self.hp <= 0:
            game_objects.remove(self)


class Block3:
    def __init__(self, px, py, size):
        decorations.append(self)
        self.type = 'decor'
        self.rect = pygame.Rect(px, py, size, size)
        self.hp = -1
        self.image = pygame.transform.scale(pygame.image.load('textures/leaves.png'), (size, size))

    def update(self):
        pass

    def draw(self, window):
        window.blit(self.image, self.rect.topleft)

    def damage(self, value):
        pass

class Base:
    def __init__(self, x, y, size):
        self.image = pygame.image.load('textures/base.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (size, size))
        self.rect = pygame.Rect(x, y, size, size)
        self.alive = True

    def draw(self, screen):
        if self.alive:
            screen.blit(self.image, (self.rect.x, self.rect.y))

class Tank(GameSprite):
    def __init__(self, player_image, x, y, width, height, speed):
        super().__init__(player_image, x, y, width, height, speed)
        self.direction = 'UP'
        self.lives = 3
        self.start_x = x
        self.start_y = y

    def update(self):
        oldX, oldY = self.rect.topleft
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
            self.direction = 'LEFT'
            self.image = pygame.transform.scale(pygame.image.load("textures/player_l.png"), (self.width, self.height))
        if keys_pressed[pygame.K_d] and self.rect.x < SCREEN_WIDTH - self.width:
            self.rect.x += self.speed
            self.direction = 'RIGHT'
            self.image = pygame.transform.scale(pygame.image.load("textures/player_r.png"), (self.width, self.height))
        if keys_pressed[pygame.K_w] and self.rect.y > 0:
            self.rect.y -= self.speed
            self.direction = 'UP'
            self.image = pygame.transform.scale(pygame.image.load("textures/player_u.png"), (self.width, self.height))
        if keys_pressed[pygame.K_s] and self.rect.y < SCREEN_HEIGHT - self.height:
            self.rect.y += self.speed
            self.direction = "DOWN"
            self.image = pygame.transform.scale(pygame.image.load("textures/player_d.png"), (self.width, self.height))

        for obj in game_objects:
            if obj != self and self.rect.colliderect(obj.rect):
                self.rect.topleft = oldX, oldY

    def fire(self, bullets):
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

    def reset_position(self):
        self.rect.x = self.start_x
        self.rect.y = self.start_y


class SuperEnemyManager:
    def __init__(self, player_tank, enemy_bullets):
        self.super_enemies = pygame.sprite.Group()
        self.spawn_delay = 1000
        self.last_spawn_time = pygame.time.get_ticks()
        self.max_super_enemies = 3
        self.player_tank = player_tank
        self.enemy_bullets = enemy_bullets
        self.spawn_timer = 0

    def spawn_super_enemy(self):
        super_enemy = SuperEnemyTank(random.randint(0, GAME_WIDTH - 60), 0, self.player_tank, self.enemy_bullets)
        self.super_enemies.add(super_enemy)

    def update(self):
        now = pygame.time.get_ticks()
        if len(self.super_enemies) < self.max_super_enemies and now - self.last_spawn_time >= self.spawn_delay:
            self.spawn_super_enemy()
            self.last_spawn_time = now
        self.super_enemies.update()

        for super_enemy in self.super_enemies:
            if random.randint(0, 100) < 2:
                super_enemy.fire()

    def draw(self, screen):
        self.super_enemies.draw(screen)

    def reset(self):
        self.super_enemies.empty()
        self.spawn_timer = 0


class Bullet(GameSprite):
    def __init__(self, bullet_image, x, y, width, height, speed, direction):
        super().__init__(bullet_image, x, y, width, height, speed)
        self.direction = direction

    def update(self, enemy_manager, score_manager, super_enemy_manager):
        if self.direction == 'UP':
            self.rect.y -= self.speed
            self.image = pygame.transform.scale(pygame.image.load("textures/bullet_u.png"), (self.width, self.height))
        elif self.direction == 'DOWN':
            self.rect.y += self.speed
            self.image = pygame.transform.scale(pygame.image.load("textures/bullet_d.png"), (self.width, self.height))
        elif self.direction == 'LEFT':
            self.rect.x -= self.speed
            self.image = pygame.transform.scale(pygame.image.load("textures/bullet_l.png"), (self.width, self.height))
        elif self.direction == 'RIGHT':
            self.rect.x += self.speed
            self.image = pygame.transform.scale(pygame.image.load("textures/bullet_r.png"), (self.width, self.height))

        if (self.rect.y < 0 or self.rect.bottom > SCREEN_HEIGHT or
                self.rect.x < 0 or self.rect.right > SCREEN_WIDTH):
            self.kill()

        for enemy in enemy_manager.enemies:
            if self.rect.colliderect(enemy.rect):
                self.kill()
                enemy.kill()
                score_manager.add_score(100)
                break

        for super_enemy in super_enemy_manager.super_enemies:
            if self.rect.colliderect(super_enemy.rect):
                super_enemy.health -= 1
                if super_enemy.health <= 0:
                    super_enemy.kill()
                    score_manager.add_score(300)
                self.kill()
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

        for super_enemy in super_enemy_manager.super_enemies:
            if self.rect.colliderect(super_enemy.rect):
                super_enemy.health -= 1
                if super_enemy.health <= 0:
                    self.kill()
                    super_enemy.kill()
                    break


class EnemyManager:
    def __init__(self, player_tank, enemy_bullets):
        self.enemies = pygame.sprite.Group()
        self.spawn_delay = 1000
        self.last_spawn_time = pygame.time.get_ticks()
        self.max_enemies = 3
        self.player_tank = player_tank
        self.enemy_bullets = enemy_bullets
        self.spawn_timer = 0

    def spawn_enemy(self):
        enemy = Enemy_Tank(random.randint(0, GAME_WIDTH - 60), 0, self.player_tank, self.enemy_bullets)
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

    def reset(self):
        self.enemies.empty()
        self.spawn_timer = 0


# Enemy tank class
class Enemy_Tank(GameSprite):
    def __init__(self, x, y, player_tank, enemy_bullets):
        super().__init__('textures/enemy.png', x, y, 40, 40, 2)
        self.directions = ["UP", "DOWN", "LEFT", "RIGHT"]
        self.direction = random.choice(self.directions)
        self.change_direction_timer = pygame.time.get_ticks()
        self.player_tank = player_tank
        self.enemy_bullets = enemy_bullets

    def update(self):
        # Рух
        self.move()
        old_x, old_y = self.rect.topleft

        now = pygame.time.get_ticks()
        if now - self.change_direction_timer > 2000:
            self.direction = random.choice(self.directions)
            self.change_direction_timer = now

        if self.rect.colliderect(self.player_tank.rect):
            self.rect.topleft = old_x, old_y
            self.direction = random.choice(self.directions)

    def move(self):
        old_pos = self.rect.topleft

        if self.direction == "UP":
            self.rect.y -= self.speed
            self.image = pygame.transform.scale(pygame.image.load("textures/enemy_u.png"), (self.width, self.height))
        elif self.direction == "DOWN":
            self.rect.y += self.speed
            self.image = pygame.transform.scale(pygame.image.load("textures/enemy_d.png"), (self.width, self.height))
        elif self.direction == "LEFT":
            self.rect.x -= self.speed
            self.image = pygame.transform.scale(pygame.image.load("textures/enemy_l.png"), (self.width, self.height))
        elif self.direction == "RIGHT":
            self.rect.x += self.speed
            self.image = pygame.transform.scale(pygame.image.load("textures/enemy_r.png"), (self.width, self.height))

        if self.rect.left < 0 or self.rect.right > GAME_WIDTH or self.rect.top < 0 or self.rect.bottom > SCREEN_HEIGHT:
            self.rect.topleft = old_pos
            self.direction = random.choice(self.directions)

        for obj in game_objects:
            if obj.type == 'block' and self.rect.colliderect(obj.rect):
                self.rect.topleft = old_pos
                self.direction = random.choice(self.directions)
                break

    def fire(self):
        bullet = EnemyBullet("textures/bullet.png", self.rect.centerx, self.rect.centery, 15, 20, 5, self.direction, self.player_tank)
        self.enemy_bullets.add(bullet)


class EnemyBullet(GameSprite):
    def __init__(self, image, x, y, width, height, speed, direction, player_tank):
        super().__init__(image, x, y, width, height, speed)
        self.direction = direction.upper()
        self.player_tank = player_tank

    def update(self):
        if self.direction == "UP":
            self.rect.y -= self.speed
        elif self.direction == "DOWN":
            self.rect.y += self.speed
        elif self.direction == "LEFT":
            self.rect.x -= self.speed
        elif self.direction == "RIGHT":
            self.rect.x += self.speed

        if self.rect.colliderect(self.player_tank.rect):
            self.kill()
            self.player_tank.lives -= 1
            self.player_tank.respaewn()

        if (self.rect.y < 0 or self.rect.y > SCREEN_HEIGHT or
            self.rect.x < 0 or self.rect.x > GAME_WIDTH):
            self.kill()

        for block in game_objects:
            if block.rect.colliderect(self.rect):
                if hasattr(block, "damage"):
                    block.damage(1)
                self.kill()
                break


class SuperEnemyTank(GameSprite):
    def __init__(self, x, y, player_tank, enemy_bullets):
        super().__init__('textures/large_enemy_u.png', x, y, 50, 50, 2)
        self.directions = ["UP", "DOWN", "LEFT", "RIGHT"]
        self.direction = random.choice(self.directions)
        self.player_tank = player_tank
        self.enemy_bullets = enemy_bullets
        self.health = 3
        self.change_direction_timer = pygame.time.get_ticks()

    def update(self):
        # Рух
        self.move()
        old_x, old_y = self.rect.topleft

        now = pygame.time.get_ticks()
        if now - self.change_direction_timer > 2000:
            self.direction = random.choice(self.directions)
            self.change_direction_timer = now

        if self.rect.colliderect(self.player_tank.rect):
            self.rect.topleft = old_x, old_y
            self.direction = random.choice(self.directions)

    def move(self):
        old_pos = self.rect.topleft

        if self.direction == "UP":
            self.rect.y -= self.speed
            self.image = pygame.transform.scale(pygame.image.load("textures/large_enemy_u.png"),
                                                (self.width, self.height))
        elif self.direction == "DOWN":
            self.rect.y += self.speed
            self.image = pygame.transform.scale(pygame.image.load("textures/large_enemy_d.png"),
                                                (self.width, self.height))
        elif self.direction == "LEFT":
            self.rect.x -= self.speed
            self.image = pygame.transform.scale(pygame.image.load("textures/large_enemy_l.png"),
                                                (self.width, self.height))
        elif self.direction == "RIGHT":
            self.rect.x += self.speed
            self.image = pygame.transform.scale(pygame.image.load("textures/large_enemy_r.png"),
                                                (self.width, self.height))

        if self.rect.left < 0 or self.rect.right > GAME_WIDTH or self.rect.top < 0 or self.rect.bottom > SCREEN_HEIGHT:
            self.rect.topleft = old_pos
            self.direction = random.choice(self.directions)

        for obj in game_objects:
            if obj.type == 'block' and self.rect.colliderect(obj.rect):
                self.rect.topleft = old_pos
                self.direction = random.choice(self.directions)
                break

    def fire(self):
        bullet = EnemyBullet("textures/bullet_u.png", self.rect.centerx, self.rect.bottom, 15, 20, 5, self.direction, self.player_tank)
        self.enemy_bullets.add(bullet)


class ScoreManager:
    def __init__(self):
        self.score = 0
        self.font = pygame.font.SysFont("Courier New", 24, bold=True)

    def add_score(self, points):
        self.score += points

    def draw(self, screen):
        text = self.font.render(f"Score: {self.score}", True, WHITE_COLOR)
        screen.blit(text, (GAME_WIDTH + 30, 150))

    def reset(self):
        self.score = 0