import pygame
from pygame.math import Vector2

class Character(pygame.sprite.Sprite):
    def __init__(self, pos, controls="WASD"):
        super().__init__()
        self.controls = controls 
        self.start_pos = pos
        
        self.anim_gun = {'idle': [], 'run': [], 'jump': [], 'attack': []}      
        self.anim_no_gun = {'idle': [], 'run': [], 'jump': [], 'attack': []}   
        self.animations = self.anim_gun 

        self.gun_image = None
        self.hand_image = None
        self.back_arm_image = None
        
        self.import_character_assets()
        
        self.frame_index = 0
        self.animation_speed = 0.15 
        
        if self.anim_gun['idle']:
            self.image = self.anim_gun['idle'][0]
        else:
            self.image = pygame.Surface((32, 32))
            
        self.rect = self.image.get_rect(topleft = pos)
        midbottom = self.rect.midbottom
        
        self.rect.width = 20  
        self.rect.height = self.image.get_height() - 20 
        self.rect.midbottom = midbottom

        self.direction = Vector2(0, 0)
        self.velocity = Vector2(0, 0)
        self.position = Vector2(pos)
        self.acceleration = 0.5   
        self.speed = 5       
        self.jump_power = -14
        
        self.health = 100 
        self.alive = True
        self.max_ammo = 15     
        self.ammo = 15         

        self.is_attacking = False
        self.attack_cooldown = 0

        if self.controls == "ARROWS":
            self.facing_right = False
        else:
            self.facing_right = True
            
        self.on_ground = False
        self.state = 'idle'     
        self.moving_right = False
        self.moving_left = False
        self.dropping_down = False 
        self.damage_dealt = False

    def load_frames(self, path, frame_count):
        try:
            sheet = pygame.image.load(path).convert_alpha()
            frames = []
            width = sheet.get_width() // frame_count
            height = sheet.get_height()
            
            for i in range(frame_count):
                frame = sheet.subsurface((i * width, 0, width, height))
                new_size = (width * 1.5, height * 1.5)
                scaled_frame = pygame.transform.scale(frame, new_size)
                frames.append(scaled_frame)
            return frames
        except FileNotFoundError:
            print(f"EROARE: Nu am gasit imaginea: {path}")
            return [pygame.Surface((32,32))]

    def import_character_assets(self):
        pass 

    def animate(self):
        if self.ammo > 0:
            self.animations = self.anim_gun
        else:
            self.animations = self.anim_no_gun

        if self.state == 'attack':
            if self.anim_no_gun['attack']:
                self.animations = self.anim_no_gun

        if self.state not in self.animations or not self.animations[self.state]:
            return 
        
        animation = self.animations[self.state]
        self.frame_index += self.animation_speed
        
        if self.frame_index >= len(animation):
            if self.state == 'attack':
                self.is_attacking = False
                self.state = 'idle' 
            self.frame_index = 0
            
        current_frame_idx = int(self.frame_index) % len(animation)
        image = animation[current_frame_idx]
        
        if self.facing_right:
            self.image = image
        else:
            self.image = pygame.transform.flip(image, True, False)

    def get_status(self):
        if self.is_attacking:
            self.state = 'attack'
        else:
            if self.velocity.y < 0:
                self.state = 'jump'
            elif self.velocity.y > 1:
                self.state = 'jump' 
            elif self.direction.x != 0:
                self.state = 'run'
            else:
                self.state = 'idle'

    def get_input(self):
        self.direction.x = 0 
        self.dropping_down = False 
        
        keys = pygame.key.get_pressed()

        if self.controls == "WASD":
            if self.moving_right:
                self.direction.x = 1
                self.facing_right = True
            if self.moving_left:
                self.direction.x = -1
                self.facing_right = False
            if keys[pygame.K_s]:
                self.dropping_down = True
            
            if keys[pygame.K_v] and not self.is_attacking:
                self.attack()

        if self.controls == "ARROWS":
            if self.moving_right:
                self.direction.x = 1
                self.facing_right = True
            if self.moving_left:
                self.direction.x = -1
                self.facing_right = False
            if keys[pygame.K_DOWN]:
                self.dropping_down = True
            
            if keys[pygame.K_n] and not self.is_attacking:
                self.attack()

    def attack(self):
        if self.is_attacking:
            return

        self.is_attacking = True
        self.damage_dealt = False 
        self.frame_index = 0
        self.state = 'attack'

    def deal_melee_damage(self, target):
        if not self.is_attacking or self.damage_dealt:
            return

        attack_range = 15
        hit = False
        
        if self.facing_right:
            if self.rect.right < target.rect.left < self.rect.right + attack_range:
                hit = True
        else:
            if self.rect.left - attack_range < target.rect.right < self.rect.left:
                hit = True
                
        if hit and abs(self.rect.centery - target.rect.centery) < 50:
            target.take_damage(5)
            self.damage_dealt = True

    def jump(self):
        if self.on_ground:
            self.velocity.y = self.jump_power
            self.on_ground = False

    def apply_gravity(self):
        self.velocity.y += self.acceleration

    def out_of_bounds(self):
        self.health = 0
        self.alive = False
        self.kill()

    def update(self, tiles_group, window_height):
        self.get_input()
        self.get_status()
        self.animate()
        
        self.rect.x += self.direction.x * self.speed
        self.collision_horizontal(tiles_group)
        
        self.apply_gravity()
        
        self.rect.y += self.velocity.y
        self.collision_vertical(tiles_group)

        if self.rect.top > window_height:
            self.out_of_bounds()

    def draw(self, surface):
        body_draw_rect = self.image.get_rect()
        body_draw_rect.midbottom = self.rect.midbottom
        
        body_offset_x = 15 
        if self.facing_right:
            body_draw_rect.centerx += body_offset_x
        else:
            body_draw_rect.centerx -= body_offset_x

        if self.ammo > 0 and self.gun_image and self.hand_image and self.back_arm_image and self.alive and not self.is_attacking:
            
            gun_offset_x = 8   
            gun_offset_y = 5   
            hand_rel_x = -18   
            hand_rel_y = 4     
            back_arm_offset_x = -24
            back_arm_offset_y = 6  

            if self.state == 'run':
                gun_offset_y = 5
                back_arm_offset_x = -16
                back_arm_offset_y = 4

            elif self.state == 'jump':
                gun_offset_y = 0       
                back_arm_offset_x = -16
                back_arm_offset_y = 4

            current_gun = self.gun_image.copy()
            current_hand = self.hand_image.copy()
            current_back_arm = self.back_arm_image.copy()
            
            gun_center = (body_draw_rect.centerx, body_draw_rect.centery + gun_offset_y)
            back_arm_center = (body_draw_rect.centerx, body_draw_rect.centery + back_arm_offset_y)

            if self.facing_right:
                gun_rect = current_gun.get_rect(center=(gun_center[0] + gun_offset_x, gun_center[1]))
                hand_rect = current_hand.get_rect(center=(gun_center[0] + gun_offset_x + hand_rel_x, gun_center[1] + hand_rel_y))
                back_arm_rect = current_back_arm.get_rect(center=(back_arm_center[0] + back_arm_offset_x, back_arm_center[1]))
            else:
                current_gun = pygame.transform.flip(current_gun, True, False)
                current_hand = pygame.transform.flip(current_hand, True, False)
                current_back_arm = pygame.transform.flip(current_back_arm, True, False)
                
                gun_rect = current_gun.get_rect(center=(gun_center[0] - gun_offset_x, gun_center[1]))
                hand_rect = current_hand.get_rect(center=(gun_center[0] - gun_offset_x - hand_rel_x, gun_center[1] + hand_rel_y))
                back_arm_rect = current_back_arm.get_rect(center=(back_arm_center[0] - back_arm_offset_x, back_arm_center[1]))

            surface.blit(current_hand, hand_rect)
            surface.blit(self.image, body_draw_rect)
            surface.blit(current_back_arm, back_arm_rect)
            surface.blit(current_gun, gun_rect)
        else:
            surface.blit(self.image, body_draw_rect)

        # pygame.draw.rect(surface, "red", self.rect, 1)

    def collision_horizontal(self, tiles):
        for tile in tiles:
            if tile.type == 'wall' and tile.rect.colliderect(self.rect):
                if self.direction.x > 0:
                    self.rect.right = tile.rect.left
                elif self.direction.x < 0:
                    self.rect.left = tile.rect.right

    def collision_vertical(self, tiles):
        self.on_ground = False 
        
        for tile in tiles:
            if tile.rect.colliderect(self.rect):
                if tile.type == 'wall':
                    if self.velocity.y > 0:
                        self.rect.bottom = tile.rect.top
                        self.velocity.y = 0
                        self.on_ground = True
                    elif self.velocity.y < 0:
                        self.rect.top = tile.rect.bottom
                        self.velocity.y = 0
                elif tile.type == 'platform':
                    if self.velocity.y > 0 and not self.dropping_down:
                        if self.rect.bottom <= tile.rect.bottom + 5:
                             if self.rect.bottom - self.velocity.y <= tile.rect.top + 5: 
                                self.rect.bottom = tile.rect.top
                                self.velocity.y = 0
                                self.on_ground = True
        
        if not self.on_ground and self.velocity.y >= 0:
            check_rect = self.rect.copy()
            check_rect.y += 1
            for tile in tiles:
                if tile.rect.colliderect(check_rect):
                    if tile.type == 'wall':
                        self.on_ground = True
                    elif tile.type == 'platform' and not self.dropping_down:
                        if self.rect.bottom <= tile.rect.bottom:
                            self.on_ground = True
                    if self.on_ground: break

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.health = 0
            self.alive = False
            self.kill() 

    def reset(self):
        self.rect.topleft = self.start_pos
        midbottom = self.rect.midbottom
        self.rect.width = 20
        self.rect.height = self.image.get_height() - 20
        self.rect.midbottom = midbottom
        
        self.velocity = Vector2(0, 0)
        self.direction = Vector2(0, 0)
        self.state = 'idle'
        
        self.health = 100
        self.ammo = self.max_ammo
        self.alive = True
        self.is_attacking = False
        
        self.animations = self.anim_gun

