from pygame import *
from random import randint

lost = 0
score = 0
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, width, height, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (width, height))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
 
class Bullet(GameSprite):

   def update(self):
       self.rect.y += self.speed

       if self.rect.y < 0:
           self.kill()


class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 65:
            self.rect.x += self.speed

    def fire(self):
       bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, -15)
       bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(60, 640)
            self.rect.y = 0
            lost += 1

class asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(60, 640)
            self.rect.y = 0

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y < 0:
            self.kill()

win_width = 700
win_height = 500
display.set_caption('Shooter')
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load('galaxy.jpg'), (win_width, win_height))

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()

ship = Player('rocket.png', 5, 430, 60, 60, 5)
finish = False
run = True

bullets = sprite.Group()
font.init()
font_1 = font.Font(None, 60)
font_2 = font.Font(None, 70)
font_3 = font.Font(None, 60)
win = font_2.render('You win!!!!!!!!!!!!!!!', True, (255, 215, 0))
lose = font_2.render('You LOSE.HAHAHAHHAHAHAHAHAHAHAHHA', True, (200, 0, 0))
retry = font_3.render('пробел - повторить', True, (150, 200, 50))

monsters = sprite.Group()
for _ in range(5):
    monster = Enemy('ufo.png', randint(60, 640), -40, 30, 30, randint(1,2))
    monsters.add(monster)

rocks = sprite.Group()
for _ in range(5):
    rock = Enemy('asteroid.png', randint(60, 640), -40, 90, 90, randint(1,2))
    rocks.add(rock)

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            ship.fire()

    if not finish:
        window.blit(background,(0, 0))
        text = font_1.render(f"Счет: {score}", 1, (15, 33, 255))
        window.blit(text, (10, 20))

        text_lose =  font_1.render(f'Пропущено: {lost}', 1, (15, 33, 255))
        window.blit(text_lose, (10, 50))

        ship.update()
        ship.reset()
        monsters.update()
        monsters.draw(window)
        rocks.update()
        rocks.draw(window)

        bullets.update()
        bullets.draw(window)

        collides = sprite.groupcollide(bullets, monsters, True, True)
        for collide in collides:
            monster = Enemy('ufo.png', randint(60, 540), -40, 30, 30, randint(1, 2))  
            monsters.add(monsters)
            score += 1     

        collides = sprite.groupcollide(bullets, rocks, True, False)
        for collide in collides:
            rock = asteroid('ufo.png', randint(60, 640), -40, 95, 95, randint(1, 2))  
            rocks.add(rocks)
            score -= 1

        if sprite.spritecollide(ship, monsters, False) or sprite.spritecollide(ship, monsters, False) or lost >= 3:
            finish = True  
            window.blit(lose, (240, 225))  
            window.blit(retry, (180, 275))

        if score >= 10:
            finish = True
            window.blit(win, (240, 225))
            window.blit(retry, (180, 275))


        display.update()
    time.delay(20)