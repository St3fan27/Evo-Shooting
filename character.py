import pygame
from pygame.math import Vector2

class Character(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        
        self.animations = {'idle': [], 'run': [], 'jump': []}
        
        self.import_character_assets()
        
        self.frame_index = 0
        self.animation_speed = 0.15 
        
        if self.animations['idle']:
            self.image = self.animations['idle'][self.frame_index]
        else:
            self.image = pygame.Surface((32, 32))
            
        self.rect = self.image.get_rect(topleft = pos)

        self.position = Vector2(pos) 
        self.velocity = Vector2(0, 0)
        self.acceleration = 0.5   
        self.speed = 4            
        self.jump_power = -12     

        self.facing_right = True
        self.on_ground = False
        self.state = 'idle'     
        
        self.moving_right = False
        self.moving_left = False

    def load_frames(self, path, frame_count):
        try:
            sheet = pygame.image.load(path).convert_alpha()
            frames = []
            width = sheet.get_width() // frame_count
            height = sheet.get_height()
            
            for i in range(frame_count):
                frame = sheet.subsurface((i * width, 0, width, height))
                frames.append(frame)
            return frames
        except FileNotFoundError:
            print(f"EROARE: Nu am gasit imaginea: {path}")
            return [pygame.Surface((32,32))] 

    def import_character_assets(self):
        pass 

    def animate(self):
        animation = self.animations[self.state]
        self.frame_index += self.animation_speed

        if self.frame_index >= len(animation):
            self.frame_index = 0

        current_frame_idx = int(self.frame_index) % len(animation)
        image = animation[current_frame_idx]

        if self.facing_right:
            self.image = image
        else:
            self.image = pygame.transform.flip(image, True, False)

    def get_status(self):
        if self.velocity.y != 0 and not self.on_ground:
            self.state = 'jump'
        elif self.velocity.x != 0:
            self.state = 'run'
        else:
            self.state = 'idle'

    def get_input(self):
        self.velocity.x = 0 
        if self.moving_right:
            self.velocity.x = self.speed
            self.facing_right = True
        if self.moving_left:
            self.velocity.x = -self.speed
            self.facing_right = False

    def jump(self):
        if self.on_ground:
            self.velocity.y = self.jump_power
            self.on_ground = False

    def apply_gravity(self):
        self.velocity.y += self.acceleration

    def update(self, window_size):
        self.get_input()
        self.get_status() 
        self.animate()    
        self.apply_gravity()
        self.position += self.velocity
        
        ground_offset = 0 
        ground_level = window_size[1] - self.image.get_height() + ground_offset
        
        if self.position.y >= ground_level:
            self.position.y = ground_level
            self.velocity.y = 0 
            self.on_ground = True  
        else:
            self.on_ground = False
            
        self.rect.topleft = self.position


class Biker(Character):
    def import_character_assets(self):
        path_idle = "assets/craftpix-net-856554-free-3-cyberpunk-characters-pixel-art/1 Biker/Biker_idle.png" 
        path_run = "assets/craftpix-net-856554-free-3-cyberpunk-characters-pixel-art/1 Biker/Biker_run.png"  
        path_jump = "assets/craftpix-net-856554-free-3-cyberpunk-characters-pixel-art/1 Biker/Biker_jump.png" 
        
        self.animations['idle'] = self.load_frames(path_idle, 4) 
        self.animations['run'] = self.load_frames(path_run, 6) 
        self.animations['jump'] = self.load_frames(path_jump, 4)

class Punk(Character):
    def import_character_assets(self):
        path_idle = "assets/craftpix-net-856554-free-3-cyberpunk-characters-pixel-art/2 Punk/Punk_idle.png" 
        path_run = "assets/craftpix-net-856554-free-3-cyberpunk-characters-pixel-art/2 Punk/Punk_run.png"  
        path_jump = "assets/craftpix-net-856554-free-3-cyberpunk-characters-pixel-art/2 Punk/Punk_jump.png" 
        
        self.animations['idle'] = self.load_frames(path_idle, 4) 
        self.animations['run'] = self.load_frames(path_run, 6) 
        self.animations['jump'] = self.load_frames(path_jump, 4)


class Cyborg(Character):
    def import_character_assets(self):
        path_idle = "assets/craftpix-net-856554-free-3-cyberpunk-characters-pixel-art/3 Cyborg/Cyborg_idle.png" 
        path_run = "assets/craftpix-net-856554-free-3-cyberpunk-characters-pixel-art/3 Cyborg/Cyborg_run.png"  
        path_jump = "assets/craftpix-net-856554-free-3-cyberpunk-characters-pixel-art/3 Cyborg/Cyborg_jump.png" 
        
        self.animations['idle'] = self.load_frames(path_idle, 4) 
        self.animations['run'] = self.load_frames(path_run, 6) 
        self.animations['jump'] = self.load_frames(path_jump, 4)