class Biker(Character):
    def import_character_assets(self):
        base_path = "assets/craftpix-net-730561-free-guns-for-cyberpunk-characters-pixel-art/1 Characters/1 Biker/"
        gun_path = "assets/craftpix-net-730561-free-guns-for-cyberpunk-characters-pixel-art/2 Guns/1_1.png"
        hand_holding_path = "assets/craftpix-net-730561-free-guns-for-cyberpunk-characters-pixel-art/3 Hands/1 Biker/3.png"
        back_arm_path = "assets/craftpix-net-730561-free-guns-for-cyberpunk-characters-pixel-art/3 Hands/1 Biker/1.png"
        
        attack_path = "assets/craftpix-net-856554-free-3-cyberpunk-characters-pixel-art/1 Biker/Biker_attack1.png"

        self.anim_gun['idle'] = self.load_frames(base_path + "Idle2.png", 4) 
        self.anim_gun['run'] = self.load_frames(base_path + "Run2.png", 6) 
        self.anim_gun['jump'] = self.load_frames(base_path + "Jump2.png", 4)

        self.anim_no_gun['idle'] = self.load_frames(base_path + "Idle1.png", 4) 
        self.anim_no_gun['run'] = self.load_frames(base_path + "Run1.png", 6) 
        self.anim_no_gun['jump'] = self.load_frames(base_path + "Jump1.png", 4)
        
        self.anim_no_gun['attack'] = self.load_frames(attack_path, 6)
        self.anim_gun['attack'] = self.load_frames(attack_path, 6)
        
        try:
            self.gun_image = pygame.image.load(gun_path).convert_alpha()
            self.gun_image = pygame.transform.scale(self.gun_image, (int(self.gun_image.get_width()*1.5), int(self.gun_image.get_height()*1.5)))
            
            self.hand_image = pygame.image.load(hand_holding_path).convert_alpha()
            self.hand_image = pygame.transform.scale(self.hand_image, (int(self.hand_image.get_width()*1.5), int(self.hand_image.get_height()*1.5)))

            self.back_arm_image = pygame.image.load(back_arm_path).convert_alpha()
            self.back_arm_image = pygame.transform.scale(self.back_arm_image, (int(self.back_arm_image.get_width()*1.5), int(self.back_arm_image.get_height()*1.5)))
        except FileNotFoundError: pass

