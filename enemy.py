import pygame as pg 
import config
import math
import player
import map
import random

class Enemy(pg.sprite.Sprite):
    def __init__(self, x, y):
        self.image = pg.Surface((config.DIMENSION_ENEMY, config.DIMENSION_ENEMY))
        self.image = pg.image.load("./assets/blue_circle.png").convert_alpha()
        self.image = pg.transform.scale(self.image, (config.DIMENSION_ENEMY, config.DIMENSION_ENEMY))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y) # position on screen
        self.speed = config.EMEMY_SPEED
        self.player = player.Player

  
    def update(self, player, game_map):
        #getting old position
        old_x = self.rect.x
        old_y = self.rect.y


        px, py = player.get_position()
        dx = px - self.rect.centerx
        dy = py - self.rect.centery
        distance = math.hypot(dx, dy)

        
        if distance < config.MIN_FOLLOW_DISTANCE:
            return
        if distance > config.MAX_FOLLOW_DISTANCE:
            return

        dx /= distance
        dy /= distance

        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed
        #check collision
        if game_map.collision(self.rect):
            self.rect.x = old_x
            self.rect.y = old_y


    def raycast(self, player, surface, ray_length=200):
        pos_x, pos_y = self.get_position()
        rays = []
        for angle in range(0, 360):
            angle_rad = math.radians(angle)
            dx = math.cos(angle_rad)
            dy = math.sin(angle_rad)
            
            end_x = pos_x + dx * ray_length
            end_y = pos_y + dy * ray_length

            ray = (pos_x, pos_y), (end_x, end_y)
            rays.append(ray)

            pg.draw.line(surface, (255, 255, 255), (pos_x, pos_y), (end_x, end_y), 1)
       
        return rays

    def draw(self, surface):
        enemy = surface.blit(self.image, self.rect)
        return enemy
    def get_position(self):
        return self.rect.topleft

    def set_position(self, x, y):
        self.rect.topleft = (x, y)
        #random position for testing
        self.rect.topleft = range(0, config.WIDTH - config.DIMENSION_ENEMY), range(0, config.HEIGHT - config.DIMENSION_ENEMY)        
        return self.rect.topleft

    def reset_position(self):
        self.rect.topleft = (300, 300)
        return self.rect.topleft

    
