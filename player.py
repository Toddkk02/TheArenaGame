import pygame as pg 
import config
import map
import math
import enemy

class Player(pg.sprite.Sprite):
    def __init__(self, x, y):
        self.image = pg.Surface((config.DIMENSION_PLAYER,config.DIMENSION_PLAYER))
        self.image = pg.image.load("./assets/player.png").convert_alpha()
        self.image = pg.transform.scale(self.image, (config.DIMENSION_PLAYER, config.DIMENSION_PLAYER))
        self.original_image = self.image.copy()
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y) # position 
        self.speed = config.PLAYER_SPEED
         
        
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
        mouse_x, mouse_y = pg.mouse.get_pos()
        dx = mouse_x - self.rect.centerx
        dy = mouse_y - self.rect.centery
        angle = math.atan2(dy, dx)
        angle_degrees = math.degrees(angle)
    
        # Il soldato parte guardando a destra (0°), quindi inverti solo l'angolo
        rotated_image = pg.transform.rotate(self.original_image, -angle_degrees)
        rotated_rect = rotated_image.get_rect(center=self.rect.center)
        surface.blit(rotated_image, rotated_rect)
    
       
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
    
    def shoot(self, surface, enemies):
        if pg.mouse.get_pressed()[0]:
            mouse_x, mouse_y = pg.mouse.get_pos()
            shoot = pg.draw.line(surface, (255, 0, 0), self.rect.center, (mouse_x, mouse_y), 2)

            dx = mouse_x - self.rect.centerx
            dy = mouse_y - self.rect.centery
            angle = math.atan2(dy, dx)

            x = self.rect.centerx
            y = self.rect.centery
            
            for i in range(0, 800, 5):
                px = x + math.cos(angle) * i
                py = y + math.sin(angle) * i
                
                for e in enemies[:]:
                    if e.rect.collidepoint(px, py):
                        enemies.remove(e)
