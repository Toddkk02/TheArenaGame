import pygame as pg 
import config


def define_status_game(player, enemies):
    if player.dead:
        return config.GAME_STATUS[1]
    elif len(enemies) == 0:
        return config.GAME_STATUS[0]
    elif pg.key.get_pressed()[pg.K_ESCAPE]:
        return config.GAME_STATUS[2]

def show_game_over(screen):
    background_image = pg.image.load("./assets/background.png").convert()
    background_image = pg.transform.scale(background_image, (config.WIDTH, config.HEIGHT))
    screen.blit(background_image, (0, 0))
    font = pg.font.Font(None, 30).render("Game Over", True, (0, 0, 0))
    text = font.get_rect(center=(config.WIDTH // 2, config.HEIGHT // 2))
    button_play_again = pg.font.Font(None, 30).render("Play Again", True, (0, 0, 0))
    button_play_again_rect = button_play_again.get_rect(center=(config.WIDTH // 2, config.HEIGHT // 2 + 50))
    screen.blit(font, text)
    screen.blit(button_play_again, button_play_again_rect)
    pg.display.flip()

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                x, y = pg.mouse.get_pos()
                if button_play_again_rect.collidepoint(x, y):
                    return

