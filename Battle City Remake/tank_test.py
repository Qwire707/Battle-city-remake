import pygame

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
FPS = 30

window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_icon(pygame.image.load('textures/leaves.png'))
bg = pygame.transform.scale(pygame.image.load('textures/TESTbg.jpg'), (SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tank class TEST")
clock = pygame.time.Clock()

#клас для всіх спрайтів
class GameSprite(pygame.sprite.Sprite):
    #конструктор класу з властивостями
    def __init__(self, img, x, y, width, height, speed):
        super().__init__()
        self.width = width
        self.height = height
        self.image = pygame.transform.scale(pygame.image.load(img), (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
    # метод для малювання спрайту
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

#class tank
class Tank(GameSprite):
    '''Управління гравцем'''
    def update(self):
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys_pressed[pygame.K_d] and self.rect.x < SCREEN_WIDTH - self.width:
            self.rect.x += self.speed
        if keys_pressed[pygame.K_w] and self.rect.y > 0:
            self.rect.y -= self.speed
        if keys_pressed[pygame.K_s] and self.rect.y < SCREEN_HEIGHT - self.height:
            self.rect.y += self.speed

    def fire(self):
        bullet = Bullet('textures/TESTbullet.png', self.rect.centerx, self.rect.top, 15, 20, 10)
        bullets.add(bullet)

Tank = Tank("textures/TESTtank.png", SCREEN_WIDTH - 95, 25, 70, 70, 4)

#class enemy tank
class Enemy_Tank(GameSprite):
    direction = "right"
    directionn = "down"

    def update_r_l(self, start, end):
        if self.direction == "right":
            self.rect.x += self.speed

        if self.direction == "left":
            self.rect.x -= self.speed

        if self.direction == "right" and self.rect.x >= end:
            self.image = pygame.transform.scale(pygame.image.load("textures/TESTtank.png"), (self.width, self.height))
            self.direction = "left"

        if self.direction == "left" and self.rect.x <= start:
            self.image = pygame.transform.scale(pygame.image.load("textures/TESTtank.png"), (self.width, self.height))
            self.direction = "right"
    
    def update_u_d(self, start, end):
        if self.directionn == "up":
            self.rect.y += self.speed

        if self.directionn == "down":
            self.rect.y -= self.speed

        if self.directionn == "up" and self.rect.y >= end:
            self.image = pygame.transform.scale(pygame.image.load("textures/TESTtank.png"), (self.width, self.height))
            self.directionn = "down"

        if self.directionn == "down" and self.rect.y <= start:
            self.image = pygame.transform.scale(pygame.image.load("textures/TESTtank.png"), (self.width, self.height))
            self.directionn = "up"

enemy1 = Enemy_Tank("textures/TESTtank.png", 60, 700, 70, 70, 2)
enemy2 = Enemy_Tank("textures/TESTtank.png", 160, 0, 70, 70, 2)

#class bullet
class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= 0:
            self.kill()

bullets = pygame.sprite.Group()

num_fire = 0
rel_time = False
running = True

while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_SPACE:
                Tank.fire()

    window.blit(bg, (0,0))
    Tank.update()
    Tank.reset()
    bullets.draw(window)
    bullets.update()
    enemy1.reset()
    enemy1.update_r_l(200, 330)
    enemy2.reset()        
    enemy2.update_u_d(0, 130)    
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()















