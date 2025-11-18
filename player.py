import pygame as pg 
import config
import map
class Player(pg.sprite.Sprite):
    def __init__(self, x, y):
        self.image = pg.Surface((config.DIMENSION_PLAYER,config.DIMENSION_PLAYER))
        self.image = pg.image.load("./assets/red_circle.png").convert_alpha()
        self.image = pg.transform.scale(self.image, (config.DIMENSION_PLAYER, config.DIMENSION_PLAYER))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y) # position 
        self.speed = config.PLAYER_SPEED
        #self.start_position = (x, y)
    def update(self, k_pressed, game_map):
        # Get current position
        old_x = self.rect.x
        old_y = self.rect.y
        
        if k_pressed[pg.K_w] and self.rect.top > 0:
            self.rect.y -= self.speed
            if game_map.collision(self.rect):  # check for collision
                self.rect.y = old_y
                
        if k_pressed[pg.K_s] and self.rect.bottom < config.HEIGHT:
            self.rect.y += self.speed
            if game_map.collision(self.rect):
                self.rect.y = old_y
                
        if k_pressed[pg.K_a] and self.rect.left > 0:
            self.rect.x -= self.speed
            if game_map.collision(self.rect):
                self.rect.x = old_x
                
        if k_pressed[pg.K_d] and self.rect.right < config.WIDTH:
            self.rect.x += self.speed
            if game_map.collision(self.rect):
                self.rect.x = old_x
    def draw(self, image, surface):
        surface.blit(self.image, self.rect)
        # Get current position
    def get_position(self):
        #print("Getting player position ")
        #print(self.rect.topleft)
        return self.rect.topleft
        
    def set_position(self, x, y):
        #print("Setting player position to: ", x, y)
        self.rect.topleft = (100, 100)
        #print("New player position: ", self.rect.topleft)
        return self.rect.topleft

    def reset_position(self):
        #print("Resetting player position to (100, 100)")
        self.rect.topleft = (100, 100)
        #print("Player position after reset: ", self.rect.topleft)
        return self.rect.topleft


