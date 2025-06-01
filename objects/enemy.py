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