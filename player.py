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
        self.health_point = 100
         
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
        
    def draw(self, image, surface, cam_x, cam_y):
        mouse_x, mouse_y = pg.mouse.get_pos()

        draw_x = self.rect.x - cam_x
        draw_y = self.rect.y - cam_y

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
   
    def take_damage(self, amount):
        self.health_point -= amount
        if self.health_point <= 0:
            self.dead = True

    def shoot(self, surface, enemies, shot_length, damage_number):
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
                    damage_number.append(DamageNumber(enemy.rect.centerx, enemy.rect.centery, "-10"))
                    if dead:
                        enemies.remove(enemy)
                    hit = True
                    break
            if hit:
                break

                    
class DamageNumber():
    def __init__(self, x, y, text):
        self.x = x
        self.y = y
        self.text = text
        self.alpha = 255
        self.font = pg.font.Font(None, 30)

    def update(self):
        self.y -= 1 
        self.alpha -= 5
        if self.alpha < 0:
            self.alpha = 0
    def draw(self, surface, cam_x, cam_y):
        text = self.font.render(self.text, True, (255, 0, 0))
        text.set_alpha(self.alpha)
        surface.blit(text, (self.x, self.y))
    def is_dead(self):
        return self.alpha <= 0


class Camera():
    def __init__(self, x,y):
        self.x = x
        self.y = y 

    def update(self, Player, game_map): 
        map_width = len(game_map.map[0]) * game_map.tile_size
        map_height = len(game_map.map) * game_map.tile_size        
        
        self.x = Player.get_position()[0] - config.WIDTH // 2 # player get_position
        self.y = Player.get_position()[1] - config.HEIGHT // 2 # player get_position

        self.x = max(0, min(self.x, map_width - config.WIDTH))
        self.y = max(0, min(self.y, map_height - config.HEIGHT))

        if self.x < 0:
            self.x = 0
        if self.y < 0:
            self.y = 0

        if self.x > map_width - config.WIDTH:
            self.x = map_width - config.WIDTH
        if self.y > map_height - config.HEIGHT:
            self.y = map_height - config.HEIGHT

        return self.x, self.y



