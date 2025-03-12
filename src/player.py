import pygame
import time
from config.settings import *
from src.sprite_manager import SpriteManager, PlayerState

class Player:
    def __init__(self, x, y):
        self.sprite_manager = SpriteManager()
        self.sprite_manager.load_sprite_sheets()
        
        # Get the dimensions from the first idle frame
        sprite = self.sprite_manager.sprites["idle"][0]
        self.width = sprite.get_width()
        self.height = sprite.get_height()
        
        # Create rect with sprite dimensions
        self.rect = pygame.Rect(x, y, self.width, self.height)
        
        # Movement variables
        self.velocity_x = 0
        self.velocity_y = 0
        self.on_ground = False
        self.on_wall = False
        self.facing_right = True
        
        # Action states
        self.is_jumping = False
        self.is_double_jumping = False
        self.is_dashing = False
        self.is_crouching = False
        self.dash_start_time = 0
        self.can_double_jump = True
        
    def update(self, action, platforms):
        current_time = time.time()
        
        # Handle dash
        if self.is_dashing:
            if current_time - self.dash_start_time > DASH_DURATION:
                self.is_dashing = False
            else:
                self.velocity_x = DASH_SPEED if self.facing_right else -DASH_SPEED
                self.velocity_y = 0
                self.sprite_manager.set_state(PlayerState.DASHING)
                return
        
        # Process sound-based actions
        if action != "none":
            self._handle_action(action)
        
        # Apply gravity if not on ground
        if not self.on_ground:
            self.velocity_y = min(self.velocity_y + GRAVITY, MAX_FALL_SPEED)
            
        # Apply friction and air resistance
        if self.on_ground:
            self.velocity_x *= FRICTION
        else:
            self.velocity_x *= AIR_RESISTANCE
            
        # Update position
        self.rect.x += self.velocity_x
        self._handle_horizontal_collisions(platforms)
        
        self.rect.y += self.velocity_y
        self._handle_vertical_collisions(platforms)
        
        # Update sprite state
        self._update_sprite_state()
        self.sprite_manager.update(current_time)
        
    def _handle_action(self, action):
        """Handle different sound-based actions"""
        if action == "walk" and self.on_ground and not self.is_crouching:
            self.velocity_x = WALK_SPEED if self.facing_right else -WALK_SPEED
            
        elif action == "jump":
            if self.on_ground:
                self.velocity_y = -JUMP_STRENGTH
                self.is_jumping = True
                self.can_double_jump = True
            elif self.can_double_jump and not self.is_double_jumping:
                self.velocity_y = -DOUBLE_JUMP_STRENGTH
                self.is_double_jumping = True
                self.can_double_jump = False
                
        elif action == "dash" and not self.is_dashing:
            self.is_dashing = True
            self.dash_start_time = time.time()
            
        elif action == "crouch" and self.on_ground:
            self.is_crouching = True
            self.velocity_x *= 0.5  # Slower movement while crouching
        else:
            self.is_crouching = False
            
    def _handle_horizontal_collisions(self, platforms):
        """Handle collisions with platforms horizontally"""
        for platform in platforms:
            if self.rect.colliderect(platform):
                if self.velocity_x > 0:  # Moving right
                    self.rect.right = platform.left
                    self.on_wall = True
                elif self.velocity_x < 0:  # Moving left
                    self.rect.left = platform.right
                    self.on_wall = True
                self.velocity_x = 0
                return
        self.on_wall = False
            
    def _handle_vertical_collisions(self, platforms):
        """Handle collisions with platforms vertically"""
        self.on_ground = False
        for platform in platforms:
            if self.rect.colliderect(platform):
                if self.velocity_y > 0:  # Moving down
                    self.rect.bottom = platform.top
                    self.on_ground = True
                    self.is_jumping = False
                    self.is_double_jumping = False
                elif self.velocity_y < 0:  # Moving up
                    self.rect.top = platform.bottom
                self.velocity_y = 0
                
    def _update_sprite_state(self):
        """Update the sprite state based on player state"""
        if self.is_dashing:
            state = PlayerState.DASHING
        elif self.is_crouching:
            state = PlayerState.CROUCHING
        elif not self.on_ground:
            state = PlayerState.JUMPING if self.velocity_y < 0 else PlayerState.FALLING
        elif abs(self.velocity_x) > 0.5:
            state = PlayerState.WALKING
        else:
            state = PlayerState.IDLE
            
        self.sprite_manager.set_state(state)
        
        # Update facing direction
        if abs(self.velocity_x) > 0:
            self.facing_right = self.velocity_x > 0
            self.sprite_manager.set_direction(self.facing_right)
            
    def draw(self, surface):
        """Draw the player on the surface"""
        sprite = self.sprite_manager.get_current_frame()
        # Center the sprite on the collision rect
        draw_x = self.rect.x - (sprite.get_width() - self.rect.width) // 2
        draw_y = self.rect.y - (sprite.get_height() - self.rect.height) // 2
        surface.blit(sprite, (draw_x, draw_y))
        
        if SHOW_HITBOXES:
            pygame.draw.rect(surface, RED, self.rect, 2)
            
    def reset(self, x, y):
        """Reset player position and state"""
        self.rect.x = x
        self.rect.y = y
        self.velocity_x = 0
        self.velocity_y = 0
        self.is_jumping = False
        self.is_double_jumping = False
        self.is_dashing = False
        self.is_crouching = False
        self.can_double_jump = True 