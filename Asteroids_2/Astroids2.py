from math import fabs
import pygame
from pygame.draw import circle
from pygame.version import PygameVersion
import random
import os
from math import sin, cos
import math



class Settings:             
    window_width = 1000
    window_height = 800
    path_file = os.path.dirname(os.path.abspath(__file__))
    path_image = os.path.join(path_file, "images")
    fps = 60
    caption = "Spaceship Animationen"
    score = 0


class Background(object):       #erstellt den Hintergrund
    def __init__(self, filename="Garfield 87.png") -> None:
        super().__init__()
        self.image = pygame.image.load(os.path.join(Settings.path_image, filename)).convert()
        self.image = pygame.transform.scale(self.image, (Settings.window_width, Settings.window_height))

    def draw(self, screen):
        screen.blit(self.image, (0, 0))

class Player(pygame.sprite.Sprite):     #erstellt den Spieler
    def __init__(self) -> None:
        super().__init__()
        self.height = 40
        self.width = 40
        self.Raumschiff = "0°Ohne Schiff.png"
        self.image_original = pygame.image.load(os.path.join(Settings.path_image, self.Raumschiff))
        self.image_scaled = pygame.transform.scale(self.image_original, (40, 40))
        self.image = pygame.transform.scale(self.image_original, (self.width, self.height))
        self.color = self.image.get_at((0,0))
        self.image.set_colorkey(self.color)
        self.rect = self.image.get_rect()
        self.rect.centerx = Settings.window_width / 2
        self.rect.centery = Settings.window_height / 2
        self.grad = 0
        self.speed_h = 0
        self.speed_v = 0
  
    def update(self):
        if self.grad >= 360:
            self.grad = 0
        if self.grad <= -360:
            self.grad = 0
        if self.speed_h >= 10:
            self.speed_h = 10
        if self.speed_v >= 10:
            self.speed_v = 10
        if self.speed_h <= -10:
            self.speed_h = -10
        if self.speed_v <= -10:
            self.speed_v = -10

        if self.rect.right < 0:
            self.rect.left = Settings.window_width
        if self.rect.left > Settings.window_width:
            self.rect.right = 0
        if self.rect.bottom < 0:
            self.rect.top = Settings.window_height
        if self.rect.top > Settings.window_height:
            self.rect.bottom = 0  
        self.rect.move_ip(self.speed_h, self.speed_v)
   

    def rotate_left(self):
        self.old_center = self.rect.center
        self.grad += 22.5
        self.image = pygame.transform.rotate(self.image_scaled, self.grad)
        self.rect = self.image.get_rect()
        self.rect.center = self.old_center

    
    def rotate_right(self):
        self.old_center = self.rect.center
        self.grad -= 22.5
        self.image = pygame.transform.rotate(self.image_scaled, self.grad)
        self.rect = self.image.get_rect()
        self.rect.center = self.old_center


    def Gas(self):
        self.rechnung()
        self.speed_h = self.speed_h - sin(self.grad_rechnung)  
        self.speed_v = self.speed_v - cos(self.grad_rechnung)

    def rechnung(self):
        self.grad_rechnung = 0
        self.grad_rechnung = (math.pi/180) * self.grad
 
    def draw(self, screen): 
        screen.blit(self.image, self.rect)







class Timer(object):
    def __init__(self, duration, with_start = True):
        self.duration = duration
        if with_start:
            self.next = pygame.time.get_ticks()
        else:
            self.next = pygame.time.get_ticks() + self.duration

    def is_next_stop_reached(self):
        if pygame.time.get_ticks() > self.next:
            self.next = pygame.time.get_ticks() + self.duration
            return True
        return False

    def change_duration(self, delta=10):
        self.duration += delta
        if self.duration < 0:
            self.duration = 0

