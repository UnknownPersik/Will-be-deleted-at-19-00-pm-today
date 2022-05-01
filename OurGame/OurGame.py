import pygame, random, enum, os
from datetime import datetime

WIDTH = 800
HEIGHT = 650
FPS = 30

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
info = pygame.Surface((WIDTH, HEIGHT / 3))
window = pygame.Surface((WIDTH, HEIGHT))
pygame.display.set_caption("Mad Mario")
clock = pygame.time.Clock()

class Conditions(enum.IntEnum):
    DEAD = 0
    JUMP = 1
    RUN = 2
    SHOOT = 3
    STAND = 4

class EnemyConditions(enum.IntEnum):
    DEAD = 0
    RUN = 1
    SHOOT = 2
    STAND = 3

class BulletConditions(enum.IntEnum):
    RUN = 0

class Menu:
    def __init__(self, punkts = [400, 350, u'Punkt', (250,250,30), (250,30,250)]):
        self.punkts = punkts
    def render(self, poverhnost, font, num_punkt):
        for i in self.punkts:
            if num_punkt == i[5]:
                poverhnost.blit(font.render(i[2], 1, i[4]), (i[0], i[1]-30))
            else:
                poverhnost.blit(font.render(i[2], 1, i[3]), (i[0], i[1]-30))
    def menu(self):
        done = True
        font_menu = pygame.font.Font(None, 50)
        pygame.key.set_repeat(0,0)
        pygame.mouse.set_visible(True)
        punkt = 0
        while done:
            info.fill((0, 100, 200))
            window.fill((0, 100, 200))
 
            mp = pygame.mouse.get_pos()
            for i in self.punkts:
                if mp[0]>i[0] and mp[0]<i[0]+155 and mp[1]>i[1] and mp[1]<i[1]+50:
                    punkt =i[5]
            self.render(window, font_menu, punkt)
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.exit()
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_ESCAPE:
                       pygame.exit()
                    if e.key == pygame.K_UP:
                        if punkt > 0:
                           punkt -= 1
                    if e.key == pygame.K_DOWN:
                        if punkt < len(self.punkts)-1:
                           punkt += 1
                if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                    if punkt == 0:
                        done = False
                    elif punkt == 1:
                        exit()
            screen.blit(info, (0, 0))
            screen.blit(window, (0, 30))
            pygame.display.flip()

class Player(pygame.sprite.Sprite):
    def __init__(self, screen_size, player_pos):
        pygame.sprite.Sprite.__init__(self)
        self.condition = {
            Conditions.DEAD: [],
            Conditions.RUN: [],
            Conditions.SHOOT: [],
            Conditions.STAND: [],
            Conditions.JUMP: []
        }
        img_player_path = os.path.join('img', 'mario')
        for k, i in enumerate(os.listdir(img_player_path)):
            img_dir = os.listdir(os.path.join(img_player_path, i))
            for j in img_dir:
                image = pygame.image.load(os.path.join(img_player_path, i, j)).convert()
                image.set_colorkey((0, 0, 0))
                self.condition[Conditions(k)].append(pygame.transform.scale(image, screen_size))
 
        self.cur_condition = self.condition[Conditions.RUN]
        self.cur_image = 0
        self.image = self.condition[Conditions.RUN][self.cur_image]
        self.rect = self.image.get_rect()
        self.rect.bottomleft = player_pos
        self.shoot_delay = 250
        self.last_shoot = pygame.time.get_ticks()
        self.is_jumping = False
        self.jump_counter = 0
        self.jump_mas = []

    def update(self):
        if self.is_jumping:
            self.image = self.condition[Conditions.JUMP][0]
            if self.jump_counter < len(self.jump_mas):
 
                if self.jump_mas[self.jump_counter] == 0:
                    self.jump_counter += 2
                    self.rect.y -= 10 * self.jump_mas[self.jump_counter - 1]
                else:
                    self.jump_mas[self.jump_counter] -= 1
            else:
                self.is_jumping = False
        else:
            self.image = self.cur_condition[self.cur_image]
            self.cur_image = (self.cur_image + 1) % len(self.cur_condition)
 

    def set_condition(self, cond):
        self.cur_image = 0
        self.cur_condition = self.condition[cond]
 
    def jump(self):
        self.is_jumping = True
        self.jump_counter = 0
        self.jump_mas = [1, 1] * 10 + [1, -1] * 10

        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_SPACE]:
            self.shoot()

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shoot > self.shoot_delay:
            self.last_shoot = now
            bullet = Bullet1(self.rect.centerx, self.rect.top)
            all_sprites.add(bullet)

