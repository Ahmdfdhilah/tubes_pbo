from ast import With
from asyncio import current_task
from glob import iglob
from importlib.util import set_loader
from lib2to3.pytree import convert
from turtle import update
import pygame
import random
import os
from pygame.locals import *

WIDTH = 400
HEIGHT = 640
FPS = 60

# Warna
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BG = (100, 100, 100)

# Health Bar
HEALTH_WIDTH = 200
HEALTH_HEIGHT = 20

mouse_pos = (0, 0)
show_mouse_pos = True

game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, "Assets")
car_folder = os.path.join(img_folder, "Car")
life_folder = os.path.join(img_folder, "Lifebar")
object_folder = os.path.join(img_folder, "Object")

def draw_text(text, font_size, font_color, x, y):
    font = pygame.font.SysFont(None, font_size)
    img_font = font.render(text, True, font_color)
    screen.blit(img_font, (x, y))

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Car Racing')
clock = pygame.time.Clock()

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load(os.path.join(car_folder, "car_6.png")).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 4

    def update(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_RIGHT] and self.rect.right < 357:
            self.rect.move_ip(self.speed, 0)
        if key[pygame.K_LEFT] and self.rect.left > 45:
            self.rect.move_ip(-self.speed, 0)

class PanahJalan(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(os.path.join(object_folder, "arrow_white.png")).convert_alpha(), (100, 50))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        if self.rect.y > HEIGHT:
            self.kill()

class Car(pygame.sprite.Sprite):
    def __init__(self, x, img):
        super().__init__()
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = -250
        self.hit = False

    def update(self):
        if self.rect.y > HEIGHT:
            self.kill()

class Batu(pygame.sprite.Sprite):
    def __init__(self, x, img):
        super().__init__()
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = -50
        self.hit = False

    def update(self):
        if self.rect.y > HEIGHT:
            self.kill()

class Bensin(pygame.sprite.Sprite):
    def __init__(self, x, img):
        super().__init__()
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = -50
        self.hit = False

    def update(self):
        if self.rect.y > HEIGHT:
            self.kill()

tribune = pygame.transform.rotate(pygame.image.load(os.path.join(object_folder, "tribune.png")).convert_alpha(), 90)
tribune_kiri = pygame.transform.scale(tribune, (144, HEIGHT))
tribune_kanan = pygame.transform.scale(tribune, (144, HEIGHT))

car_list = []
for i in range(8):
    img = pygame.image.load(os.path.join(car_folder, "car_{}.png".format(i))).convert_alpha()
    car_list.append(img)

batu_list = []
for i in range(3):
    img = pygame.image.load(os.path.join(object_folder, "rock_{}.png".format(i))).convert_alpha()
    batu_list.append(img)

bensin_img = pygame.image.load(os.path.join(object_folder, "gas.png")).convert_alpha()

all_sprites = pygame.sprite.Group()
panahGrup = pygame.sprite.Group()
cars = pygame.sprite.Group()
batus = pygame.sprite.Group()
bensins = pygame.sprite.Group()

b = Batu(random.randrange(82, 302), random.choice(batu_list))
batus.add(b)

mobil = Car(random.randrange(82, 302), random.choice(car_list))
cars.add(mobil)

