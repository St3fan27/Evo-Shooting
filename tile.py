import pygame

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, size, tile_type):
        super().__init__()
        self.type = tile_type 
        
        base_path = "assets/craftpix-net-314143-free-industrial-zone-tileset-pixel-art/1 Tiles/"
        
        if self.type == 'platform':
            image_path = base_path + "IndustrialTile_18.png"
        else:
            image_path = base_path + "IndustrialTile_14.png"
        
        try:
            full_image = pygame.image.load(image_path).convert_alpha()
            
            if self.type == 'platform':
                self.image = pygame.transform.scale(full_image, (size, 15)) 
            else:
                self.image = pygame.transform.scale(full_image, (size, size))
                
        except FileNotFoundError:
            print(f"EROARE: Nu am gasit imaginea: {image_path}")
            if self.type == 'platform':
                self.image = pygame.Surface((size, 15))
                self.image.fill('blue')
            else:
                self.image = pygame.Surface((size, size))
                self.image.fill('grey')
            
        self.rect = self.image.get_rect(topleft=pos)