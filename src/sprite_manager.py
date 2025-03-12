import pygame
from enum import Enum
import time

class PlayerState(Enum):
    IDLE = "idle"
    WALKING = "walking"
    JUMPING = "jumping"
    FALLING = "falling"
    DASHING = "dashing"
    CROUCHING = "crouching"

class SpriteManager:
    def __init__(self):
        self.sprites = {}
        self.current_frame = 0
        self.animation_speed = 0.1  # Adjusted for smoother animation
        self.last_update = 0
        self.current_state = PlayerState.IDLE
        self.facing_right = True
        
        # Animation transition smoothing
        self.transition_time = 0
        self.transition_duration = 0.2  # Duration of transition in seconds
        self.previous_state = None
        
        # Sprite scaling
        self.scale_factor = 3.0  # Scale sprites to 3x their original size
        
        # Define frame counts for each animation
        self.frame_counts = {
            "idle": 11,
            "walking": 10,  # Using run animation for walking
            "jumping": 6,
            "falling": 6,   # Using last frames of jump for falling
            "dashing": 10,  # Using run animation for dash
            "crouching": 11 # Using idle animation for crouch
        }
        
    def load_sprite_sheets(self):
        """Load all sprite sheets for different animations"""
        try:
            # Load the sprite sheets
            idle_sheet = pygame.image.load("assets/images/character/idle.png").convert_alpha()
            run_sheet = pygame.image.load("assets/images/character/run2.png").convert_alpha()
            jump_sheet = pygame.image.load("assets/images/character/jump.png").convert_alpha()
            
            # Calculate frame dimensions
            idle_frame_width = idle_sheet.get_width() // self.frame_counts["idle"]
            run_frame_width = run_sheet.get_width() // self.frame_counts["walking"]
            jump_frame_width = jump_sheet.get_width() // self.frame_counts["jumping"]
            
            # Split and scale sprite sheets into individual frames
            self.sprites["idle"] = self._split_and_scale_sprite_sheet(idle_sheet, self.frame_counts["idle"])
            self.sprites["walking"] = self._split_and_scale_sprite_sheet(run_sheet, self.frame_counts["walking"])
            self.sprites["dashing"] = self.sprites["walking"]  # Reuse run animation for dash
            self.sprites["jumping"] = self._split_and_scale_sprite_sheet(jump_sheet, self.frame_counts["jumping"])
            self.sprites["falling"] = [self.sprites["jumping"][-1]]  # Use last jump frame for falling
            self.sprites["crouching"] = self.sprites["idle"]  # Reuse idle animation for crouch
            
        except Exception as e:
            print(f"Error loading sprites: {e}")
            self._create_fallback_sprites()
            
    def _split_and_scale_sprite_sheet(self, sheet, frame_count):
        """Split a sprite sheet into individual frames and scale them"""
        frames = []
        frame_width = sheet.get_width() // frame_count
        frame_height = sheet.get_height()
        
        for i in range(frame_count):
            # Create frame surface
            frame_surface = pygame.Surface((frame_width, frame_height), pygame.SRCALPHA)
            frame_surface.blit(sheet, (0, 0), (i * frame_width, 0, frame_width, frame_height))
            
            # Scale frame
            scaled_width = int(frame_width * self.scale_factor)
            scaled_height = int(frame_height * self.scale_factor)
            scaled_frame = pygame.transform.scale(frame_surface, (scaled_width, scaled_height))
            
            frames.append(scaled_frame)
            
        return frames

    def _create_fallback_sprites(self):
        """Create basic rectangular sprites as fallback"""
        for state in PlayerState:
            surface = pygame.Surface((50, 50))
            surface.fill((0, 0, 255))
            self.sprites[state.value] = [surface]

    def update(self, current_time):
        """Update animation frame"""
        if current_time - self.last_update > self.animation_speed:
            self.current_frame = (self.current_frame + 1) % len(self.sprites[self.current_state.value])
            self.last_update = current_time

    def set_state(self, state):
        """Set the current animation state with smooth transition"""
        if isinstance(state, str):
            try:
                state = PlayerState(state)
            except ValueError:
                return
        
        if self.current_state != state:
            self.previous_state = self.current_state
            self.current_state = state
            self.transition_time = time.time()
            # Don't reset frame to 0 immediately for smoother transition
            if state in [PlayerState.JUMPING, PlayerState.FALLING]:
                self.current_frame = 0  # Reset only for certain state changes

    def get_current_frame(self):
        """Get the current animation frame with transition handling"""
        try:
            # Get current sprite
            sprite = self.sprites[self.current_state.value][self.current_frame]
            
            # Handle transition blending if in transition period
            if self.previous_state and time.time() - self.transition_time < self.transition_duration:
                # Get previous sprite
                prev_frame = min(self.current_frame, len(self.sprites[self.previous_state.value]) - 1)
                prev_sprite = self.sprites[self.previous_state.value][prev_frame]
                
                # Calculate blend factor (0 to 1)
                blend = (time.time() - self.transition_time) / self.transition_duration
                
                # Create a new surface for blending
                blended = pygame.Surface(sprite.get_size(), pygame.SRCALPHA)
                blended.blit(prev_sprite, (0, 0))
                sprite.set_alpha(int(255 * blend))
                blended.blit(sprite, (0, 0))
                sprite = blended
            
            if not self.facing_right:
                return pygame.transform.flip(sprite, True, False)
            return sprite
        except (KeyError, IndexError):
            # Return a default sprite if there's an error
            surface = pygame.Surface((50, 50))
            surface.fill((255, 0, 0))
            return surface

    def set_direction(self, facing_right):
        """Set the direction the sprite is facing"""
        self.facing_right = facing_right 