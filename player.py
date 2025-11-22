import pygame as pg 
import config
import math

class Player(pg.sprite.Sprite):
    def __init__(self, x, y):
        self.image = pg.Surface((config.DIMENSION_PLAYER, config.DIMENSION_PLAYER))
        self.image = pg.image.load("./assets/player.png").convert_alpha()
        self.image = pg.transform.scale(self.image, (config.DIMENSION_PLAYER, config.DIMENSION_PLAYER))
        self.original_image = self.image.copy()
        
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        
        self.velocity = pg.math.Vector2(0, 0)
        self.speed = config.PLAYER_SPEED
        self.facing_angle = 0
        
        self.dead = False
        self.health_point = 100
         
    def update(self, k_pressed, game_map, mouse_pos, cam_x, cam_y):
                old_pos = pg.math.Vector2(self.rect.topleft)
                
                mx, my = mouse_pos
                px = self.rect.centerx - cam_x
                py = self.rect.centery - cam_y
            
                dir_vec = pg.math.Vector2(mx - px, my - py)
                
                if dir_vec.length_squared() >= 100:
                    self.facing_angle = math.atan2(dir_vec.y, dir_vec.x)
                
                move = pg.math.Vector2(0, 0)
                
                if k_pressed[pg.K_w]:
                    move.y -= 1
                if k_pressed[pg.K_s]:
                    move.y += 1
                if k_pressed[pg.K_a]:
                    move.x -= 1
                if k_pressed[pg.K_d]:
                    move.x += 1
                
                if move.length_squared() > 0:
                    move = move.normalize() * self.speed
                
                self.rect.x += move.x
                self.rect.y += move.y
                
                self.rect.x = max(0, min(self.rect.x, game_map.map_width - config.DIMENSION_PLAYER))
                self.rect.y = max(0, min(self.rect.y, game_map.map_height - config.DIMENSION_PLAYER))
                
                if game_map.collision(self.rect):
                    self.rect.topleft = old_pos
        
    def draw(self, image, surface, cam_x, cam_y):
        draw_pos = pg.math.Vector2(self.rect.x - cam_x, self.rect.y - cam_y)
        
        angle_deg = -math.degrees(self.facing_angle)
        rotated = pg.transform.rotate(self.original_image, angle_deg)
        
        center = draw_pos + pg.math.Vector2(config.DIMENSION_PLAYER // 2, config.DIMENSION_PLAYER // 2)
        rot_rect = rotated.get_rect(center=center)
        
        surface.blit(rotated, rot_rect)
    
    def create_torch_overlay(self, cam_x, cam_y, length=300, cone_angle=math.pi / 3):
        screen_center = (
            self.rect.centerx - cam_x,
            self.rect.centery - cam_y
        )
        
        surf = pg.Surface((config.WIDTH, config.HEIGHT), pg.SRCALPHA)
        
        points = [screen_center]
        segments = 20
        half_cone = cone_angle / 2
        
        for i in range(segments + 1):
            t = i / segments
            angle = self.facing_angle - half_cone + cone_angle * t
            px = screen_center[0] + length * math.cos(angle)
            py = screen_center[1] + length * math.sin(angle)
            points.append((px, py))
        
        pg.draw.polygon(surf, (255, 255, 200, 100), points)
        return surf

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

    def shoot(self, surface, enemies, shot_length, damage_number, cam_x, cam_y):
        origin = pg.math.Vector2(self.rect.center)
        direction = pg.math.Vector2(math.cos(self.facing_angle), math.sin(self.facing_angle))
        endpoint = origin + direction * shot_length
        
        screen_origin = origin - pg.math.Vector2(cam_x, cam_y)
        screen_end = endpoint - pg.math.Vector2(cam_x, cam_y)
        pg.draw.line(surface, (255, 0, 0), screen_origin, screen_end, 2)
        
        step = 5
        for dist in range(0, shot_length, step):
            point = origin + direction * dist
            
            for enemy in enemies:
                if enemy.rect.collidepoint(point.x, point.y):
                    dead = enemy.get_damage(10)
                    damage_number.append(DamageNumber(enemy.rect.centerx, enemy.rect.centery, "-10"))
                    if dead:
                        enemies.remove(enemy)
                    return


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
        surface.blit(text, (self.x - cam_x, self.y - cam_y))

    def is_dead(self):
        return self.alpha <= 0


class Camera():
    def __init__(self, x, y):
        self.x = x
        self.y = y 

    def update(self, player, game_map): 
        map_w = len(game_map.map[0]) * game_map.tile_size
        map_h = len(game_map.map) * game_map.tile_size        
        
        target = player.get_position()
        self.x = target[0] - config.WIDTH // 2
        self.y = target[1] - config.HEIGHT // 2

        self.x = max(0, min(self.x, map_w - config.WIDTH))
        self.y = max(0, min(self.y, map_h - config.HEIGHT))

        return self.x, self.y
    
    def get_position(self):
        return self.x, self.y
