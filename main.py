import pygame as pg
import random
from settings import *
from sprites import *
from os import path, getcwd
import sys

class Game:
    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.clock = pg.time.Clock()
        self.running = True
        self.font_name = pg.font.match_font('segoeui')
        self.load_data()
        pg.display.set_caption(TITLE)
       
        pg.display.set_icon(self.icon)

    def load_data(self):
        #load high score

        if getattr(sys, 'frozen', False):  # Is it CXFreeze frozen
            #self.dir = path.dirname( sys.executable ) 
            self.dir = sys._MEIPASS
        else:
            self.dir = path.dirname( path.realpath( __file__ ) ) 

        img_dir = path.join(self.dir, 'img')
        with open(path.join(self.dir, HS_FILE), 'r+') as f:
            try:
                self.high_score = int(f.read())
            except:
                self.high_score = 0
        
        #load images
        self.spritesheet = Spritesheet(path.join(img_dir, SPRITESHEET))
        self.bg0 = Background(path.join(img_dir, 'bg_layer1.png'))
        self.bg1 = Background(path.join(img_dir, 'bg_layer2.png'))
        self.bg2 = Background(path.join(img_dir, 'bg_layer3.png'))
        self.bg3 = Background(path.join(img_dir, 'bg_layer4.png'))
        self.score_image = self.spritesheet.get_image(244, 1981, 61, 61) #gold coin
        self.icon = pg.image.load(path.join(img_dir, "icon.png"))

        #load sounds
        self.snd_dir = path.join(self.dir, 'snd')
        self.jump_sound = pg.mixer.Sound(path.join(self.snd_dir, 'Jump10.wav'))
        self.coin_sound = pg.mixer.Sound(path.join(self.snd_dir, 'money2.mp3'))
        self.kill_sound = pg.mixer.Sound(path.join(self.snd_dir, 'kill1.mp3'))
        self.shoot_sound = pg.mixer.Sound(path.join(self.snd_dir, 'shoot1.mp3'))

    def new(self):
        # start a new game
        self.score = 0
        self.start_time = pg.time.get_ticks()
        self.last_shoot = self.start_time
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.money_group = pg.sprite.Group()
        self.enimies = pg.sprite.Group()
        self.caroots = pg.sprite.Group() 
        self.player = Player(self)
        self.all_sprites.add(self.player)
        for plat in PLATFORM_LIST:
            p = Platform(self, *plat)
            self.all_sprites.add(p)
            self.platforms.add(p)
        pg.mixer.music.load(path.join(self.snd_dir, '1fon.mp3'))
        self.run()

    def run(self):
        pg.mixer.music.play(loops=-1)
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
        pg.mixer.music.fadeout(500)
        self.end_time = pg.time.get_ticks() 
        self.ending = True
        while self.ending:
            self.clock.tick(FPS)
            self.player.fall()
            self.draw()

    def update(self):
        self.all_sprites.update()

        # jump
        hits = pg.sprite.spritecollide(self.player, self.platforms, False)
        if hits:
                if self.player.pos.x < hits[0].rect.right+30 and \
                self.player.pos.x > hits[0].rect.left-30 and \
                self.player.pos.y < hits[0].rect.bottom:
                    self.player.vel.y = 0
                    self.player.pos.y = hits[0].rect.top
                    self.player.rect.midbottom = self.player.pos
                    self.player.jumping = False

        # player gets money
        money_hits = pg.sprite.spritecollide(self.player, self.money_group, True)
        for m in money_hits:
            self.coin_sound.play()
            if m.type == 'coin':
                self.score += 100
            else:
                self.score += 500

        # player meets enimy
        enimy_hits = pg.sprite.spritecollide(self.player, self.enimies, False)
        for enimy in enimy_hits:
            self.playing = False

        # caroot meets enimy
        for enimy in self.enimies:
            caroot_hits = pg.sprite.spritecollide(enimy, self.caroots, True)
            for caroot in caroot_hits:
                self.kill_sound.play()
                enimy.kill()
                self.score += 100
            

        # moving screen 
        if self.player.rect.right >= WIDTH / 4:
            speed = abs(self.player.vel.x)
            self.player.pos.x -= speed
            for plat in self.platforms:
                plat.rect.x -= speed
                if plat.rect.right < 0:
                    plat.kill()
                    self.score += 10
            for money in self.money_group:
                money.rect.x -= speed
                if money.rect.right < 0:
                    money.kill()
            for caroot in self.caroots:
                caroot.rect.x -= speed
                if caroot.rect.left > WIDTH or caroot.rect.right < 0:
                    caroot.kill() 
            for enimy in self.enimies:
                enimy.rect.x -= speed
                if enimy.rect.right < 0:
                    enimy.kill()


                  
        # You die
        if self.player.rect.bottom > HEIGHT-20:
           self.playing = False       

        # span new platforms
        while len(self.platforms) < 5:
            p = Platform(self, WIDTH + random.randrange(80, 200),
                        HEIGHT - random.randrange(60, 160), 2)     
            self.platforms.add(p)
            self.all_sprites.add(p)


    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                now_time = pg.time.get_ticks()   
                if (now_time - self.start_time < 2000):
                    continue
                if event.key == pg.K_RIGHT or event.key == pg.K_z:
                    if now_time - self.last_shoot > 300:
                        c = Caroot(self)
                        self.shoot_sound.play()
                        self.caroots.add(c)
                        self.all_sprites.add(c)
                        self.last_shoot = pg.time.get_ticks()   
                if event.key == pg.K_SPACE:
                    self.player.jump()
                    
        
    def draw(self):
        self.screen.fill(WHITE)
        self.screen.blit(self.bg0.bg_image, (0, 0))
        self.screen.blit(self.bg1.bg_image, (0, 0))
        self.screen.blit(self.bg2.bg_image, (0, 0))
        self.screen.blit(self.bg3.bg_image, (0, 0))
        self.all_sprites.draw(self.screen)
        self.screen.blit(self.player.image, self.player.rect)
        self.screen.blit(self.score_image, (150, 15))
        self.draw_text(str(self.score), 22, DARK_BLUE, 220, 15)
        pg.display.flip()

    def show_start_screen(self):
        pg.mixer.music.load(path.join(self.snd_dir, 'Yippee.wav'))
        pg.mixer.music.play()
        self.screen.fill(WHITE)
        image1 = pg.transform.scale(self.spritesheet.get_image(416, 1660, 150, 181), (100, 120))
        image1 = pg.transform.rotate(image1, 20)
        image2 = pg.transform.scale(self.spritesheet.get_image(382, 763, 150, 181), (100, 120))
        image2 = pg.transform.rotate(image2, -20)
        self.screen.blit(self.bg2.bg_image, (0, 0))
        self.screen.blit(image1, (50, 50))
        self.screen.blit(image2, (800, 100))
        self.draw_text(TITLE, 48, DARK_BLUE, WIDTH/2, HEIGHT/4)
        self.draw_text("Help Bunny to overcome obstacles", 22, DARK_BLUE, WIDTH/2, HEIGHT/2)
        self.draw_text("Press a key to play", 22, DARK_BLUE, WIDTH/2, HEIGHT*3/4)
        self.draw_text("High Score:" + str(self.high_score), 22, DARK_BLUE, WIDTH/2, 15)
        pg.display.flip()
        self.wait_for_key()
        pg.mixer.music.fadeout(500)

    def show_go_screen(self):
        if not self.running:
            return
        pg.mixer.music.load(path.join(self.snd_dir, 'end1.mp3'))
        pg.mixer.music.play()    
        self.screen.fill(WHITE)
        image1 = pg.transform.scale(self.spritesheet.get_image(411, 1866, 150, 174), (100, 120))
        image1 = pg.transform.rotate(image1, 20)
        image2 = pg.transform.scale(self.spritesheet.get_image(382, 946, 150, 174), (100, 120))
        image2 = pg.transform.rotate(image2, -20)
        self.screen.blit(self.bg3.bg_image, (0, 0))
        self.screen.blit(image1, (50, 50))
        self.screen.blit(image2, (800, 100))
        self.draw_text("GAME OVER", 48, DARK_BLUE, WIDTH/2, HEIGHT/4-50)
        self.draw_text("Score: " + str(self.score), 22, DARK_BLUE, WIDTH/2, HEIGHT/2-50)
        self.draw_text("Press a key to play again", 22, DARK_BLUE, WIDTH/2, HEIGHT*3/4-50)
        if self.score > self.high_score:
            self.high_score = self.score
            self.draw_text("NEW HIGH SCORE!", 22, DARK_BLUE, WIDTH/2, HEIGHT/2 - 10)
            with open(path.join(self.dir, HS_FILE), 'w') as f:
                f.write(str(self.score))
        else:
            self.draw_text("High Score:" + str(self.high_score), 22, DARK_BLUE, WIDTH/2, HEIGHT/2 - 10)
        pg.display.flip()
        self.wait_for_key()
        pg.mixer.music.fadeout(500)


    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYUP:
                    waiting = False

    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)
        

g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()

pg.quit()