for i in range(3):
    panah = PanahJalan(WIDTH//2 -50, i * 230 + 40)
    panahGrup.add(panah)

player = Player(WIDTH // 2 - 30, HEIGHT // 2 + 100)
all_sprites.add(player)

# Health Bar
health = 100

# Score
score = 0
score_font = pygame.font.SysFont(None, 30)

run = True
scene = {
    0: "MAIN MENU",
    1: "PLAY",
    2: "GAME OVER",
}

current_scene = 0
while run:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == KEYUP:
            if event.key == K_r and current_scene == 2:
                all_sprites.empty()
                panahGrup.empty()
                cars.empty()
                batus.empty()
                bensins.empty()

                b = Batu(random.randrange(82, 302), random.choice(batu_list))
                batus.add(b)

                mobil = Car(random.randrange(82, 302), random.choice(car_list))
                cars.add(mobil)

                for i in range(3):
                    panah = PanahJalan(WIDTH//2 -50, i * 230 + 40)
                    panahGrup.add(panah)

                player = Player(WIDTH // 2 - 30, HEIGHT // 2 + 100)
                all_sprites.add(player)

                # Reset health
                health = 100

                # Reset score
                score = 0

                current_scene = 1

        if event.type == KEYDOWN:
            if event.key == K_x:
                show_mouse_pos = not show_mouse_pos

            mouse_pos = pygame.mouse.get_pos()
            if event.key == K_ESCAPE and current_scene == 0:
                run = False
            if event.key == K_ESCAPE and current_scene == 2:
                run = False
            if event.key == K_SPACE and current_scene == 0:
                current_scene = 1

    if scene.get(current_scene) == "PLAY":
        for panah in panahGrup:
            panah.rect.y += 2

        for car in cars:
            car.rect.y += 3

        for batu in batus:
            batu.rect.y += 2

        for bensin in bensins:
            bensin.rect.y += 2

        while len(panahGrup) < 3:
            panah_new = PanahJalan(WIDTH // 2 - 50, -50)
            panahGrup.add(panah_new)

        while len(cars) < 1:
            mobil_new = Car(random.randrange(82, 302), random.choice(car_list))
            cars.add(mobil_new)

        while len(batus) < 1:
            b_new = Batu(random.randrange(82, 302), random.choice(batu_list))
            batus.add(b_new)

        while len(bensins) < 1:
            bensin_new = Bensin(random.randrange(82, 302), bensin_img)
            bensins.add(bensin_new)

        # Check Collision
        kena_mobil = pygame.sprite.spritecollide(player, cars, True)
        if kena_mobil:
            for m in kena_mobil:
                if not m.hit:
                    m.hit = True
                    health -= 10
                    if health <= 0:
                        current_scene = 2
            kena_mobil_sfx = pygame.mixer.Sound("sound\Duar.mp3")
            kena_mobil_sfx.play()

        kena_batu = pygame.sprite.spritecollide(player, batus, True)
        if kena_batu:
            for b in kena_batu:
                if not b.hit:
                    b.hit = True
                    health -= 10
                    if health <= 0:
                        current_scene = 2
            kena_batu_sfx = pygame.mixer.Sound("sound\Duar.mp3")
            kena_batu_sfx.play()

        kena_bensin = pygame.sprite.spritecollide(player, bensins, True)
        if kena_bensin:
            for bensin in kena_bensin:
                if not bensin.hit:
                    bensin.hit = True
                    health += 10
                    if health > 100:
                        health = 100

        all_sprites.update()
        panahGrup.update()
        cars.update()
        batus.update()
        bensins.update()

        # Increase score
        score += 1

    screen.fill(BG)

    screen.blit(tribune_kiri, (-105, 0))
    screen.blit(tribune_kanan, (WIDTH - 40, 0))

    if scene.get(current_scene) == "MAIN MENU":
        draw_text("MAIN MENU", 40, WHITE, WIDTH // 2 - 100, HEIGHT // 4)
        draw_text("Press SPACE to Play", 30, WHITE, WIDTH // 2 - 100, HEIGHT // 2)
        draw_text("Press ESC to Exit", 30, WHITE, WIDTH // 2 - 100, HEIGHT // 2 + 50)

    if scene.get(current_scene) == "PLAY":
        panahGrup.draw(screen)
        batus.draw(screen)
        cars.draw(screen)
        bensins.draw(screen)
        all_sprites.draw(screen)

        # Draw Health Bar
        pygame.draw.rect(screen, GREEN, (10, 10, health, 20))
        pygame.draw.rect(screen, WHITE, (10, 10, 100, 20), 2)

        # Draw Score
        score_text = score_font.render("Score: " + str(score), True, WHITE)
        screen.blit(score_text, (10, 40))

    if scene.get(current_scene) == "GAME OVER":
        draw_text("GAME OVER", 40, WHITE, WIDTH // 2 - 120, HEIGHT // 4)
        draw_text("Final Score : {}".format(score), 30, WHITE, WIDTH // 2 - 100, HEIGHT // 2 + 100)
        draw_text("Press R to Restart", 30, WHITE, WIDTH // 2 - 100, HEIGHT // 2)
        draw_text("Press ESC to Exit", 30, WHITE, WIDTH // 2 - 100, HEIGHT // 2 + 50)

    pygame.display.flip()

pygame.quit()