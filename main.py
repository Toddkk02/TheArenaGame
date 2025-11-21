
#!/usr/bin/env python3
import config
import pygame as pg
import player 
import enemy
import map
import game_over

def initialize_game():
    pg.init()
    screen = pg.display.set_mode((config.WIDTH, config.HEIGHT))
    pg.display.set_caption(config.TITLE)
    clock = pg.time.Clock() 
    return screen, clock

def initialize_player():
    player_instance = player.Player(config.DIMENSION_PLAYER, config.DIMENSION_PLAYER)
    return player_instance, player_instance.update, player_instance.draw

def initialize_camera(player_instance):
    x, y = player_instance.get_position()
    return player.Camera(x, y)


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
    camera = initialize_camera(player_instance)
    player_instance.set_position()
    enemies = initialize_enemies()
    game_map = map.Map()
    
    running = True
    #Timer for shot
    shot_timer = 0
    

    damage_number = []
    paused = False
    
    background = pg.image.load("./assets/background.png").convert()
    background = pg.transform.scale(background, (config.WIDTH, config.HEIGHT))


    while running:
        clock.tick(config.FPS)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    paused = not paused
            elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:   
                shot_timer = 3
        if paused:
            screen.blit(background, (0,0))
            font = pg.font.Font(None, 60)
            text = font.render("PAUSED", True, (0, 0,0))
            screen.blit(text, (config.WIDTH // 2 - text.get_width() // 2, config.HEIGHT // 2 - text.get_height() // 2))
            pg.display.flip()
            continue
        
        status = game_over.define_status_game(player_instance, enemies) #status of the game
        if status == config.GAME_STATUS[1]:
            running = False
            if status == config.GAME_STATUS[1]:
                game_over.show_game_over(screen)
                main()
                return
            continue
        camera_x, camera_y = camera.update(player_instance, game_map)
        game_map.draw(screen, camera_x, camera_y) 
        for e in enemies:
            e.update(player_instance, game_map)
         

        for e in enemies:
            e.draw(screen, camera_x, camera_y)
            e.attack_player(screen, player_instance, damage_number, camera_x, camera_y)        
        k_pressed = pg.key.get_pressed()
        update_player(k_pressed, game_map)
        paused = False
        status = game_over.define_status_game(player_instance, enemies) #status of the game 
        if status == config.GAME_STATUS[2]:
            continue
            
        draw_player(None, screen, camera_x, camera_y)
        if shot_timer > 0:
            player_instance.shoot(screen, enemies, config.SHOT_LENGTH, damage_number, camera_x, camera_y)
            shot_timer -= 1
        for dn in damage_number:
            dn.update()
            dn.draw(screen, camera_x, camera_y)

        damage_number[:] = [dn for dn in damage_number if not dn.is_dead()]

        pg.display.flip()

if __name__ == "__main__":
    main()

