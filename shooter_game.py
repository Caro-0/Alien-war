from pygame import *
from random import randint
from time import time as timer
 
#фоновая музыка
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')
 
#шрифты и надписи
font.init()
font1 = font.Font(None, 80)
win = font1.render('YOU WIN!', True, (255, 255, 255))
lose = font1.render('YOU LOSE!', True, (180, 0, 0))
font2 = font.Font(None, 36)
 
#нам нужны такие картинки:
img_back = "Space-780x437.jpg" #фон игры
img_hero = "battleship.png" #герой
img_bullet = "bullet1.png" #пуля
img_enemy = "ufo.png" #враг
img_asteroid = "asteroid.png" #Астероид


score = 0 #сбито кораблей
lost = 0 #пропущено кораблей
max_lost = 3 #проиграли, если пропустили столько
HP = 3 

clip = 5
is_cooldown = False
timer_cooldown = 0

#класс-родитель для других спрайтов
class GameSprite(sprite.Sprite):
 #конструктор класса
   def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
       #Вызываем конструктор класса (Sprite):
       sprite.Sprite.__init__(self)
 
       #каждый спрайт должен хранить свойство image - изображение
       self.image = transform.scale(image.load(player_image), (size_x, size_y))
       self.speed = player_speed
 
       #каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
       self.rect = self.image.get_rect()
       self.rect.x = player_x
       self.rect.y = player_y
 #метод, отрисовывающий героя на окне
   def reset(self):
       window.blit(self.image, (self.rect.x, self.rect.y))
 
#класс главного игрока
class Player(GameSprite):
   #метод для управления спрайтом стрелками клавиатуры
   def update(self):
       keys = key.get_pressed()
       if keys[K_LEFT] and self.rect.x > 5:
           self.rect.x -= self.speed
       if keys[K_RIGHT] and self.rect.x < win_width - 80:
           self.rect.x += self.speed
 #метод "выстрел" (используем место игрока, чтобы создать там пулю)
   def fire(self):
       global clip
       global is_cooldown
       global timer_cooldown
       if not is_cooldown:
           bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
           bullets.add(bullet)
           clip -= 1
           if clip == 0:
               is_cooldown = True
               timer_cooldown    = timer()

 
#класс спрайта-врага  
class Enemy(GameSprite):
   #движение врага
   def update(self):
       self.rect.y += self.speed
       global lost
       #исчезает, если дойдет до края экрана
       if self.rect.y > win_height:
           self.rect.x = randint(80, win_width - 80)
           self.rect.y = 0
           lost = lost + 1
 
#класс спрайта-пули  
class Bullet(GameSprite):
   #движение врага
   def update(self):
       self.rect.y += self.speed
       #исчезает, если дойдет до края экрана
       if self.rect.y < 0:
           self.kill()
 
#класс астеройдов
class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed
        #исчезает, если дойдет до края экрана
        if self.rect.y > win_height:
           self.rect.x = randint(80, win_width - 80)
           self.rect.y = 0




#Создаем окошко
win_width = 700
win_height = 500
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))
 
#создаем спрайты
ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)
 
monsters = sprite.Group()
for i in range(1, 6):
   monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
   monsters.add(monster)
 
bullets = sprite.Group()

# Создание астреидов
asteroids = sprite.Group()
for i in range(3):
    asteroid = Asteroid(img_asteroid,randint(80, win_width - 80), -40, 80, 50, randint(1, 5) )
    asteroids.add(asteroid)
 
#переменная "игра закончилась": как только там True, в основном цикле перестают работать спрайты
finish = False
#Основной цикл игры:
run = True #флаг сбрасывается кнопкой закрытия окна
while run:
   #событие нажатия на кнопку Закрыть
   for e in event.get():
       if e.type == QUIT:
           run = False
       #событие нажатия на пробел - спрайт стреляет
       elif e.type == KEYDOWN:
           if e.key == K_SPACE:
               fire_sound.play()
               ship.fire()
 
   if not finish:
       #обновляем фон
       window.blit(background,(0,0))
 

       #производим движения спрайтов
       ship.update()
       monsters.update()
       bullets.update()
       asteroids.update()

       sprite_list = sprite.groupcollide(monsters, bullets, False, True)
       for enem in sprite_list:
           enem.rect.x = randint(80, win_width - 80)
           enem.rect.y = 0

           score += 1

       #пишем текст на экране
       text = font2.render("Счет: " + str(score), 1, (255, 255, 255))
       window.blit(text, (10, 20))
 
       text_lose = font2.render("Пропущено: " + str(lost), 1, (255, 255, 255))
       window.blit(text_lose, (10, 50))
 

       # Проверка завершения перезарядки
       if is_cooldown:
           if timer() - timer_cooldown >= 3:
               is_cooldown = False
               clip = 5

       # Проверка на завершение игры
       if score >= 20:
           finish = True
           window.blit(win, [200, 200])
       
       if lost >= 3 or sprite.spritecollide(ship, monsters, False):
           finish = True
           window.blit(lose, [200, 200])

       if sprite.spritecollide(ship, asteroids, False):
           asteroid = spritecollide(ship, asteroids, False)[0]
           asteroid.rect.x = randint(80, win_width - 80)
           asteroid.rect.y = 0
           HP -= 1
           if HP == 0:
               finish = True
               window.blit(lose, [200, 200])

 
       #обновляем их в новом местоположении при каждой итерации цикла
       ship.reset()
       monsters.draw(window)
       bullets.draw(window)
       asteroids.draw(window)
       display.update()
   #цикл срабатывает каждую 0.05 секунд
   time.delay(50)
