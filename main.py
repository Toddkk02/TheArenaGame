#!/usr/bin/env python3
import config
import pygame as pg
import player 
import enemy
import map
import random
def initialize_game():
# initialize pygamepg
    pg.init()
    # set up display
    screen = pg.display.set_mode((config.WIDTH, config.HEIGHT))
    pg.display.set_caption(config.TITLE)
    clock = pg.time.Clock() 
    return screen, clock

def initialize_player():
    # create player instance
    player_instance = player.Player(config.DIMENSION_PLAYER, config.DIMENSION_PLAYER) # starting position  
    return player_instance, player_instance.update, player_instance.draw


def initialize_enemies(num_enemies=5):
    enemies = []
    for _ in range(num_enemies):
        x = random.randint(0, config.WIDTH - config.DIMENSION_ENEMY)
        y = random.randint(0, config.HEIGHT - config.DIMENSION_ENEMY)
        enemies.append(enemy.Enemy(x, y))
    return enemies

def main():
    screen, clock = initialize_game()
    player_instance, update_player, draw_player = initialize_player()
    player_instance.set_position(100, 100) # set player position to starting position
    enemies = initialize_enemies(5)
    game_map = map.Map()
    
    running = True
    while running:
        clock.tick(config.FPS)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False 
        for e in enemies:
                e.update(player_instance, game_map)
                e.raycast(player_instance, screen)
        
        game_map.draw(screen) 
        for e in enemies:
            e.draw(screen)
        k_pressed = pg.key.get_pressed()
        update_player(k_pressed, game_map)

        
        draw_player(None, screen) # draw player
        pg.display.flip() # update display
             

if __name__ == "__main__":
    main()