class Punk(Character):
    def import_character_assets(self):
        base_path = "assets/craftpix-net-730561-free-guns-for-cyberpunk-characters-pixel-art/1 Characters/2 Punk/"
        gun_path = "assets/craftpix-net-730561-free-guns-for-cyberpunk-characters-pixel-art/2 Guns/1_1.png"
        hand_holding_path = "assets/craftpix-net-730561-free-guns-for-cyberpunk-characters-pixel-art/3 Hands/2 Punk/3.png"
        back_arm_path = "assets/craftpix-net-730561-free-guns-for-cyberpunk-characters-pixel-art/3 Hands/2 Punk/1.png"
        
        attack_path = "assets/craftpix-net-856554-free-3-cyberpunk-characters-pixel-art/2 Punk/Punk_attack1.png"

        self.anim_gun['idle'] = self.load_frames(base_path + "Idle2.png", 4) 
        self.anim_gun['run'] = self.load_frames(base_path + "Run2.png", 6) 
        self.anim_gun['jump'] = self.load_frames(base_path + "Jump2.png", 4)

        self.anim_no_gun['idle'] = self.load_frames(base_path + "Idle1.png", 4) 
        self.anim_no_gun['run'] = self.load_frames(base_path + "Run1.png", 6) 
        self.anim_no_gun['jump'] = self.load_frames(base_path + "Jump1.png", 4)
        
        self.anim_no_gun['attack'] = self.load_frames(attack_path, 6)
        self.anim_gun['attack'] = self.load_frames(attack_path, 6)
        
        try:
            self.gun_image = pygame.image.load(gun_path).convert_alpha()
            self.gun_image = pygame.transform.scale(self.gun_image, (int(self.gun_image.get_width()*1.5), int(self.gun_image.get_height()*1.5)))
            
            self.hand_image = pygame.image.load(hand_holding_path).convert_alpha()
            self.hand_image = pygame.transform.scale(self.hand_image, (int(self.hand_image.get_width()*1.5), int(self.hand_image.get_height()*1.5)))

            self.back_arm_image = pygame.image.load(back_arm_path).convert_alpha()
            self.back_arm_image = pygame.transform.scale(self.back_arm_image, (int(self.back_arm_image.get_width()*1.5), int(self.back_arm_image.get_height()*1.5)))
        except FileNotFoundError: pass

