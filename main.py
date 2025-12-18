import pygame, sys
from pygame.locals import *
from button import Button, MenuButton
from character import Punk, Cyborg, Biker

clock = pygame.time.Clock()

pygame.init()

WINDOW_SIZE = (1280, 720)
SCREEN = pygame.display.set_mode(WINDOW_SIZE)

BG = pygame.image.load("assets/craftpix-net-314143-free-industrial-zone-tileset-pixel-art/Background/Background.png")
BG = pygame.transform.scale(BG, (1280, 720))

BUTTON_IMAGE = pygame.image.load("assets/craftpix-net-894687-free-gui-for-cyberpunk-pixel-art/6 Buttons/1/1_04.png")

SURFACE = pygame.Surface((1280, 720), pygame.SRCALPHA)

def get_font(size): 
    return pygame.font.Font("assets/craftpix-net-894687-free-gui-for-cyberpunk-pixel-art/10 Font/CyberpunkCraftpixPixel.otf", size)

def main_menu():
    pygame.display.set_caption("MENU")

    while True:
        SCREEN.blit(BG, (0, 0))
        
        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center = (640, 100))

        SINGLEPLAYER_BUTTON = MenuButton(image = pygame.transform.scale(BUTTON_IMAGE, (700, 100)),
                                    pos = (640, 250),
                                    text_input = "SINGLEPLAYER",
                                    font = get_font(75),
                                    base_color = "#d7fcd4",
                                    hovering_color = "White")
        MULTYPLAYER_BUTTON = MenuButton(image = pygame.transform.scale(BUTTON_IMAGE, (660, 100)),
                                    pos = (640, 360),
                                    text_input = "MULTYPLAYER",
                                    font = get_font(75),
                                    base_color = "#d7fcd4",
                                    hovering_color = "White")
        OPTIONS_BUTTON = MenuButton(image = pygame.transform.scale(BUTTON_IMAGE, (400, 100)),
                                pos = (640, 470),
                                text_input = "OPTIONS",
                                font = get_font(75),
                                base_color = "#d7fcd4",
                                hovering_color = "White")
        QUIT_BUTTON = MenuButton(image = pygame.transform.scale(BUTTON_IMAGE, (220, 100)),
                            pos = (640, 580),
                            text_input = "QUIT",
                            font = get_font(75),
                            base_color = "#d7fcd4",
                            hovering_color = "White")

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

    player1 = Punk((200, 300), controls="WASD")
    player2 = Biker((1000, 300), controls="ARROWS") 

    players_group = pygame.sprite.Group() 
    players_group.add(player1)
    players_group.add(player2)

    resume_btn = MenuButton(image=pygame.transform.scale(BUTTON_IMAGE, (600, 100)), pos=(640, 250), 
                            text_input="RESUME", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
    restart_btn = MenuButton(image=pygame.transform.scale(BUTTON_IMAGE, (600, 100)), pos=(640, 370), 
                            text_input="RESTART", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
    exit_btn = MenuButton(image=pygame.transform.scale(BUTTON_IMAGE, (600, 100)), pos=(640, 490), 
                          text_input="MAIN MENU", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
    
    pause_buttons = [resume_btn, restart_btn, exit_btn]

    while True:
        clock.tick(60)
        SCREEN.fill("black") 
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        if not pause:
            players_group.update(WINDOW_SIZE)

        players_group.draw(SCREEN)

        if pause:
            pygame.draw.rect(SURFACE, (0, 0, 0, 150), [0, 0, 1280, 720])
            SCREEN.blit(SURFACE, (0, 0))
            
            for button in pause_buttons:
                button.changeColor(PLAY_MOUSE_POS)
                button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()                

            if event.type == pygame.MOUSEBUTTONDOWN:
                if pause:
                    if resume_btn.checkForInput(PLAY_MOUSE_POS):
                        pause = False
                    
                    if restart_btn.checkForInput(PLAY_MOUSE_POS):
                        player1.reset()
                        player2.reset()
                        pause = False
                        
                    if exit_btn.checkForInput(PLAY_MOUSE_POS):
                        return
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pause = not pause 

                if not pause:
                    if event.key == pygame.K_d: player1.moving_right = True
                    if event.key == pygame.K_a: player1.moving_left = True
                    if event.key == pygame.K_w: player1.jump()
                    
                    if event.key == pygame.K_RIGHT: player2.moving_right = True
                    if event.key == pygame.K_LEFT: player2.moving_left = True
                    if event.key == pygame.K_UP: player2.jump()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_d: player1.moving_right = False
                if event.key == pygame.K_a: player1.moving_left = False
                if event.key == pygame.K_RIGHT: player2.moving_right = False
                if event.key == pygame.K_LEFT: player2.moving_left = False

        pygame.display.update()

def multyplayer():
    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("black")

        PLAY_TEXT = get_font(45).render("This is the MULTYPLAYER screen.", True, "White")
        PLAY_RECT = PLAY_TEXT.get_rect(center=(640, 260))
        SCREEN.blit(PLAY_TEXT, PLAY_RECT)

        PLAY_BACK = Button(image=None, pos=(640, 460), 
                            text_input="BACK", font=get_font(75), base_color="White", hovering_color="Green")

        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    main_menu()

        pygame.display.update()

def options():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("white")

        OPTIONS_TEXT = get_font(45).render("This is the OPTIONS screen.", True, "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 260))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_BACK = Button(image=None, pos=(640, 460), 
                            text_input="BACK", font=get_font(75), base_color="Black", hovering_color="Green")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()

        pygame.display.update()

main_menu()


