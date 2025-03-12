import pygame
import sys
from config.settings import *
from src.game_state import GameStateManager, GameState
from src.sound_processor import SoundProcessor
from src.player import Player
from src.level_manager import LevelManager

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Initialize game components
        self.sound_processor = SoundProcessor(
            sample_rate=SAMPLE_RATE,
            window_size=WINDOW_SIZE,
            history_size=HISTORY_SIZE
        )
        
        self.state_manager = GameStateManager(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.level_manager = LevelManager()
        
        # Create player at spawn point
        current_level = self.level_manager.get_current_level()
        spawn_x, spawn_y = current_level.spawn_point
        self.player = Player(spawn_x, spawn_y)
        
        # Load background
        try:
            self.background = pygame.image.load("assets/images/background.png").convert()
            self.background = pygame.transform.scale(self.background, (WINDOW_WIDTH, WINDOW_HEIGHT))
        except pygame.error:
            print("Warning: Could not load background image. Using solid color.")
            self.background = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
            self.background.fill((50, 50, 100))
            
    def handle_events(self):
        """Process all game events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return
                
            # Let the state manager handle the event first
            if self.state_manager.handle_event(event):
                continue
                
            # Handle game-specific events when playing
            if self.state_manager.state == GameState.PLAYING:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.state_manager.state = GameState.PAUSED
                        
    def update(self):
        """Update game state"""
        current_state = self.state_manager.state
        current_level = self.level_manager.get_current_level()
        
        if current_state == GameState.CALIBRATING:
            # Handle calibration
            if self.sound_processor.is_calibrating:
                self.sound_processor.update_calibration()
            else:
                self.state_manager.state = GameState.MENU
                
        elif current_state == GameState.PLAYING:
            # Get action from sound input
            action = self.sound_processor.get_action()
            
            # Update player with all platforms (static and moving)
            all_platforms = [p.rect for p in current_level.platforms + current_level.moving_platforms]
            self.player.update(action, all_platforms)
            
            # Check for level completion
            if self.player.rect.colliderect(pygame.Rect(*current_level.exit_point, 30, 30)):
                if self.level_manager.has_next_level():
                    self.level_manager.next_level()
                    new_level = self.level_manager.get_current_level()
                    spawn_x, spawn_y = new_level.spawn_point
                    self.player.reset(spawn_x, spawn_y)
                    self.state_manager.state = GameState.LEVEL_COMPLETE
                else:
                    self.state_manager.state = GameState.VICTORY
                    
            # Check for death (falling off screen or hitting hazards)
            if (self.player.rect.top > WINDOW_HEIGHT or
                any(p.type == "spike" and self.player.rect.colliderect(p.rect)
                    for p in current_level.platforms)):
                self.state_manager.state = GameState.GAME_OVER
                
        # Update moving platforms
        if current_state in [GameState.PLAYING, GameState.PAUSED]:
            current_level.update()
            
    def draw(self):
        """Draw the game screen"""
        # Draw background
        self.screen.blit(self.background, (0, 0))
        
        current_state = self.state_manager.state
        
        # Draw level and player during gameplay
        if current_state in [GameState.PLAYING, GameState.PAUSED]:
            current_level = self.level_manager.get_current_level()
            current_level.draw(self.screen)
            self.player.draw(self.screen)
            
        # Draw sound debug info if enabled
        if SHOW_SOUND_DEBUG and current_state in [GameState.PLAYING, GameState.CALIBRATING]:
            self._draw_sound_debug()
            
        # Draw UI elements
        self.state_manager.draw(self.screen)
        
        pygame.display.flip()
        
    def _draw_sound_debug(self):
        """Draw sound debug information"""
        intensity = self.sound_processor.get_current_intensity()
        avg_intensity = self.sound_processor.get_average_intensity()
        
        # Draw intensity bars
        bar_width = 20
        bar_height = 100
        x = WINDOW_WIDTH - 30
        y = WINDOW_HEIGHT - 120
        
        # Current intensity
        pygame.draw.rect(self.screen, RED,
                        (x, y + bar_height * (1 - intensity),
                         bar_width, bar_height * intensity))
                         
        # Average intensity
        pygame.draw.rect(self.screen, BLUE,
                        (x - 30, y + bar_height * (1 - avg_intensity),
                         bar_width, bar_height * avg_intensity))
                         
        # Thresholds
        for threshold, color in [(WALK_THRESHOLD, GREEN),
                               (JUMP_THRESHOLD, YELLOW),
                               (DASH_THRESHOLD, RED)]:
            y_pos = y + bar_height * (1 - threshold)
            pygame.draw.line(self.screen, color,
                           (x - 40, y_pos),
                           (x + bar_width + 10, y_pos), 2)
                           
    def cleanup(self):
        """Clean up resources"""
        self.sound_processor.cleanup()
        pygame.quit()
        
    def game_loop(self):
        """Main game loop"""
        try:
            while self.running:
                self.handle_events()
                self.update()
                self.draw()
                self.clock.tick(FPS)
        finally:
            self.cleanup()
            
if __name__ == "__main__":
    game = Game()
    game.game_loop()