class Astroid(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image_original = pygame.image.load(os.path.join(Settings.path_image, "asteroid.png")).convert_alpha()
        self.size = 64
        self.image = pygame.transform.scale(self.image_original, (self.size, self.size))
        self.rect = self.image.get_rect()
        self.rect.centery = random.randint(80, Settings.window_height - 80)
        self.rect.centerx = random.randint(80, Settings.window_width - 80)
        self.speed_x = random.randint(-3, 3)
        self.speed_y = random.randint(-3, 3)
        
    def draw(self, screen):
        screen.blit(self.image, self.rect)
        
    def update(self):
        if self.rect.right < 0:
            self.rect.left = Settings.window_width
        if self.rect.left > Settings.window_width:
            self.rect.right = 0
        if self.rect.bottom < 0:
            self.rect.top = Settings.window_height
        if self.rect.top > Settings.window_height:
            self.rect.bottom = 0
        self.rect.move_ip(self.speed_x, self.speed_y)

        if self.rect.bottom <= 0:
            self.rect.centery += Settings.window_height
        
        if self.rect.right <= 0:
            self.rect.centerx += Settings.window_width

        if self.rect.left >= Settings.window_width:
            self.rect.centery -= Settings.window_height

        if self.rect.top >= Settings.window_height:
            self.rect.centerx -= Settings.window_height





class Schuss(pygame.sprite.Sprite):
    def __init__(self, pos_y, pos_x, player_speed_x, player_speed_y, grad) -> None:
        super().__init__()
        self.height = 20
        self.width = 20
        self.image_original = pygame.image.load(os.path.join(Settings.path_image, "beam.png"))
        self.image = pygame.transform.scale(self.image_original, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.centerx = pos_y
        self.rect.centery = pos_x
        self.grad = grad
        self.player_speed_x = player_speed_x
        self.player_speed_y = player_speed_y
        self.speed_x = 0
        self.speed_y = 0
        self.life_timer = Timer(5000, False)


    def richtung(self):
        self.grad_ = 0
        self.grad_ = (math.pi/180) * self.grad

    
    def update(self):
        self.geschwindigkeit()
        self.rect.move_ip(self.speed_x, self.speed_y)
        if self.life_timer.is_next_stop_reached():
            self.kill()

    def geschwindigkeit(self):
        self.richtung()
        self.speed_x = self.speed_x - math.sin(self.grad_)
        self.speed_y = self.speed_y - math.cos(self.grad_)                
        if self.player_speed_x > 3:
            self.speed_x = self.player_speed_x
        elif self.player_speed_y > 3:
            self.speed_y = self.player_speed_y    

    def draw(self, screen): 
        screen.blit(self.image, self.rect)


class Game(object):
    def __init__(self) -> None:
        super().__init__()
        os.environ['SDL_VIDEO_WINDOW_POS'] = "650,30"
        pygame.init()      
        pygame.display.set_caption(Settings.caption)
        self.screen = pygame.display.set_mode((Settings.window_width,Settings.window_height))
        self.clock = pygame.time.Clock()
        self.running = False
        self.players = pygame.sprite.GroupSingle()
        self.player = Player()
        self.astroids = pygame.sprite.Group()
        self.schuesse = pygame.sprite.Group() 
        self.astroid = Astroid()
        self.spawn_timer = Timer(1500)
        self.background = Background()

    def start(self):    
        self.players.add(self.player)


    def schuss(self):
        if len(self.schuesse.sprites()) < 10:
            self.schuesse.add(Schuss(self.player.rect.centerx, self.player.rect.centery,
                             self.player.speed_h, self.player.speed_v, self.player.grad))
        


    def update(self):
        self.player.update()
        self.astroids.update()
        self.schuesse.update()
        if len(self.astroids.sprites()) < 5 and self.spawn_timer.is_next_stop_reached():             
            self.astroids.add(Astroid())
           

    def draw(self):
        self.background.draw(self.screen)
        self.player.draw(self.screen)
        self.astroids.draw(self.screen)
        self.schuesse.draw(self.screen)
        pygame.display.flip()

    def collide(self):
        if pygame.sprite.groupcollide(self.astroids, self.players, False, False):
            self.running = False
            
    def run(self):
        self.running = True
        self.start()
        self.update()
        while self.running:
            self.clock.tick(Settings.fps)
            self.watch_for_events()
            self.update()
            self.draw()
            #self.collide()
        pygame.quit()

    def watch_for_events(self):  
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_UP:
                    Player.Gas(self.player)
                elif event.key == pygame.K_LEFT:
                    Player.rotate_left(self.player)
                elif event.key == pygame.K_RIGHT:
                    Player.rotate_right(self.player)
                elif event.key == pygame.K_RETURN:
                    self.schuss()

                 

          
       

if __name__ == "__main__":

    game = Game()
    game.run()
