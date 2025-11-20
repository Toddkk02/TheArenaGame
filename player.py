import pygame as pg 
import config
import map
import math

class Player(pg.sprite.Sprite):
    def __init__(self, x, y):
        self.image = pg.Surface((config.DIMENSION_PLAYER,config.DIMENSION_PLAYER))
        self.image = pg.image.load("./assets/player.png").convert_alpha()
        self.image = pg.transform.scale(self.image, (config.DIMENSION_PLAYER, config.DIMENSION_PLAYER))
        self.original_image = self.image.copy()
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.speed = config.PLAYER_SPEED
        self.dead = False
         
    def update(self, k_pressed, game_map):
        old_x = self.rect.x
        old_y = self.rect.y
        
        if k_pressed[pg.K_w] and self.rect.top > 0:
            self.rect.y -= self.speed
            if game_map.collision(self.rect):
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
        rotated_image = pg.transform.rotate(self.original_image, -angle_degrees)
        rotated_rect = rotated_image.get_rect(center=self.rect.center)
        surface.blit(rotated_image, rotated_rect)

    def get_position(self):
        return self.rect.topleft
        
    def set_position(self):
        self.rect.topleft = (100, 100)
        return self.rect.topleft

    def reset_position(self):
        self.rect.topleft = (100, 100)
        return self.rect.topleft
    
    def shoot(self, surface, enemies, shot_length):
        mouse_x, mouse_y = pg.mouse.get_pos()
        x0, y0 = self.rect.center
        dx = mouse_x - x0 
        dy = mouse_y - y0 
        angle = math.atan2(dy, dx)
        x1 = x0 + math.cos(angle) * shot_length
        y1 = y0 + math.sin(angle) * shot_length
        hit, dead = False, False
        pg.draw.line(surface, (255, 0, 0), (x0, y0), (x1, y1), 2)

        for i in range(0, shot_length, 5):
            px = x0 + math.cos(angle) * i
            py = y0 + math.sin(angle) * i
            for enemy in enemies:
                if enemy.rect.collidepoint(px, py):
                    dead = enemy.get_damage(10)
                    if dead:
                        enemies.remove(enemy)
                    hit = True
                    break
            if hit:
                damage_logo = pg.font.SysFont("Arial", 20)
                damage_text = damage_logo.render("-10", True, (255, 0, 0))
                surface.blit(damage_text, (enemy.rect.centerx, enemy.rect.centery))
                break

                    
                
