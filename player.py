import pygame as pg 
import config
import math

class Player(pg.sprite.Sprite):
    def __init__(self, x, y):
        # Load and scale player sprite
        self.image = pg.Surface((config.DIMENSION_PLAYER, config.DIMENSION_PLAYER))
        self.image = pg.image.load("./assets/player.png").convert_alpha()
        self.image = pg.transform.scale(self.image, (config.DIMENSION_PLAYER, config.DIMENSION_PLAYER))
        self.original_image = self.image.copy()  # Keep original for rotation
        
        # Position and collision rect
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        
        # Movement
        self.speed = config.PLAYER_SPEED
        self.facing_angle = 0  # Direction player is facing (radians)
        
        # Stats
        self.dead = False
        self.health_point = 100
         
    def update(self, k_pressed, game_map):
        """Handle player movement with WASD keys"""
        old_x = self.rect.x
        old_y = self.rect.y
        
        # Track movement direction
        dx, dy = 0, 0
        
        if k_pressed[pg.K_w]:
            dy = -1
        if k_pressed[pg.K_s]:
            dy = 1
        if k_pressed[pg.K_a]:
            dx = -1
        if k_pressed[pg.K_d]:
            dx = 1
        
        # Update facing angle only when moving
        if dx != 0 or dy != 0:
            self.facing_angle = math.atan2(dy, dx)
        
        # Apply movement
        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed
        
        # Keep player within map bounds
        self.rect.x = max(0, min(self.rect.x, game_map.map_width - config.DIMENSION_PLAYER))
        self.rect.y = max(0, min(self.rect.y, game_map.map_height - config.DIMENSION_PLAYER))
        
        # Collision check - revert if hitting wall
        if game_map.collision(self.rect):
            self.rect.x = old_x
            self.rect.y = old_y
        
    def draw(self, image, surface, cam_x, cam_y):
        """Draw player sprite rotated towards movement direction"""
        # Convert world position to screen position
        draw_x = self.rect.x - cam_x
        draw_y = self.rect.y - cam_y
        
        # Rotate sprite based on facing angle
        angle_degrees = math.degrees(self.facing_angle)
        rotated_image = pg.transform.rotate(self.original_image, -angle_degrees)
        
        # Center the rotated image on player position
        screen_center_x = draw_x + config.DIMENSION_PLAYER // 2
        screen_center_y = draw_y + config.DIMENSION_PLAYER // 2
        rotated_rect = rotated_image.get_rect(center=(screen_center_x, screen_center_y))
        
        surface.blit(rotated_image, rotated_rect)
    
    def create_torch_overlay(self, cam_x, cam_y, length=300, cone_angle=math.pi / 3):
        """Create a cone of light following player's movement direction"""
        # Player center in screen coordinates
        screen_center_x = self.rect.centerx - cam_x
        screen_center_y = self.rect.centery - cam_y
        
        # Create transparent surface
        surf = pg.Surface((config.WIDTH, config.HEIGHT), pg.SRCALPHA)
        
        # Build cone polygon points
        center = (screen_center_x, screen_center_y)
        points = [center]
        
        num_points = 20  # More points = smoother edge
        for i in range(num_points + 1):
            # Calculate angle for this point along the cone arc
            a = self.facing_angle - cone_angle/2 + (cone_angle * i / num_points)
            px = center[0] + length * math.cos(a)
            py = center[1] + length * math.sin(a)
            points.append((px, py))
        
        # Draw the light cone
        pg.draw.polygon(surf, (255, 255, 200, 100), points)
        
        return surf

    def get_position(self):
        """Return player position in world coordinates"""
        return self.rect.topleft
        
    def set_position(self):
        """Set player to starting position"""
        self.rect.topleft = (100, 100)
        return self.rect.topleft

    def reset_position(self):
        """Reset player to starting position"""
        self.rect.topleft = (100, 100)
        return self.rect.topleft
   
    def take_damage(self, amount):
        """Reduce health and check for death"""
        self.health_point -= amount
        if self.health_point <= 0:
            self.dead = True

    def shoot(self, surface, enemies, shot_length, damage_number, cam_x, cam_y):
        """Fire a shot in the direction player is facing"""
        # Start position (player center in world coords)
        x0, y0 = self.rect.center
        
        # End position based on facing angle
        x1 = x0 + math.cos(self.facing_angle) * shot_length
        y1 = y0 + math.sin(self.facing_angle) * shot_length
        
        # Draw shot line (convert to screen coords)
        pg.draw.line(surface, (255, 0, 0), 
                     (x0 - cam_x, y0 - cam_y), 
                     (x1 - cam_x, y1 - cam_y), 2)
        
        # Check for hits along the shot path
        hit = False
        for i in range(0, shot_length, 5):
            # Point along the ray in world coords
            px = x0 + math.cos(self.facing_angle) * i
            py = y0 + math.sin(self.facing_angle) * i
            
            for enemy in enemies:
                if enemy.rect.collidepoint(px, py):
                    # Hit! Apply damage
                    dead = enemy.get_damage(10)
                    damage_number.append(DamageNumber(enemy.rect.centerx, enemy.rect.centery, "-10"))
                    
                    if dead:
                        enemies.remove(enemy)
                    hit = True
                    break
            if hit:
                break


class DamageNumber():
    """Floating damage text that rises and fades"""
    def __init__(self, x, y, text):
        # Position in WORLD coordinates
        self.x = x
        self.y = y
        self.text = text
        self.alpha = 255
        self.font = pg.font.Font(None, 30)

    def update(self):
        """Move up and fade out"""
        self.y -= 1 
        self.alpha -= 5
        if self.alpha < 0:
            self.alpha = 0

    def draw(self, surface, cam_x, cam_y):
        """Draw at screen position (world pos - camera)"""
        text = self.font.render(self.text, True, (255, 0, 0))
        text.set_alpha(self.alpha)
        surface.blit(text, (self.x - cam_x, self.y - cam_y))

    def is_dead(self):
        """Check if faded completely"""
        return self.alpha <= 0


class Camera():
    """Camera that follows the player"""
    def __init__(self, x, y):
        self.x = x
        self.y = y 

    def update(self, player, game_map): 
        """Center camera on player, clamped to map bounds"""
        map_width = len(game_map.map[0]) * game_map.tile_size
        map_height = len(game_map.map) * game_map.tile_size        
        
        # Center on player
        self.x = player.get_position()[0] - config.WIDTH // 2
        self.y = player.get_position()[1] - config.HEIGHT // 2

        # Clamp to map bounds
        self.x = max(0, min(self.x, map_width - config.WIDTH))
        self.y = max(0, min(self.y, map_height - config.HEIGHT))

        return self.x, self.y
    
    def get_position(self):
        """Return camera position"""
        return self.x, self.y
