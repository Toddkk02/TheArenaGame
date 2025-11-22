
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
        # Casa in alto a sinistra (interno)
        (280, 280),
        
        # Casa grande in alto centro (interno grande)
        (1176, 280),
        (1344, 336),
        
        # Casa in alto a destra (interno)
        (1960, 280),
        
        # Casa centro-sinistra 
        (672, 672),
        (728, 728),
        
        # Casa centro-destra
        (1680, 672),
        
        # Casetta centrale piccola
        (1176, 1008),
        
        # Casa grande in basso a sinistra
        (280, 1344),
        (392, 1400),
        
        # Casa grande in basso a destra
        (2016, 1344),
        (2128, 1400),
        
        # Pattuglie esterne (corridoi)
        (504, 504),      # corridoio nord-ovest
        (1400, 896),     # centro mappa
        (2240, 560),     # corridoio est
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
        mouse_pos = pg.mouse.get_pos()
        update_player(k_pressed, game_map, mouse_pos, camera_x, camera_y)
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

        game_map.render_lighting(screen, camera, player_instance)
        pg.display.flip()

if __name__ == "__main__":
    main()