class Enemy(pygame.sprite.Sprite):
    def __init__(self, screen_size, enemy_pos):
        pygame.sprite.Sprite.__init__(self)
        self.condition = {
            EnemyConditions.DEAD: [],
            EnemyConditions.RUN: [],
            EnemyConditions.STAND: [],
            EnemyConditions.SHOOT: []
        }
        img_enemy_path = os.path.join('img', 'enemy')
        for k, i in enumerate(os.listdir(img_enemy_path)):
            img_enemy_dir = os.listdir(os.path.join(img_enemy_path, i))
            for j in img_enemy_dir:
                image = pygame.image.load(os.path.join(img_enemy_path, i, j)).convert()
                image.set_colorkey((255, 255, 255))
                self.condition[EnemyConditions(k)].append(pygame.transform.scale(image, screen_size))
        self.cur_condition = self.condition[EnemyConditions.RUN]
        self.cur_image = 0
        self.image = self.condition[EnemyConditions.RUN][self.cur_image]
        self.rect = self.image.get_rect()
        self.rect.bottomright = enemy_pos
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()
        self.moving = 2
                
    def update(self):
        self.image = self.cur_condition[self.cur_image]
        self.cur_image = (self.cur_image + 1) % len(self.cur_condition)
        self.rect.x -= self.moving
        if self.rect.x < WIDTH / 3 * 2:
            self.moving = 0

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > random.randint(1500, 2500):
            self.last_shot = now
            bullet = Bullet(self.rect.centerx, self.rect.top)
            all_sprites.add(bullet)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.condition = {
            BulletConditions.RUN: []
        }
        img_bullet_path = os.path.join('img', 'bullet')
        for k, i in enumerate(os.listdir(img_bullet_path)):
            img_bullet_dir = os.listdir(os.path.join(img_bullet_path, i))
            for j in img_bullet_dir:
                image = pygame.image.load(os.path.join(img_bullet_path, i, j)).convert()
                image.set_colorkey((0, 0, 0))
                self.condition[BulletConditions(k)].append(image)
        self.cur_condition = self.condition[BulletConditions.RUN]
        self.cur_image = 0
        self.image = self.condition[BulletConditions.RUN][self.cur_image]
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedx = -20

    def update(self):
        self.rect.x += self.speedx
        self.rect.y = HEIGHT -35
        if self.rect.bottom < 0:
            self.kill()

class Bullet1(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.condition = {
            BulletConditions.RUN: []
        }
        img_bullet_path = os.path.join('img', 'bullet')
        for k, i in enumerate(os.listdir(img_bullet_path)):
            img_bullet_dir = os.listdir(os.path.join(img_bullet_path, i))
            for j in img_bullet_dir:
                image = pygame.image.load(os.path.join(img_bullet_path, i, j)).convert()
                image.set_colorkey((0, 0, 0))
                self.condition[BulletConditions(k)].append(image)
        self.cur_condition = self.condition[BulletConditions.RUN]
        self.cur_image = 0
        self.image = self.condition[BulletConditions.RUN][self.cur_image]
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedx = -20

    def update(self):
        self.rect.x += self.speedx
        self.rect.y = HEIGHT -35
        if self.rect.bottom < 0:
            self.kill()


all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()
player = Player((250, 100), (0, HEIGHT))
enemy = Enemy((250,100), (WIDTH, HEIGHT))
all_sprites.add(enemy)
all_sprites.add(player)
player.set_condition(Conditions.RUN)
punkts = [(350, 300, u'Play', (11, 0, 77), (250,250,30), 0),
          (350, 340, u'Exit', (11, 0, 77), (250,250,30), 1)]
game = Menu(punkts)
game.menu()
cur_tick = pygame.time.get_ticks()


running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if not player.is_jumping:
                    player.jump()
    enemy.shoot()
    #hits = pygame.sprite.groupcollide(enemies, )
    all_sprites.update()
    screen.fill(WHITE)
    all_sprites.draw(screen)
    pygame.display.flip()

pygame.quit()
