# Imports
import pygame
import random
import sys
import os

if getattr(sys, 'frozen', False):
    current_path = sys._MEIPASS
else:
    current_path = os.path.dirname(__file__)

# Initialize game engine
pygame.init()


# Window
WIDTH = 1600
HEIGHT = 960
SIZE = (WIDTH, HEIGHT)
TITLE = "imperial assault"
screen = pygame.display.set_mode(SIZE, pygame.FULLSCREEN)
pygame.display.set_caption(TITLE)


# Timer
clock = pygame.time.Clock()
refresh_rate = 60


# Colors
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
LIGHT_GREEN = (100, 255, 100)
GREEN = (0, 255, 0)


# Fonts
FONT_SM = pygame.font.Font(current_path + "/assets/fonts/spacerangerboldital.ttf", 24)
FONT_MD = pygame.font.Font(current_path + "/assets/fonts/spacerangerboldital.ttf", 32)
FONT_LG = pygame.font.Font(current_path + "/assets/fonts/spacerangerboldital.ttf", 64)
FONT_XL = pygame.font.Font(current_path + "/assets/fonts/spacerangerboldital.ttf", 96)


# Images
'''ships'''
ship_img = pygame.image.load(current_path + '/assets/images/x-wing.png').convert_alpha()
enemy_img_left = pygame.image.load(current_path + '/assets/images/tieFighterLeft.png').convert_alpha()
enemy_img_right = pygame.image.load(current_path + '/assets/images/tieFighterRight.png').convert_alpha()
'''shooting stuff'''
laser_img = pygame.image.load(current_path + '/assets/images/laserRed.png').convert_alpha()
bomb_img = pygame.image.load(current_path + '/assets/images/enemyLaserGreen.png').convert_alpha()

'''bonuses'''
death_star_img = pygame.image.load(current_path + '/assets/images/death_star.png').convert_alpha()
powerup_img = pygame.image.load(current_path + '/assets/images/laserGreenShot.png').convert_alpha()

'''planets'''
planet_img1 = pygame.image.load(current_path + '/assets/images/Earth.png').convert_alpha()
planet_img2 = pygame.image.load(current_path + '/assets/images/Mustafar.png').convert_alpha()
planet_img3 = pygame.image.load(current_path + '/assets/images/Hoth.png').convert_alpha()
planet_img4 = pygame.image.load(current_path + '/assets/images/tatooine.png').convert_alpha()
planet_img5 = pygame.image.load(current_path + '/assets/images/kamino.png').convert_alpha()
planet_img6 = pygame.image.load(current_path + '/assets/images/asteroid.png').convert_alpha()


# Sounds
laser_sound = pygame.mixer.Sound(current_path + "/assets/sounds/laser.ogg")
DEATH = pygame.mixer.Sound(current_path + "/assets/sounds/WilhelmScream.ogg")
EXPLOSION = pygame.mixer.Sound(current_path + '/assets/sounds/explosion.ogg')

# music
battle_theme = (current_path + "/assets/sounds/duel_of_fates.ogg")
main_theme = (current_path + "/assets/sounds/starwars_theme.ogg")
victory_music = (current_path + "/assets/sounds/rebel_theme.ogg")
defeat_music = (current_path + "/assets/sounds/imperial_march.ogg")

# Stages
START = 0
PLAYING = 1
END = 2

# create stars
stars = []

for i in range(100):
    x = random.randrange(0, WIDTH)
    y = random.randrange(0, HEIGHT)
    r = random.randrange(1, 5)
    s = [x, y, r, r]
    stars.append(s)

# variables
score = 0
max_mobs = 13

