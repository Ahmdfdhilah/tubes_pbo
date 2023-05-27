from abc import ABC, abstractmethod
import pygame
import random
import os
from pygame.locals import *
import threading

BACKGROUND_WIDTH = 800
BACKGROUND_HEIGHT = 600
FPS = 80


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
bahan_folder = os.path.join(game_folder, "Bahan")
png_folder = os.path.join(bahan_folder, "PNG")
tiles_folder = os.path.join(png_folder, "Tiles")
grass_folder = os.path.join(tiles_folder, "Grass")

def play_sound(sound_file):
    pygame.mixer.Channel(1).play(pygame.mixer.Sound(sound_file))

def play_sound_threaded(sound_file):
    sound_thread = threading.Thread(target=play_sound, args=(sound_file,))
    sound_thread.start()

def draw_text(text, font_size, font_color, x, y):
    font = pygame.font.SysFont(None, font_size)
    text_surface = font.render(text, True, font_color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((BACKGROUND_WIDTH, BACKGROUND_HEIGHT))
pygame.display.set_caption('Car Racing')
clock = pygame.time.Clock()
player_speed = 4

class GameObject(ABC, pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.hit = False
    
    @abstractmethod
    def update(self):
        pass

class Player(GameObject):
    def __init__(self, x, y, car):
        super().__init__(x, y, car)
        self.__speed = player_speed
        self.__slippery = False
        self.__slide_direction = 0
        self.__slide_counter = 0 
        self.__slide_duration = 30
    def set_slippery(self, slippery):
        self.__slippery = slippery
    def update(self):
        key = pygame.key.get_pressed()
        if not self.__slippery :
            if key[pygame.K_RIGHT] and self.rect.right < 680:
                self.rect.move_ip(self.__speed, 0)
            if key[pygame.K_LEFT] and self.rect.left > 100:
                self.rect.move_ip(-self.__speed, 0)
            if key[pygame.K_DOWN] and self.rect.bottom < BACKGROUND_HEIGHT:
                self.rect.move_ip(0, self.__speed)
            if key[pygame.K_UP] and self.rect.top > 0:
                self.rect.move_ip(0, -self.__speed)
        else:
             # Logika pergerakan player saat efek slippery aktif
            self.__slide_counter += 1
            if self.__slide_counter >= 1 and self.__slide_counter <= self.__slide_duration:
                if self.__slide_counter % 10 == 0:
                    # Setiap 10 frame, ubah arah pergerakan secara acak
                    self.__slide_direction = random.choice([-1, 1])
                self.rect.move_ip(self.__speed * self.__slide_direction, 0)
            else:
                # Menghentikan efek slippery setelah durasi tertentu
                self.__slide_counter = 0
                self.__slide_direction = 0
                self.__slippery = False
            if self.__slippery and not self.__slide_direction == 0:
                self.__speed = 2  # Mengurangi kecepatan saat efek slippery aktif
            else:
                self.__speed = player_speed
    

class Pohon(GameObject):
    def __init__(self, x, img):
        super().__init__(x, -50, img)

    def update(self):
        if self.rect.y > BACKGROUND_HEIGHT:
            self.kill()

class PanahJalan(GameObject):
    def __init__(self, x, y):
        super().__init__(x,y, image = pygame.transform.scale(pygame.image.load(os.path.join(object_folder, "arrow_white.png")).convert_alpha(), (100, 50)))

    def update(self):
        if self.rect.y > BACKGROUND_HEIGHT:
            self.kill()

class CarLeft(GameObject):
    def __init__(self, x, img):
        super().__init__(x, -250, pygame.transform.rotate(img, 180))
        
    def update(self):
        if self.rect.y > BACKGROUND_HEIGHT:
            self.kill()
        else:
            self.rect.y += random.randint(1, 3)

class CarRight(GameObject):
    def __init__(self, x, img):
        super().__init__(x, BACKGROUND_HEIGHT + 100, img)
        
    def update(self):
        if self.rect.y < -150:
            self.kill()
        else:
            self.rect.y -= random.randint(1, 3)


class Oli(GameObject):
    def __init__(self, x, img):
        super().__init__(x, -50, img)

    def update(self):
        if self.rect.y > BACKGROUND_HEIGHT:
            self.kill()

class Bensin(GameObject):
    def __init__(self, x, img):
        super().__init__(x, -50, img)

    def update(self):
        if self.rect.y > BACKGROUND_HEIGHT:
            self.kill()
current_car = 0
rumput = (pygame.image.load(os.path.join(grass_folder, "land_grass01.png")).convert_alpha())
rumput_kanan = pygame.transform.scale(rumput, (144, BACKGROUND_HEIGHT))
rumput_kiri = rumput_kanan
tribune = pygame.transform.rotate(pygame.image.load(os.path.join(object_folder, "tribune.png")).convert_alpha(), 90)
tribune_kiri = pygame.transform.scale(tribune, (144, BACKGROUND_HEIGHT))
tribune_kanan = tribune_kiri
def draw_main_menu():
       car_image = pygame.image.load(f"./Assets/Car/car_{current_car}.png").convert_alpha()
       car_rect = car_image.get_rect()
       car_rect.center = (BACKGROUND_WIDTH // 2, BACKGROUND_HEIGHT // 2 - 50)
       screen.blit(car_image, car_rect)
       draw_text("Press SPACE to Play", 30, WHITE, BACKGROUND_WIDTH // 2, BACKGROUND_HEIGHT // 2 + 200)
       draw_text("Press ESC to Exit", 30, WHITE, BACKGROUND_WIDTH // 2, BACKGROUND_HEIGHT // 2 + 250)
       selected_car_text = urutan_mobil[current_car]
       draw_text("<-  "+selected_car_text+"  ->", 30, WHITE, BACKGROUND_WIDTH // 2, BACKGROUND_HEIGHT // 2 + 150)

car_list = []
car_list_img = []
for i in range(8):
    img = pygame.image.load(os.path.join(car_folder, "car_{}.png".format(i))).convert_alpha()
    car_list.append(img)
    car_list_img.append(f"car_{i}.png")

def generate_pohon():
    x_positions = [-20, 708]
    for x in x_positions:
        if random.random() < 0.5:
            img = pygame.image.load(os.path.join(object_folder, "tree_small.png")).convert_alpha()
            pohon = Pohon(x, img)
            pohons.add(pohon)

oli_list = pygame.image.load(os.path.join(object_folder, "oil.png")).convert_alpha()
pohon_list = pygame.image.load(os.path.join(object_folder, "tree_small.png")).convert_alpha()
bensin_img = pygame.image.load(os.path.join(object_folder, "last.png")).convert_alpha()

all_sprites = pygame.sprite.Group()
panahGrup = pygame.sprite.Group()
carsLeft = pygame.sprite.Group()
carsRight = pygame.sprite.Group()
oils = pygame.sprite.Group()
bensins = pygame.sprite.Group()
pohons = pygame.sprite.Group()

objOli = Oli(random.randrange(100, 600), oli_list)
oils.add(objOli)
  
generate_pohon()

mobilLeft = CarLeft(random.randrange(100, 300), random.choice(car_list))
carsLeft.add(mobilLeft)
mobilRight = CarRight(random.randrange(310, 600), random.choice(car_list))
carsRight.add(mobilRight)

for i in range(3):
    panah = PanahJalan(BACKGROUND_WIDTH//2 -50, i * 230 + 40)
    panahGrup.add(panah)


urutan_mobil = ["Honda Jazz", "Rubicon", "Civic", "Taxi", "Camri", "SLK100", "Supra GTR"]

# Health Bar
health = 100
#speed increment
speed_increment = 1
# Score
score = 0
score_font = pygame.font.SysFont(None, 30)
run = True
scene = {
    0: "MAIN MENU",
    1: "PLAY",
    2: "GAME OVER",
}

player_car = pygame.image.load(os.path.join(car_folder, f"car_{current_car}.png")).convert_alpha()
player = Player(BACKGROUND_WIDTH // 2 - 30, BACKGROUND_HEIGHT/2-50, player_car)
all_sprites.add(player)
current_scene = 0
pygame.mixer.music.load("sound/backsound.mp3")  # Load file musik
pygame.mixer.music.set_volume(0.4)
pygame.mixer.music.play(-1)

while run:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == KEYUP:
            if event.key == K_r and current_scene == 2:
                all_sprites.empty()
                panahGrup.empty()
                carsLeft.empty()
                carsRight.empty()
                oils.empty()
                bensins.empty()
                pohons.empty()

                objOli = Oli(random.randrange(100, 600), oli_list)
                oils.add(objOli)
                
                generate_pohon()

                mobilLeft = CarLeft(random.randrange(100, 300), random.choice(car_list))
                carsLeft.add(mobilLeft)
                mobilRight = CarRight(random.randrange(310, 600), random.choice(car_list))
                carsRight.add(mobilRight)

                for i in range(3):
                    panah = PanahJalan(BACKGROUND_WIDTH//2 -50, i * 230 + 40)
                    panahGrup.add(panah)

                player_car = pygame.image.load(os.path.join(car_folder, f"car_{current_car}.png")).convert_alpha()
                player = Player(BACKGROUND_WIDTH // 2 - 30, BACKGROUND_HEIGHT/2-50, player_car)

                all_sprites.add(player)
                # Reset health
                health = 100

                # Reset score
                score = 0

                current_scene = 1

        if event.type == KEYDOWN:
            if scene.get(current_scene) == "MAIN MENU":
                if event.key == K_RIGHT:
                    current_car = (current_car + 1) % len(urutan_mobil)
                elif event.key == K_LEFT:
                    current_car = (current_car - 1) % len(urutan_mobil)
                player.image = pygame.image.load(os.path.join(car_folder, f"car_{current_car}.png")).convert_alpha()    
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
        for pohon in pohons:
            pohon.rect.y += 2
        for car in carsLeft:
            car.rect.y += 3
        for car in carsRight:
            car.rect.y -= 3
        for oli in oils:
            oli.rect.y += 2
        for bensin in bensins:
            bensin.rect.y += 2
        while len(panahGrup) < 3:
            panah_new = PanahJalan(BACKGROUND_WIDTH // 2 - 50, -50)
            panahGrup.add(panah_new)
        while len(pohons) < 1:
            generate_pohon()
        while len(carsLeft) < 1:
            mobil_new = CarLeft(random.randrange(100, 300), random.choice(car_list))
            carsLeft.add(mobil_new)
        while len(carsRight) < 1: 
            mobil_new = CarRight(random.randrange(310, 600), random.choice(car_list))
            carsRight.add(mobil_new)
        while len(oils) < 1:
            oli_new = Oli(random.randrange(100, 600), oli_list)
            oils.add(oli_new)
        while len(bensins) < 1:
            bensin_new = Bensin(random.randrange(100, 600), bensin_img)
            bensins.add(bensin_new)
        # Check Collision
        kena_mobil_kiri = pygame.sprite.spritecollide(player, carsLeft, True)
        kena_mobil_kanan = pygame.sprite.spritecollide(player, carsRight, True)
        if kena_mobil_kiri:
            for m in kena_mobil_kiri:
                if not m.hit:
                    m.hit = True
                    health = 0
                    if health <= 0:
                        current_scene = 2
            play_sound_threaded("sound/Duar.mp3")
        if kena_mobil_kanan:
            for m in kena_mobil_kanan:
                if not m.hit:
                    m.hit = True
                    health = 0
                    if health <= 0:
                        current_scene = 2
            play_sound_threaded("sound/Duar.mp3") 
        kena_oli = pygame.sprite.spritecollide(player, oils, True)
        if kena_oli:
            for objOli in kena_oli:
                if not objOli.hit:
                    objOli.hit = True
                    health -= 5
                    if health <= 0:
                        current_scene = 2
            player.set_slippery(True)
            play_sound_threaded("sound/ngepot.mp3")

        kena_bensin = pygame.sprite.spritecollide(player, bensins, True)
        if kena_bensin:
            for bensin in kena_bensin:
                if not bensin.hit:
                    bensin.hit = True
                    health += 5
                    if health > 100:
                        health = 100
        
        all_sprites.update()
        panahGrup.update()
        carsLeft.update()
        carsRight.update()
        oils.update()
        bensins.update()
        pohons.update()

        # Increase score
        score += 0.1
        score = round(score,2)
        if score == 100 or score == 200 or score == 300 or score == 400:
            player_speed += speed_increment
    screen.fill(BG)

    screen.blit(tribune_kiri, (-40, 0))
    screen.blit(tribune_kanan, (BACKGROUND_WIDTH - 120, 0))
    screen.blit(rumput_kiri, (-90, 0))
    screen.blit(rumput_kanan, (BACKGROUND_WIDTH - 60, 0))


    if scene.get(current_scene) == "MAIN MENU":
       draw_main_menu()
    if scene.get(current_scene) == "PLAY": 
        panahGrup.draw(screen)
        oils.draw(screen)
        carsLeft.draw(screen)
        carsRight.draw(screen)
        bensins.draw(screen)
        pohons.draw(screen)
        all_sprites.draw(screen)

        # Draw Health Bar
        pygame.draw.rect(screen, GREEN, (10, 10, health, 20))
        pygame.draw.rect(screen, WHITE, (10, 10, 100, 20), 2)

        # Draw Score
        score_text = score_font.render("Score: " + str(score), True, WHITE)
        screen.blit(score_text, (10, 40))

    if scene.get(current_scene) == "GAME OVER":
        draw_text("GAME OVER", 40, WHITE, BACKGROUND_WIDTH // 2 - 120, BACKGROUND_HEIGHT // 4)
        draw_text("Final Score : {}".format(score), 30, WHITE, BACKGROUND_WIDTH // 2 - 100, BACKGROUND_HEIGHT // 2 + 100)
        draw_text("Press R to Restart", 30, WHITE, BACKGROUND_WIDTH // 2 - 100, BACKGROUND_HEIGHT // 2)
        draw_text("Press ESC to Exit", 30, WHITE, BACKGROUND_WIDTH // 2 - 100, BACKGROUND_HEIGHT // 2 + 50)

    pygame.display.flip()

pygame.mixer.music.stop() 
pygame.quit()