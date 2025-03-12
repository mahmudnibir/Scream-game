import pygame
from enum import Enum

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
        self.animation_speed = 0.2
        self.last_update = 0
        self.current_state = PlayerState.IDLE
        self.facing_right = True
        
    def load_sprite_sheets(self):
        """Load all sprite sheets for different animations"""
        try:
            # Load sprite sheets for each state
            # For now, we'll create colored rectangles as placeholders
            # In a real game, you'd load actual sprite sheets here
            states = [state.value for state in PlayerState]
            for state in states:
                self.sprites[state] = self._create_placeholder_animation(state)
        except Exception as e:
            print(f"Error loading sprites: {e}")
            # Fallback to basic rectangles if loading fails
            self._create_fallback_sprites()

    def _create_placeholder_animation(self, state):
        """Create placeholder animations until real sprites are added"""
        frames = []
        colors = {
            "idle": (0, 0, 255),      # Blue
            "walking": (0, 255, 0),    # Green
            "jumping": (255, 255, 0),  # Yellow
            "falling": (255, 165, 0),  # Orange
            "dashing": (255, 0, 0),    # Red
            "crouching": (128, 0, 128) # Purple
        }
        
        # Create 4 slightly different frames for each animation
        for i in range(4):
            surface = pygame.Surface((50, 50))
            color = colors.get(state, (0, 0, 255))
            surface.fill(color)
            
            # Add some variation to frames
            if i % 2:  # Every other frame
                pygame.draw.rect(surface, (255, 255, 255), 
                               (10, 10, 30, 30), 2)
            
            frames.append(surface)
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
        """Set the current animation state"""
        if isinstance(state, str):
            try:
                state = PlayerState(state)
            except ValueError:
                return
        
        if self.current_state != state:
            self.current_state = state
            self.current_frame = 0

    def get_current_frame(self):
        """Get the current animation frame"""
        try:
            sprite = self.sprites[self.current_state.value][self.current_frame]
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