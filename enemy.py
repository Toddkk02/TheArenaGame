import pygame as pg 
import config
import math
import player
import map
import random

class Enemy(pg.sprite.Sprite):
    def __init__(self, x, y):
        self.image = pg.Surface((config.DIMENSION_ENEMY, config.DIMENSION_ENEMY))
        self.image = pg.image.load("./assets/enemy.png").convert_alpha()
        self.image = pg.transform.scale(self.image, (config.DIMENSION_ENEMY, config.DIMENSION_ENEMY))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y) # position on screen
        self.speed = config.EMEMY_SPEED
        self.player = player.Player
        self.facing_angle = 0
  
    def update(self, player, game_map):
        if not self.angle_vision_degree(player):
            return
        
                # getting old position
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
    
        # check collision
        if game_map.collision(self.rect):
            self.rect.x = old_x
            self.rect.y = old_y            

        self.facing_angle = math.atan2(dy, dx)

    def angle_vision_degree(self, player):
        px, py = player.get_position()
        dx = px - self.rect.centerx
        dy = py - self.rect.centery
        distance = math.hypot(dx, dy)
    
        angle_to_player = math.atan2(dy, dx)
        angle_diff = angle_to_player - self.facing_angle
    
        if angle_diff < -math.pi:
            angle_diff += 2 * math.pi
        elif angle_diff > math.pi:
            angle_diff -= 2 * math.pi
            
        return abs(angle_diff) < math.pi / 4 and distance < config.MAX_FOLLOW_DISTANCE 
    
    def draw_fov_debug(self, surface):
        fov_distance = config.MAX_FOLLOW_DISTANCE
        left_angle = self.facing_angle - math.pi / 4
        right_angle = self.facing_angle + math.pi / 4

        left_end = (self.rect.centerx + fov_distance * math.cos(left_angle), self.rect.centery + fov_distance * math.sin(left_angle))
        right_end = (self.rect.centerx + fov_distance * math.cos(right_angle), self.rect.centery + fov_distance * math.sin(right_angle))

        pg.draw.line(surface, (255, 0, 0), self.rect.center, left_end)
        pg.draw.line(surface, (255, 0, 0), self.rect.center, right_end)

    def draw(self, surface):
        enemy = surface.blit(self.image, self.rect)
        self.draw_fov_debug(surface)
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

    
