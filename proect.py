#импорты и всякое важное
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import QUrl
from ui import Ui_MainWindow
import pygame
from socket import*
from threading import* 
import pygame.sprite
client = socket(AF_INET,SOCK_STREAM)
client.connect(("localhost",2010))
pygame.init()
win_width = 1200
win_height = 700
with open("lvl1.txt","r",) as file:
    level1 = file.readlines()
    clock = pygame.time.Clock()
#клас
class GameSprite(pygame.sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load(player_image), (size_x, size_y))
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
class Wall(pygame.sprite.Sprite):
    def __init__(self,wall_width,wall_height,wall_x,wall_y):
        super().__init__()
        self.width = wall_width
        self.height = wall_height
        self.image = pygame.Surface((self.width,self.height))
        self.image.fill((255, 69, 0))
        self.rect = self.image.get_rect()
        self.rect.x = wall_x
        self.rect.y = wall_y
    def draw_wall(self):
        window.blit(self.image,(self.rect.x,self.rect.y))
class Player(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_x_speed,player_y_speed):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.x_speed = player_x_speed
        self.y_speed = player_y_speed
        self.direction = "right"
    def update(self, barriers):
        if self.rect.x <= win_width-80 and self.x_speed > 0 or self.rect.x >= 0 and self.x_speed < 0:
            self.rect.x += self.x_speed
        platforms_touched = pygame.sprite.spritecollide(self, barriers, False)
        if self.x_speed > 0:
            for p in platforms_touched:
                self.rect.right = min(self.rect.right, p.rect.left) 
        elif self.x_speed < 0:
            for p in platforms_touched:
                self.rect.left = max(self.rect.left, p.rect.right)
        
        if self.rect.y <= win_height-80 and self.y_speed > 0 or self.rect.y >= 0 and self.y_speed < 0:
            self.rect.y += self.y_speed
        platforms_touched = pygame.sprite.spritecollide(self, barriers, False)
        if self.y_speed > 0:
            for p in platforms_touched:
                self.rect.bottom = min(self.rect.bottom, p.rect.top) 
        elif self.y_speed < 0:
            for p in platforms_touched:
                self.rect.top = max(self.rect.top, p.rect.bottom)
class Widget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Створюємо медіаплеєр
        self.media = QMediaPlayer(self)

        # Використовуємо існуючий QVideoWidget з UI
        self.media.setVideoOutput(self.ui.widget)  # відео-віджет

        # Ставимо відео на задній план
        self.ui.widget.lower()  # відео під усі кнопки/написи

        # Завантажуємо відео
        self.media.setMedia(QMediaContent(QUrl.fromLocalFile('fon.mp4')))

        # Зациклення
        self.media.mediaStatusChanged.connect(self.loop_video)

        # Запускаємо
        self.media.play()

    def loop_video(self, status):
        if status == QMediaPlayer.EndOfMedia:
            self.media.setPosition(0)
            self.media.play()
prinyat_sms = client.recv(1024).decode()
prinyat_sms=prinyat_sms.split(",")
# print(int(prinyat_sms[0]),int(prinyat_sms[1]),int(prinyat_sms[2]),int(prinyat_sms[3]))
my_id = int(prinyat_sms[0])
my_x = int(prinyat_sms[1])
my_y = int(prinyat_sms[2])
my_rad = int(prinyat_sms[3])
global vragi
vragi = []
def obmen():
    
    while 1:
        global vragi
        try:
            
            danni = client.recv(1024).decode()
            danni = danni.strip("|").split("|")
            vragi = []
            for eneme in danni:
                danni2 = eneme.split(",")
                danni2 = list(map(int,danni2[:4]))# берем все кроме имени
                vragi.append(danni2)
                
        except:
            pass
Thread(target=obmen).start()
#чтото нужное
stenki = pygame.sprite.Group()
hero = Player('orange.png', 5, win_height - 130, 80, 80, 0, 0)
pol = Wall(1200,50,0,650)
platforma = Wall(50,50,700,500)
platforma2 = Wall(50,50,800,400)
stenki.add(pol)
stenki.add(platforma)
stenki.add(platforma2)
key = GameSprite("key.png",932,299,20,20)
lvl = "lvl1"
jump = False
gravity = False
finish = False
game = False
barriers = pygame.sprite.Group()
app = QApplication([])
ex = Widget()
def poka():
    ex.destroy()
def nachalo():
    global game
    ex.hide()
    game = True
    ex.close()
    app.quit()
ex.ui.STARt.clicked.connect(nachalo)
ex.ui.pushButton_2.clicked.connect(poka)
ex.show()
app.exec_()
#конец
if game == True:
    window = pygame.display.set_mode((win_width, win_height))
    run = True
    while run:
        window.fill((255, 255, 255))
        if lvl == "lvl1":
                
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    run = False
                elif e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_LEFT:
                        hero.x_speed = -4
                    if e.key == pygame.K_RIGHT:
                        hero.x_speed = 4
                    if e.key == pygame.K_SPACE:
                        jump = True


                elif e.type == pygame.KEYUP:
                    if e.key == pygame.K_LEFT:
                        hero.x_speed = 0
                    if e.key == pygame.K_RIGHT:
                        hero.x_speed = 0 
                    # if e.key == pygame.K_SPACE:
                    #     jump = False
            if not finish:
                hero.update(barriers)
                if pygame.sprite.spritecollide(
                    hero,stenki,False
                ):
                    gravity = False
                else:
                    gravity = True
                if gravity == True:
                    hero.rect.y+=2
                if jump == True and pygame.sprite.spritecollide(hero,stenki,False):
                    for i in range(45):
                        hero.rect.y-=3
                    jump = False
                try:
                    msg = f"{my_id},{hero.rect.x},{hero.rect.y},80"  # id, x, y, radius
                    client.send(msg.encode())
                except:
                    pass

                hero.reset()
                stenki.draw(window)
                # pol.draw_wall()
                # platforma.draw_wall()
                # platforma2.draw_wall()
                key.reset()
                for enemy in vragi:
                    id_, x, y, r = enemy  # id, x, y, radius
                    if id_ != my_id:  # не малюємо себе
                        img = pygame.transform.scale(pygame.image.load("hero.png"), (r, r))
                        window.blit(img, (x, y))


        pygame.display.update()
        clock.tick(60)   # FPS = 60
    pygame.quit()