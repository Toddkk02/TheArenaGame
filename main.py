
#!/usr/bin/env python3
import config
import pygame as pg
import player 
import enemy
import map

def initialize_game():
    pg.init()
    screen = pg.display.set_mode((config.WIDTH, config.HEIGHT))
    pg.display.set_caption(config.TITLE)
    clock = pg.time.Clock() 
    return screen, clock

def initialize_player():
    player_instance = player.Player(config.DIMENSION_PLAYER, config.DIMENSION_PLAYER)
    return player_instance, player_instance.update, player_instance.draw

def initialize_enemies():
    enemies = []
    enemy_positions = [
        (174, 734),
        (1452, 739),
        (1398, 116),
        (287, 378),
        (1274, 388)
    ]
    for x, y in enemy_positions:
        enemies.append(enemy.Enemy(x, y))
    return enemies

def main():
    screen, clock = initialize_game()
    player_instance, update_player, draw_player = initialize_player()
    player_instance.set_position()
    enemies = initialize_enemies()
    game_map = map.Map()
    
    running = True
    #Timer for shot
    shot_timer = 0
    
    
    while running:
        clock.tick(config.FPS)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:   
                shot_timer = 3
        for e in enemies:
            e.update(player_instance, game_map)
                
        game_map.draw(screen) 
        for e in enemies:
            e.draw(screen)
        
        k_pressed = pg.key.get_pressed()
        update_player(k_pressed, game_map)
        
        draw_player(None, screen)
        if shot_timer > 0:
            player_instance.shoot(screen, enemies, shot_length=config.SHOT_LENGTH)
            shot_timer -= 1
        pg.display.flip()

if __name__ == "__main__":
    main()

