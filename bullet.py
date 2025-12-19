import pygame

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, owner):
        super().__init__()
        
        self.direction = direction 
        self.owner = owner
        self.speed = 15

        image_path = "assets/craftpix-net-730561-free-guns-for-cyberpunk-characters-pixel-art/5 Bullets/1.png"
        
        try:
            raw_image = pygame.image.load(image_path).convert_alpha()
            self.image = pygame.transform.scale(raw_image, (20, 10))
            
            if self.direction == -1:
                self.image = pygame.transform.flip(self.image, True, False)
                
        except FileNotFoundError:
            print("Eroare: Nu am gasit imaginea glontului.")
            self.image = pygame.Surface((10, 5))
            self.image.fill("yellow")
        
        self.rect = self.image.get_rect(center=(x, y))
        
    def update(self, screen_width):
        self.rect.x += self.direction * self.speed
        
        if self.rect.right < 0 or self.rect.left > screen_width:
            self.kill()