class Cyborg(Character):
    def import_character_assets(self):
        base_path = "assets/craftpix-net-730561-free-guns-for-cyberpunk-characters-pixel-art/1 Characters/3 Cyborg/"
        gun_path = "assets/craftpix-net-730561-free-guns-for-cyberpunk-characters-pixel-art/2 Guns/1_1.png"
        hand_holding_path = "assets/craftpix-net-730561-free-guns-for-cyberpunk-characters-pixel-art/3 Hands/3 Cyborg/3.png"
        back_arm_path = "assets/craftpix-net-730561-free-guns-for-cyberpunk-characters-pixel-art/3 Hands/3 Cyborg/1.png"
        
        attack_path = "assets/craftpix-net-856554-free-3-cyberpunk-characters-pixel-art/3 Cyborg/Cyborg_attack1.png"

        self.anim_gun['idle'] = self.load_frames(base_path + "Idle2.png", 4) 
        self.anim_gun['run'] = self.load_frames(base_path + "Run2.png", 6) 
        self.anim_gun['jump'] = self.load_frames(base_path + "Jump2.png", 4)

        self.anim_no_gun['idle'] = self.load_frames(base_path + "Idle1.png", 4) 
        self.anim_no_gun['run'] = self.load_frames(base_path + "Run1.png", 6) 
        self.anim_no_gun['jump'] = self.load_frames(base_path + "Jump1.png", 4)
        
        self.anim_no_gun['attack'] = self.load_frames(attack_path, 6)
        self.anim_gun['attack'] = self.load_frames(attack_path, 6)
        
        try:
            self.gun_image = pygame.image.load(gun_path).convert_alpha()
            self.gun_image = pygame.transform.scale(self.gun_image, (int(self.gun_image.get_width()*1.5), int(self.gun_image.get_height()*1.5)))
            
            self.hand_image = pygame.image.load(hand_holding_path).convert_alpha()
            self.hand_image = pygame.transform.scale(self.hand_image, (int(self.hand_image.get_width()*1.5), int(self.hand_image.get_height()*1.5)))

            self.back_arm_image = pygame.image.load(back_arm_path).convert_alpha()
            self.back_arm_image = pygame.transform.scale(self.back_arm_image, (int(self.back_arm_image.get_width()*1.5), int(self.back_arm_image.get_height()*1.5)))
        except FileNotFoundError: pass



