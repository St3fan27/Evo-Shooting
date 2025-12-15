import pygame, sys
from pygame.locals import *
from button import Button, MenuButton

clock = pygame.time.Clock()

pygame.init()

WINDOW_SIZE = (1280, 720)
SCREEN = pygame.display.set_mode(WINDOW_SIZE)

BG = pygame.image.load("assets/craftpix-net-314143-free-industrial-zone-tileset-pixel-art/Background/Background.png")
BG = pygame.transform.scale(BG, (1280, 720))

BUTTON_IMAGE = pygame.image.load("assets/craftpix-net-894687-free-gui-for-cyberpunk-pixel-art/6 Buttons/1/1_04.png")

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
    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("black")

        PLAY_TEXT = get_font(45).render("This is the SINGLEPLAYER screen.", True, "White")
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