# Game classes
class Ship(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()

        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = image.get_rect()
        self.max_health = 3
        self.health = self.max_health
        self.double_shot = False
        self.hits = 0
        self.speed = 5

    def move_left(self):
        self.rect.x -= self.speed
    
    def move_right(self):
        self.rect.x += self.speed

    def shoot(self):
        print("PEW!")
        laser_sound.play()

        if self.double_shot:
            laser1 = Laser(laser_img)
            laser1.rect.x = self.rect.left
            laser1.rect.centery = self.rect.centery

            laser2 = Laser(laser_img)
            laser2.rect.right = self.rect.right
            laser2.rect.centery = self.rect.centery
            
            lasers.add(laser1, laser2)
        else:    
            laser1 = Laser(laser_img)
            laser1.rect.centerx = self.rect.centerx
            laser1.rect.centery = self.rect.y

            lasers.add(laser1)

    def check_powerups(self):
        hit_list = pygame.sprite.spritecollide(self, powerups, True,
                                               pygame.sprite.collide_mask)
        
        for hit in hit_list:
            hit.apply(self)

    def check_health(self):
        hit_list = pygame.sprite.spritecollide(self, bombs, True,
                                               pygame.sprite.collide_mask)
        
        hit_list2 = pygame.sprite.spritecollide(self, mobs, True,
                                               pygame.sprite.collide_mask)

        if len(hit_list2) > 0:
            self.kill()

        for h in hit_list:
            self.health -= 1
            self.double_shot = False
        
        if self.health == 0:
            print("Boom!")
            DEATH.play()
            self.kill()

    def update(self):
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > WIDTH:
            self.rect.right = WIDTH

        self.check_powerups()
        self.check_health()
        
class Laser(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()

        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = image.get_rect()
        self.speed = 10

    def update(self):
        self.rect.y -= self.speed

        if self.rect.bottom < 0:
            self.kill()

        
        hit_list = pygame.sprite.spritecollide(self, bombs, True,
                                               pygame.sprite.collide_mask)

        if len(hit_list) > 0:
            self.kill()
        

class Mob(pygame.sprite.Sprite):
    def __init__(self, x, y, image, value):
        super().__init__()

        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.max_health = value
        self.health = value
        self.value = value * 50

    def drop_bomb(self):
        print("Bwwamp!")
        laser_sound.play()
        
        bomb = Bomb(bomb_img)
        bomb.rect.centerx = self.rect.centerx
        bomb.rect.y = self.rect.bottom - 25
        bombs.add(bomb)

    def update(self):
        hit_list = pygame.sprite.spritecollide(self, lasers, True,
                                               pygame.sprite.collide_mask)

        for h in hit_list:
            self.health -= 1
            ship.hits += 1

        if self.health <= 0:
            print("Boom!")
            EXPLOSION.play()
            player.score += self.value
            self.kill()

class Bomb(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()

        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = image.get_rect()
        self.speed = 12

    def update(self):
        self.rect.y += self.speed

        if self.rect.top > HEIGHT:
            self.kill()

class LaserPowerUp(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()

        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 5

    def apply(self, ship):
        ship.double_shot = True

    def update(self):
        self.rect.y += self.speed

        if self.rect.top > HEIGHT:
            self.rect.y = -3000
            self.rect.x = random.randrange(10, WIDTH - 50)

class BonusTarget(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()

        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 2

    def apply(self):
        player.score += 500

    def update(self):
        self.rect.x += self.speed

        if self.rect.left > WIDTH:
            self.rect.x = -1000

        hit_list2 = pygame.sprite.spritecollide(self, lasers, True,
                                               pygame.sprite.collide_mask)

        if len(hit_list2) > 0:
            self.apply()
            EXPLOSION.play()
            self.kill()

class Fleet():
    def __init__(self, mobs):
        self.mobs = mobs
        self.speed = 3
        self.drop_speed = 25
        self.bomb_rate = 25
        self.moving_right = True

    def move(self):
        hits_edge = False

        for m in mobs:
            if self.moving_right:
                m.rect.x += self.speed
                m.image = enemy_img_right

                if m.rect.right >= WIDTH:
                    hits_edge = True
            else:
                m.rect.x -= self.speed
                m.image = enemy_img_left

                if m.rect.left <= 0:
                    hits_edge = True
                    
        if hits_edge:
            self.reverse()
            self.move_down()

    def reverse(self):
        self.moving_right = not self.moving_right

    def move_down(self):
        for m in mobs:
            if m.rect.bottom < HEIGHT:
                m.rect.y += self.drop_speed

    def choose_bomber(self):
        rand = random.randrange(self.bomb_rate)
        mob_list = mobs.sprites()

        if len(mob_list) > 0 and rand == 0:
            bomber = random.choice(mob_list)
            bomber.drop_bomb()
    
    def update(self):
        self.move()
        self.choose_bomber()

class Planet(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pick_planet()
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, WIDTH)
        self.rect.y = random.randrange(-HEIGHT*2, HEIGHT/2)
        
    def update(self):
        if self.rect.top > HEIGHT:
            self.image = pick_planet()
            self.rect.y = random.randrange(-HEIGHT*2, -200)
            self.rect.x = random.randrange(0, WIDTH)

    

# Game helper functions
def show_title_screen():
    screen.fill(BLACK)
    title_text = FONT_XL.render(TITLE + "!", 1, WHITE)
    w = title_text.get_width()
    screen.blit(title_text, [WIDTH/2 - w/2, 325])
    start_text = FONT_MD.render("Press Space to Start" + "!", 1, WHITE)
    w = start_text.get_width()
    screen.blit(start_text, [WIDTH/2 - w/2, 500])

def show_end_screen(winner, winner_img):
    screen.fill(BLACK)

    w = winner_img.get_width()
    screen.blit(winner_img, [ WIDTH/2 - w/2, 75])
    
    end_text = FONT_XL.render(winner + "!", 1, WHITE)
    w = end_text.get_width()
    h = end_text.get_height()
    screen.blit(end_text, [WIDTH/2 - w/2, 275])
    
    restart_text = FONT_MD.render("'R' to Restart", 1, LIGHT_GREEN)
    w = restart_text.get_width()
    h = restart_text.get_height()
    screen.blit(restart_text, [WIDTH/2 - w/2, 450])

def draw_background():
    screen.fill(BLACK)
    
    for s in stars:
        pygame.draw.ellipse(screen, WHITE, s)

    for s in stars:
        s[1] += 0.8
        if s[1] > HEIGHT:
            s[1] = -10

    planets.draw(screen)

    for p in planets:
        p.rect.y += 1

def draw_healthbar(player):
    height_ratio = 0.05
    ratio = player.health / player.max_health

    if ratio > .67:
        color = GREEN
    elif ratio > .34:
        color = YELLOW
    else:
        color = RED

    bar_length = ratio * (player.rect.width - 10)
    height = height_ratio *  player.rect.height

    pygame.draw.rect(screen, WHITE, [player.rect.x + 5, player.rect.bottom + 5, player.rect.width - 10, height])
    pygame.draw.rect(screen, color, [player.rect.x + 5, player.rect.bottom + 5, bar_length, height])

def set_music(song):
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(-1)

def pick_planet():
    choice = random.randrange(0, 6)

    if choice == 1:
        planet_img = planet_img1
    elif choice == 2:
        planet_img = planet_img2
    elif choice == 3:
        planet_img = planet_img3
    elif choice == 4:
        planet_img = planet_img4
    elif choice == 5:
        planet_img = planet_img5
    else:
        planet_img = planet_img6

    return planet_img


def setup():
    global stage, done
    global player, ship, lasers, mobs, fleet, bombs, powerups, bonuses, planets
    global shots
    
    ''' Make game objects '''
    ship = Ship(ship_img)
    ship.rect.centerx = WIDTH/2
    ship.rect.bottom = HEIGHT - 20
    
    mob1 = Mob(100, 200, enemy_img_right, 3)
    mob2 = Mob(300, 200, enemy_img_right, 3)
    mob3 = Mob(500, 200, enemy_img_right, 3)
    mob4 = Mob(700, 200, enemy_img_right, 3)
    mob5 = Mob(900, 200, enemy_img_right, 3)
    mob6 = Mob(1100, 200, enemy_img_right, 3)
    mob7 = Mob(1300, 200, enemy_img_right, 3)
    mob8 = Mob(200, 100, enemy_img_right, 5)
    mob9 = Mob(400, 100, enemy_img_right, 5)
    mob10 = Mob(600, 100, enemy_img_right, 5)
    mob11 = Mob(800, 100, enemy_img_right, 5)
    mob12 = Mob(1000, 100, enemy_img_right, 5)
    mob13 = Mob(1200, 100, enemy_img_right, 5)
    
    planet1 = Planet()
    planet2 = Planet()
    planet3 = Planet()

    powerup1 = LaserPowerUp(random.randrange(100, WIDTH-100), -2000, powerup_img)

    bonus1 = BonusTarget(-1500, 50, death_star_img)

    ''' Make sprite groups '''
    player = pygame.sprite.GroupSingle()
    player.add(ship)
    player.score = 0

    lasers = pygame.sprite.Group()
    bombs = pygame.sprite.Group()

    mobs = pygame.sprite.Group()
    mobs.add(mob1, mob2, mob3, mob4, mob5, mob6, mob7,
             mob8, mob9, mob10, mob11, mob12, mob13)

    planets = pygame.sprite.Group()
    planets.add(planet1, planet2, planet3)
    

    powerups = pygame.sprite.Group()
    powerups.add(powerup1)

    fleet = Fleet(mobs)

    bonuses = pygame.sprite.Group()
    bonuses.add(bonus1)

    ''' score and shots '''
    shots = 0
    player.hits = 0
    
    ''' set stage '''
    stage = START
    done = False

    ''' set music '''
    set_music(main_theme)

def show_statscreen():
    stats_text = FONT_LG.render("STATS", 1, YELLOW)
    w = stats_text.get_width()
    screen.blit(stats_text, [WIDTH/2 - w/2, 650])
    
    accu_text = FONT_MD.render("Accuracy: " + str(accuracy) + "%", 1, YELLOW)
    w = accu_text.get_width()
    screen.blit(accu_text, [WIDTH/2 - w/2, 800])
    
    score_text = FONT_MD.render("Score: " + str(player.score), 1, YELLOW)
    w = score_text.get_width()
    screen.blit(score_text, [WIDTH/2 - w/2, 750])

def display_stats():
    score_title_text = FONT_MD.render("Score", 1, WHITE)    
    score_text = FONT_MD.render(str(player.score), 1, WHITE)
    screen.blit(score_title_text, [45, 20])
    screen.blit(score_text, [45, 50])
        
# Game loop
setup()

while not done:
    # Input handling (React to key presses, mouse clicks, etc.)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                done = True
            if stage == START:
                if event.key == pygame.K_SPACE:
                    stage = PLAYING
                    set_music(battle_theme)
            elif stage == PLAYING:
                if event.key == pygame.K_SPACE:
                    ship.shoot()
                    shots += 1
                if event.key == pygame.K_r:
                    setup()
            elif stage == END:
                if event.key == pygame.K_r:
                    setup()

    pressed = pygame.key.get_pressed()    
    
    # Game logic (Check for collisions, update points, etc.)
    if stage == PLAYING:
        if pressed[pygame.K_LEFT]:
            ship.move_left()
        elif pressed[pygame.K_RIGHT]:
            ship.move_right()

        player.update()
        lasers.update()
        bombs.update()
        fleet.update()
        mobs.update()
        powerups.update()
        bonuses.update()
        planets.update()

    score = ((13 - len(mobs))* 200)

    hits = ship.hits

    if shots > 0 and hits > 0:
        accuracy = (hits/shots) * 100
        accuracy = accuracy // 1
    else:
        accuracy = 0

    if len(player) <= 0:
        if stage != END:
            stage = END
            winner = "The Empire has invaded"
            winner_img = pygame.image.load(current_path + '/assets/images/death_star.png').convert_alpha()
            score -= 1000
            set_music(defeat_music)
    elif len(mobs) <= 0:
        if stage!= END:
            stage = END
            winner = "You Stopped the Empire"
            winner_img = pygame.image.load(current_path + '/assets/images/x-wing.png').convert_alpha()
            player.score += (ship.health * 50)
            set_music(victory_music)
            
            if accuracy > 50:
                player.score += 500
                if accuracy > 75:
                    player.score += 500
    else:
        for m in mobs:
            if m.rect.bottom >= HEIGHT:
                stage = END
                winner = "The Empire has invaded"
                winner_img = pygame.image.load(current_path + '/assets/images/death_star.png').convert_alpha()
                set_music(defeat_music)
    
    
        
    # Drawing code (Describe the picture. It isn't actually drawn yet.)
    draw_background()
    lasers.draw(screen)
    bombs.draw(screen)
    player.draw(screen)
    draw_healthbar(ship)
    powerups.draw(screen)
    bonuses.draw(screen)
    for mob in mobs:
        draw_healthbar(mob)
    mobs.draw(screen)
    display_stats()

    if stage == START:
        show_title_screen()
    if stage == END:
        show_end_screen(winner, winner_img)
        show_statscreen()

        
    # Update screen (Actually draw the picture in the window.)
    pygame.display.flip()


    # Limit refresh rate of game loop 
    clock.tick(refresh_rate)


# Close window and quit
pygame.quit()
