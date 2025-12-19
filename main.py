import pygame, sys
from pygame.locals import *
from button import Button, MenuButton
from character import Punk, Cyborg, Biker
from bullet import Bullet
from tile import Tile

clock = pygame.time.Clock()
pygame.init()

WINDOW_SIZE = (1280, 720)
SCREEN = pygame.display.set_mode(WINDOW_SIZE)

BG = pygame.image.load("assets/craftpix-net-314143-free-industrial-zone-tileset-pixel-art/Background/Background.png")
BG = pygame.transform.scale(BG, (1280, 720))
BUTTON_IMAGE = pygame.image.load("assets/craftpix-net-894687-free-gui-for-cyberpunk-pixel-art/6 Buttons/1/1_04.png")

SURFACE = pygame.Surface((1280, 720), pygame.SRCALPHA)
SURFACE.fill((0, 0, 0, 150))

def get_font(size): 
    return pygame.font.Font("assets/craftpix-net-894687-free-gui-for-cyberpunk-pixel-art/10 Font/CyberpunkCraftpixPixel.otf", size)

def main_menu():
    pygame.display.set_caption("MENU")
    while True:
        SCREEN.blit(BG, (0, 0))
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        MENU_TEXT = get_font(100).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center = (640, 100))

        SINGLEPLAYER_BUTTON = MenuButton(image=pygame.transform.scale(BUTTON_IMAGE, (700, 100)), pos=(640, 250), 
                            text_input="SINGLEPLAYER", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        MULTYPLAYER_BUTTON = MenuButton(image=pygame.transform.scale(BUTTON_IMAGE, (660, 100)), pos=(640, 360), 
                            text_input="MULTYPLAYER", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        OPTIONS_BUTTON = MenuButton(image=pygame.transform.scale(BUTTON_IMAGE, (400, 100)), pos=(640, 470), 
                            text_input="OPTIONS", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = MenuButton(image=pygame.transform.scale(BUTTON_IMAGE, (220, 100)), pos=(640, 580), 
                            text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)
        for button in [SINGLEPLAYER_BUTTON, MULTYPLAYER_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if SINGLEPLAYER_BUTTON.checkForInput(MENU_MOUSE_POS):
                    singleplayer()
                if MULTYPLAYER_BUTTON.checkForInput(MENU_MOUSE_POS):
                    multyplayer()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()
        pygame.display.update()

def singleplayer():
    pause = False
    game_over = False
    outcome_text = ""
    outcome_color = "White"
    
    tiles_group = pygame.sprite.Group()
    tile_size = 40 
    
    map_data = [
        "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX", 
        "X                              X",
        "X                              X",
        "X                              X",
        "X           PPPPPPPPPPP        X", 
        "X                              X",
        "X                              X",
        "X      PP            PP        X", 
        "X                              X",
        "X             PPXPP            X", 
        "X               X              X",
        "X               X              X",
        "X      PPPP     X     PPPP     X",
        "X                              X",
        "X                              X",
        "X                              X",
        "X                              X", 
        "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX", 
    ]
 
    for row_index, row in enumerate(map_data):
        for col_index, cell in enumerate(row):
            x = col_index * tile_size
            y = row_index * tile_size
            
            if cell == 'X':
                tile = Tile((x, y), tile_size, 'wall')
                tiles_group.add(tile)
            elif cell == 'P':
                tile = Tile((x, y), tile_size, 'platform')
                tiles_group.add(tile)

    player1 = Punk((100, 500), controls="WASD")
    player2 = Biker((1100, 500), controls="ARROWS") 
    
    players_group = pygame.sprite.Group() 
    players_group.add(player1)
    players_group.add(player2)

    bullet_group = pygame.sprite.Group()

    ammo_font = get_font(20) 
    victory_font = get_font(100)

    resume_btn = MenuButton(image=pygame.transform.scale(BUTTON_IMAGE, (600, 100)), pos=(640, 250), 
                            text_input="RESUME", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
    restart_btn = MenuButton(image=pygame.transform.scale(BUTTON_IMAGE, (600, 100)), pos=(640, 370), 
                            text_input="RESTART", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
    exit_btn = MenuButton(image=pygame.transform.scale(BUTTON_IMAGE, (600, 100)), pos=(640, 490), 
                          text_input="MAIN MENU", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
    pause_buttons = [resume_btn, restart_btn, exit_btn]

    play_again_btn = MenuButton(image=pygame.transform.scale(BUTTON_IMAGE, (600, 100)), pos=(640, 350), 
                            text_input="PLAY AGAIN", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
    game_over_exit_btn = MenuButton(image=pygame.transform.scale(BUTTON_IMAGE, (600, 100)), pos=(640, 470), 
                          text_input="MAIN MENU", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
    game_over_buttons = [play_again_btn, game_over_exit_btn]

    while True:
        clock.tick(60)
        SCREEN.fill("black") 
        SCREEN.blit(BG, (0,0)) 
        
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        if not pause and not game_over:
            players_group.update(tiles_group, 720)
            bullet_group.update(1280)

            hits_wall = pygame.sprite.groupcollide(bullet_group, tiles_group, False, False)
            for bullet, tiles in hits_wall.items():
                for tile in tiles:
                    if tile.type == 'wall':
                        bullet.kill()

            for bullet in bullet_group:
                hit_players = pygame.sprite.spritecollide(bullet, players_group, False)
                for player in hit_players:
                    if player != bullet.owner and player.alive:
                        player.take_damage(10)
                        bullet.kill()
            
            if not player1.alive and not player2.alive:
                game_over = True
                outcome_text = "DRAW!"
                outcome_color = "Gray"
            elif not player1.alive:
                game_over = True
                outcome_text = "PLAYER 2 WINS!"
                outcome_color = "#b68f40" 
            elif not player2.alive:
                game_over = True
                outcome_text = "PLAYER 1 WINS!"
                outcome_color = "#b68f40"

        tiles_group.draw(SCREEN)
        bullet_group.draw(SCREEN)
        
        for player in players_group:
            player.draw(SCREEN)
            pygame.draw.rect(SCREEN, "red", (player.rect.x, player.rect.y - 20, player.rect.width, 5))
            current_health_width = (player.health / 100) * player.rect.width
            pygame.draw.rect(SCREEN, "green", (player.rect.x, player.rect.y - 20, current_health_width, 5))
            ammo_text = ammo_font.render(f"{player.ammo}/15", True, "White")
            SCREEN.blit(ammo_text, (player.rect.x, player.rect.y - 40))

        if game_over:
            SCREEN.blit(SURFACE, (0, 0)) 
            
            outcome_surf = victory_font.render(outcome_text, True, outcome_color)
            outcome_rect = outcome_surf.get_rect(center=(640, 150))
            SCREEN.blit(outcome_surf, outcome_rect)

            for button in game_over_buttons:
                button.changeColor(PLAY_MOUSE_POS)
                button.update(SCREEN)

        elif pause:
            SCREEN.blit(SURFACE, (0, 0)) 
            for button in pause_buttons:
                button.changeColor(PLAY_MOUSE_POS)
                button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()                

            if event.type == pygame.MOUSEBUTTONDOWN:
                if game_over:
                    if play_again_btn.checkForInput(PLAY_MOUSE_POS):
                        player1.reset()
                        player2.reset()
                        bullet_group.empty()
                        players_group.add(player1) 
                        players_group.add(player2)
                        game_over = False
                    
                    if game_over_exit_btn.checkForInput(PLAY_MOUSE_POS):
                        return 
                
                elif pause:
                    if resume_btn.checkForInput(PLAY_MOUSE_POS):
                        pause = False
                    if restart_btn.checkForInput(PLAY_MOUSE_POS):
                        player1.reset()
                        player2.reset()
                        bullet_group.empty() 
                        players_group.add(player1)
                        players_group.add(player2)
                        pause = False
                    if exit_btn.checkForInput(PLAY_MOUSE_POS):
                        return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE and not game_over:
                    pause = not pause 

                if not pause and not game_over:
                    if player1.alive:
                        if event.key == pygame.K_d: player1.moving_right = True
                        if event.key == pygame.K_a: player1.moving_left = True
                        if event.key == pygame.K_w: player1.jump()
                        if event.key == pygame.K_SPACE:
                            if player1.ammo > 0: 
                                facing = 1 if player1.facing_right else -1
                                bullet = Bullet(player1.rect.centerx, player1.rect.centery, facing, player1)
                                bullet_group.add(bullet)
                                player1.ammo -= 1 
                        if event.key == pygame.K_v:
                            player1.attack()
                            player1.deal_melee_damage(player2)

                    if player2.alive:
                        if event.key == pygame.K_RIGHT: player2.moving_right = True
                        if event.key == pygame.K_LEFT: player2.moving_left = True
                        if event.key == pygame.K_UP: player2.jump()
                        if event.key == pygame.K_m: 
                            if player2.ammo > 0: 
                                facing = 1 if player2.facing_right else -1
                                bullet = Bullet(player2.rect.centerx, player2.rect.centery, facing, player2)
                                bullet_group.add(bullet)
                                player2.ammo -= 1 
                        if event.key == pygame.K_n:
                            player2.attack()
                            player2.deal_melee_damage(player1)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_d: player1.moving_right = False
                if event.key == pygame.K_a: player1.moving_left = False
                if event.key == pygame.K_RIGHT: player2.moving_right = False
                if event.key == pygame.K_LEFT: player2.moving_left = False

        pygame.display.update()

def multyplayer(): pass
def options(): pass

main_menu()