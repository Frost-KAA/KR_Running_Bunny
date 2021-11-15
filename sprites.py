# sprite classes for game
import pygame as pg
from random import choice, randrange
from settings import *
vec = pg.math.Vector2

class Spritesheet:
    # loading and parsing spritesheets
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert_alpha()

    def get_image(self, x, y, width, height):
        # grab on image out of a larger spritesheet
        image = pg.Surface((width, height), pg.SRCALPHA)
        image.blit(self.spritesheet, (0,0), (x,y,width, height))
        image = pg.transform.scale(image, (width // 2, height // 2))
        #image.set_colorkey(BLACK)
        return image

class Background:
    # loading and parsing bg
    def __init__(self, filename):
        image = pg.image.load(filename).convert()
        self.bg_image = pg.transform.scale(image, (1000, 500))
        self.bg_image.set_colorkey(BLACK)


class Player(pg.sprite.Sprite):

    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.walking = False
        self.jumping = False
        self.falling = False
        self.current_frame = 0
        self.last_update = 0
        self.load_images()
        self.image = self.game.spritesheet.get_image(614, 1063, 120, 191)
        self.rect = self.image.get_rect()
        self.rect.center = (50, HEIGHT-PLAT_H-20)
        self.pos = vec(50, HEIGHT-PLAT_H-20)
        self.vel = vec(4, 0)
        self.acc = vec(0, 0)

    def load_images(self):
        # bunny 2
        self.standing_frames = [self.game.spritesheet.get_image(581, 1265, 121, 191), #ready
                                self.game.spritesheet.get_image(584, 0, 121, 201) #stand
                                ]
        # bunny 1
        #self.standing_frames = [self.game.spritesheet.get_image(614, 1063, 120, 191), #ready
        #                        self.game.spritesheet.get_image(690, 406, 120, 201) #stand
        #                        ]


         # bunny 2
        self.walking_frames = [self.game.spritesheet.get_image(584, 203, 121, 201), #walk1
                                self.game.spritesheet.get_image(678, 651, 121, 207) #walk2
                                ]
        # bunny 1
        # self.walking_frames = [self.game.spritesheet.get_image(678, 860, 120, 201), #walk1
        #                         self.game.spritesheet.get_image(692, 1458, 120, 207) #walk2
        #                         ]


        # bunny 2
        self.jumping_frame = self.game.spritesheet.get_image(416, 1660, 150, 181) #jump
        # bunny 1
        #self.jumping_frame = self.game.spritesheet.get_image(382, 763, 150, 181) #jump


        # bunny 2
        self.falling_frame = self.game.spritesheet.get_image(411, 1866, 150, 174)
        # bunny 1
        #self.falling_frame = self.game.spritesheet.get_image(382, 946, 150, 174)


    def jump(self):
        # jump only if standing on a platform
        self.rect.y += 2
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.y -= 2
        if hits and not self.jumping:
            self.jumping = True
            self.vel.y -= PLAYER_JUMP
            self.game.jump_sound.play()
        elif not hits and self.jumping:
            self.vel.y = -0.8*PLAYER_JUMP
            self.jumping = False
            self.game.jump_sound.play()

    def fall(self):
        self.now_time = pg.time.get_ticks()   
        if (self.now_time - self.game.end_time > 500):
            self.game.ending = False
        bottom = self.rect.midbottom
        self.image = self.falling_frame
        self.rect = self.image.get_rect()
        self.rect.midbottom = bottom

        speed = abs(self.vel.y)
        for one in self.game.all_sprites:
            if one is self:
                continue
            one.rect.y -= speed
        

    def update(self):
        self.animate()
        self.now_time = pg.time.get_ticks()   
        if (self.now_time - self.game.start_time < 2000):
                return 
        self.walking = True
        self.acc = vec(0.001, PLAYER_GRAV)
        keys = pg.key.get_pressed()

        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        self.rect.midbottom = self.pos

    def animate(self):
        now = pg.time.get_ticks()

        if self.vel.y != 0:
            self.falling = True
        else:
            self.falling = False 
        
        #jumping
        if self.falling:
             if now - self.last_update > 150:
                 self.last_update = now
                 bottom = self.rect.midbottom
                 self.image = self.jumping_frame
                 self.rect = self.image.get_rect()
                 self.rect.midbottom = bottom

        # walking
        elif self.walking:
            if now - self.last_update > 150:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.walking_frames)
                bottom = self.rect.midbottom
                self.image = self.walking_frames[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.midbottom = bottom

        #standing
        else:
            if now - self.last_update > 300:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
                bottom = self.rect.midbottom
                self.image = self.standing_frames[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.midbottom = bottom
        


class Platform(pg.sprite.Sprite):
    def __init__(self, game, x, y, size_number):
        pg.sprite.Sprite.__init__(self)
        self.game = game

      
        #stone
        # images = [self.game.spritesheet.get_image(0, 96, 380, 94), #ground_stone
        #             self.game.spritesheet.get_image(382, 408, 200, 100), #ground_stone_small
        #             self.game.spritesheet.get_image(0, 192, 380, 94), #ground_stone_broken
        #             self.game.spritesheet.get_image(232, 1288, 200, 100) #ground_stone_small_broken
        #             ]

        #cake
        # images = [self.game.spritesheet.get_image(0, 576, 380, 94), #ground_cake
        #             self.game.spritesheet.get_image(218, 1456, 201, 100), #ground_cake_small
        #             self.game.spritesheet.get_image(0, 0, 380, 94), #ground_cake_broken
        #             self.game.spritesheet.get_image(262, 1152, 200, 100) #ground_cake_small_broken
        #             ]


        # grass
        images = [self.game.spritesheet.get_image(0, 288, 380, 94), #ground_grass
                    self.game.spritesheet.get_image(213, 1662, 201, 100), #ground_small_grass
                    self.game.spritesheet.get_image(0, 384, 380, 94), #ground_grass_broken
                    self.game.spritesheet.get_image(382, 204, 200, 100) #ground_grass_small_broken
                    ]
        
        if size_number == 0:
            self.image = images[0]
        elif size_number == 1:
            self.image = images[1]
        else:
            self.image = choice(images)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.rect.width += 30

        if randrange(100) < MONEY_SPAN:
            m = Money(self.game, self)
            self.game.money_group.add(m)
            self.game.all_sprites.add(m)

        self.now_time = pg.time.get_ticks()   
        is_time_for_enimy = self.now_time - self.game.start_time > 5000
        if randrange(100) < ENIMY_SPAN and is_time_for_enimy :
            e = Enimy(self.game, self)
            self.game.enimies.add(e)
            self.game.all_sprites.add(e)


class Money(pg.sprite.Sprite):
    def __init__(self, game, plat):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.plat = plat
        self.current_frame = 0
        self.last_update = 0
        self.type = 'coin'

        # gold caroot
        if randrange(100) < GOLD_CAROOT_SPAN:
            self.type = 'caroot'

        self.frames = [self.game.spritesheet.get_image(698, 1931, 84, 84), #gold1
                    self.game.spritesheet.get_image(829, 0, 66, 84), #gold2
                    self.game.spritesheet.get_image(897, 1574, 50, 84), #gold3
                    self.game.spritesheet.get_image(645, 651, 15, 84) #gold4
                    ]
        
        if self.type == 'coin':
            self.image = self.frames[0]
        else:
            self.image = self.game.spritesheet.get_image(814, 1661, 78, 70) #carrot_gold

        self.rect = self.image.get_rect()

        place = choice([0,1])
        self.x = 0
        self.y = 5
        if place == 0:
            self.x = randrange(50, 200)
            self.y = randrange(5, 100)
        self.rect.centerx = self.plat.rect.centerx + self.x
        self.rect.bottom = self.plat.rect.top - self.y

    def update(self):
        if not self.game.platforms.has(self.plat):
            self.kill()
        self.animate()

    def animate(self):
        if self.type == 'coin':
            now = pg.time.get_ticks()
            if now - self.last_update > 300:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.frames)
                self.image = self.frames[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.centerx = self.plat.rect.centerx + self.x
                self.rect.bottom = self.plat.rect.top - self.y



 
class Enimy(pg.sprite.Sprite):
    def __init__(self, game, plat):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.plat = plat
        self.current_frame = 0
        self.last_update = 0
        self.frames = [self.game.spritesheet.get_image(814, 1417, 90, 155), #spikeMan_stand
                        self.game.spritesheet.get_image(736, 1063, 114, 155), #spikeMan_jump 
                        ]
        self.image = self.frames[0]
        self.rect = self.image.get_rect()
        self.rect.centerx = self.plat.rect.centerx
        self.rect.bottom = self.plat.rect.top - 5

    def update(self):
        if not self.game.platforms.has(self.plat):
            self.kill()
        self.animate()

    def animate(self):
        now = pg.time.get_ticks()
        if now - self.last_update > 300:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]
            self.rect = self.image.get_rect()
            self.rect.centerx = self.plat.rect.centerx 
            self.rect.bottom = self.plat.rect.top - 5



class Caroot(pg.sprite.Sprite):
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image =  self.game.spritesheet.get_image(820, 1733, 78, 70) #carrot
        self.image = pg.transform.rotate(self.image, 45)
        self.rect = self.image.get_rect()

        self.rect.center = (self.game.player.rect.x+40, self.game.player.rect.y+40)
        self.pos = self.rect.x+10
        self.vel = 6
        self.acc = 0

    def update(self):
        self.acc = 0.005
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        self.rect.centerx = self.pos

