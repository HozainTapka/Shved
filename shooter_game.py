 
from pygame import *
from random import randint
from time import time as tm 

def get_path(name_file):
    """Получает правильный путь к файлу как в EXE, так и при разработке """
    if getattr(sys, "frozen", False):
        # Режим EXE
        base_path = getattr(sys, "_MEIPASS", os.path.dirname(sys.executable))
    else: 
        base_path = os.path.dirname(os.path.abspath(__file__))

    full_path = os.path.join(base_path, name_file)


    print(f'Поиск файла: {full_path}')
    if not os.path.exists(full_path):
        print(f'Файл не найден: {full_path}')

    return full_path


#фоновая музыка
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

font.init()
font1 = font.Font(None, 50)

font_reload = font.Font(None, 33)
text_reload = font_reload.render('ПЕРЕЗАРЯДКА', True, (255, 0, 0)) 


count = 0
count_loss = 0

#font.init()
#font1 = font.Font(None, 30)
#text = font1.render('Счет:', True, (100, 200, 100))

#font.init()
#font2 = font.Font(None, 30)
#text1 = font2.render('Пропущено:', True, (100, 200, 100))


#нам нужны такие картинки:
img_back = "galaxy.jpg" #фон игры
img_hero = "rocket.png" #герой


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
        bullets.add(Bullet('bullet.png', self.rect.centerx, self.rect.centery, 20, 20, 20 ))
    
        bullet = mixer.music.load('fire.ogg')

        


class Enemy(GameSprite):
    def update(self):
        global count_loss
        global finish
        if self.rect.y + self.speed > 500:
            count_loss += 1
            if count_loss > 5:
                finish = True
            self.rect.y = 10
        else:
            self.rect.y += self.speed


class Bullet(GameSprite):
    def update(self):
        if self.rect.y < 0:
            self.kill()
        else:
            self.rect.y -= self.speed


enemy_group = sprite.Group()
for i in range(6):
    enemy_group.add(Enemy('ufo.png', randint(10,600), 15, 70, 70, 5 ))

bullets = sprite.Group()


#Создаем окошко
win_width = 700
win_height = 500
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))


#создаем спрайты
ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)

#переменная "игра закончилась": как только там True, в основном цикле перестают работать спрайты
finish = False
#Основной цикл игры:
run = True 
num_fire = 0
begin_reload_time = None # Время начала перезарядки 
#флаг сбрасывается кнопкой закрытия окна
while run:
   #событие нажатия на кнопку Закрыть
    for e in event.get():
        if e.type == QUIT:
           run = False
        if e.type == KEYDOWN:   
            if e.key == K_SPACE:
                if num_fire > 5:
                    time_now = tm()
                    if time_now - begin_reload_time > 2:
                        num_fire = 0
                else:
                    ship.fire()
                    num_fire += 1
                    if num_fire > 5:
                        begin_reload_time = tm()



    if not finish:
        #обновляем фон
        window.blit(background,(0,0))
        collides = sprite.groupcollide(enemy_group, bullets, True, True)
        for _ in collides:
            enemy_group.add(Enemy('ufo.png', randint(10,600), 15, 70, 70, 5 ))
            count += 1
            if count > 10:
                finish = True
                

            
        text = font1.render(f'Cчет: {count}', True, (100,200, 100))
        text1 = font1.render(f'Пропущенные: {count_loss}', True, (100,200, 100))
        enemy_group.update()
        enemy_group.draw(window)
        
        bullets.update()
        bullets.draw(window)   

        
        window.blit(text, (10, 20))
        
        window.blit(text1, (10, 50))


    


        #производим движения спрайтов
        ship.update()


        #обновляем их в новом местоположении при каждой итерации цикла
        ship.reset()

        if num_fire > 5:
            window.blit(text_reload, (ship.rect.centerx, ship.rect.centery))

    else:
        if count > 11:
            text_win = font1.render('ПОБЕДА', True, (0, 200, 0))
            window.blit(text_win, (300, 300))
        elif count_loss > 5:
            text_loss = font1.render('ПРОИГРЫШ', True, (255, 0, 0))
            window.blit(text_loss, (300, 300))

    display.update()
    #цикл срабатывает каждые 0.05 секунд
    time.delay(50)