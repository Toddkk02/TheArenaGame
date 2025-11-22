import pygame as pg
from config import *
import config

class Map:
    def __init__(self):
        self.tile_size = TILE_SIZE
        self.map = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 1, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 1],
    [1, 0, 2, 1, 1, 1, 1, 1, 2, 0, 0, 0, 0, 0, 1, 0, 0, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 2, 0, 0, 0, 0, 0, 1],
    [1, 0, 2, 1, 3, 3, 3, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 3, 3, 3, 3, 3, 3, 3, 1, 2, 0, 0, 0, 2, 1, 3, 3, 3, 3, 1, 2, 0, 0, 0, 0, 0, 1],
    [1, 0, 2, 1, 3, 3, 3, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 3, 3, 3, 3, 3, 3, 3, 1, 2, 0, 0, 0, 2, 1, 3, 3, 3, 3, 1, 2, 0, 0, 0, 0, 0, 1],
    [1, 0, 2, 1, 3, 3, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 3, 3, 3, 3, 3, 3, 3, 0, 2, 0, 0, 0, 2, 3, 3, 3, 3, 3, 1, 2, 0, 0, 0, 0, 0, 1],
    [1, 0, 2, 1, 1, 1, 1, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 2, 0, 0, 0, 0, 0, 1],
    [1, 0, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 3, 3, 3, 3, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 3, 3, 3, 3, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 3, 3, 3, 3, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 3, 3, 3, 3, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 3, 3, 3, 3, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 3, 3, 3, 3, 3, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 1, 1, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 3, 3, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 3, 3, 3, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 1, 1, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 1],
    [1, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 0, 1],
    [1, 0, 2, 1, 3, 3, 3, 3, 3, 3, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 3, 3, 3, 3, 3, 3, 1, 2, 0, 1],
    [1, 0, 2, 1, 3, 3, 3, 3, 3, 3, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 3, 3, 3, 3, 3, 3, 1, 2, 0, 1],
    [1, 0, 2, 2, 3, 3, 3, 3, 3, 3, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 3, 3, 3, 3, 3, 3, 3, 1, 2, 0, 1],
    [1, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1],
    [1, 0, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]       
        self.floor = pg.image.load("./assets/floor.png").convert_alpha()
        self.wall = pg.image.load("./assets/wall.png").convert_alpha()
        self.grass = pg.image.load("./assets/grass.png").convert_alpha()
        self.roof = pg.image.load("./assets/roof.png").convert_alpha()
        self.floor = pg.transform.scale(self.floor, (self.tile_size, self.tile_size))
        self.wall = pg.transform.scale(self.wall, (self.tile_size, self.tile_size))
        self.map_width = len(self.map[0]) * self.tile_size
        self.map_height = len(self.map) * self.tile_size
        
        self.light_positions = [
            (280, 280),
            (1176, 280),
            (1344, 336),
            (1960, 280),
            (672, 672),
            (728, 728),
            (1680, 672),
            (1176, 1008),
            (280, 1344),
            (392, 1400),
            (2016, 1344),
            (2128, 1400),
            (504, 504),
            (1400, 896),
            (2240, 560),
        ]
        
        self.light_mask = self.create_light_mask(150)
        self.player_light_mask = self.create_light_mask(180)

    def create_light_mask(self, radius):
        size = radius * 2
        mask = pg.Surface((size, size), pg.SRCALPHA)
        for y in range(size):
            for x in range(size):
                dx = x - radius
                dy = y - radius
                dist = (dx * dx + dy * dy) ** 0.5
                if dist < radius:
                    alpha = int(255 * (1 - dist / radius))
                    mask.set_at((x, y), (255, 255, 255, alpha))
        return mask

    def draw(self, surface, cam_x, cam_y):
        for row_index, row in enumerate(self.map):
            for column_index, tile in enumerate(row):
                x = column_index * self.tile_size - cam_x
                y = row_index * self.tile_size - cam_y

                if tile == 1:
                    surface.blit(self.wall, (x, y))
                elif tile == 0:
                    surface.blit(self.floor, (x, y))
                elif tile == 2:
                    surface.blit(self.grass, (x, y))
                elif tile == 3:
                    surface.blit(self.roof, (x, y))

    def collision(self, rect):
        for row_index, row in enumerate(self.map):
            for column_index, tile in enumerate(row):
                x = column_index * self.tile_size
                y = row_index * self.tile_size

                if tile == 1:
                    if rect.colliderect(pg.Rect(x, y, self.tile_size, self.tile_size)):
                        return True
        return False

    def render_lighting(self, surface, camera, player):
        cam_x, cam_y = camera.get_position()
        
        darkness = pg.Surface((config.WIDTH, config.HEIGHT), pg.SRCALPHA)
        darkness.fill((0, 0, 0, 220))
        
        light_layer = pg.Surface((config.WIDTH, config.HEIGHT), pg.SRCALPHA)
        
        for pos in self.light_positions:
            screen_x = pos[0] - cam_x - 150
            screen_y = pos[1] - cam_y - 150
            light_layer.blit(self.light_mask, (screen_x, screen_y))
        
        player_x = player.rect.centerx - cam_x - 180
        player_y = player.rect.centery - cam_y - 180
        light_layer.blit(self.player_light_mask, (player_x, player_y))
        
        darkness.blit(light_layer, (0, 0), special_flags=pg.BLEND_RGBA_SUB)
        
        surface.blit(darkness, (0, 0))
