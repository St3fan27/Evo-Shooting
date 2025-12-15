class Button:
    def __init__(self, image, pos, text_input, font, base_color, hovering_color):
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)

        self.image = image
        if self.image is None:
            self.image = self.text
            self.has_background = False
        else:
            self.has_background = True

        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))
    
    def update(self, screen):
        if self.has_background:
            screen.blit(self.image, self.rect)
        
        screen.blit(self.text, self.text_rect)
    
    def checkForInput(self, position):
        if self.rect.collidepoint(position):
            return True
        return False
    
    def changeColor(self, position):
        if self.rect.collidepoint(position):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)

class MenuButton(Button):
    def __init__(self, image, pos, text_input, font, base_color, hovering_color):
        super().__init__(image, pos, text_input, font, base_color, hovering_color)
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos + 10))