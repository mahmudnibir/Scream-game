import pygame
from enum import Enum
from config.settings import *

class GameState(Enum):
    MENU = "menu"
    CALIBRATING = "calibrating"
    PLAYING = "playing"
    PAUSED = "paused"
    GAME_OVER = "game_over"
    LEVEL_COMPLETE = "level_complete"
    VICTORY = "victory"

class Button:
    def __init__(self, x, y, width, height, text, color, hover_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False
        
    def draw(self, surface):
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(surface, color, self.rect, border_radius=10)
        
        font = pygame.font.Font(None, 36)
        text_surface = font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.is_hovered:
                return True
        return False

class GameStateManager:
    def __init__(self, screen_width, screen_height):
        self.state = GameState.MENU
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.setup_ui()
        self.score = 0
        self.high_score = 0
        self.calibration_time = 5  # seconds
        self.calibration_start = 0
        
    def setup_ui(self):
        """Setup UI elements for different states"""
        # Menu buttons
        button_width = 200
        button_height = 50
        button_x = (self.screen_width - button_width) // 2
        
        self.menu_buttons = {
            "start": Button(button_x, 200, button_width, button_height, 
                          "Start Game", (0, 100, 0), (0, 150, 0)),
            "calibrate": Button(button_x, 300, button_width, button_height,
                              "Calibrate", (0, 0, 100), (0, 0, 150)),
            "quit": Button(button_x, 400, button_width, button_height,
                         "Quit", (100, 0, 0), (150, 0, 0))
        }
        
        # Pause buttons
        self.pause_buttons = {
            "resume": Button(button_x, 200, button_width, button_height,
                           "Resume", (0, 100, 0), (0, 150, 0)),
            "menu": Button(button_x, 300, button_width, button_height,
                         "Main Menu", (0, 0, 100), (0, 0, 150))
        }
        
        # Game over buttons
        self.game_over_buttons = {
            "retry": Button(button_x, 300, button_width, button_height,
                          "Retry", (0, 100, 0), (0, 150, 0)),
            "menu": Button(button_x, 400, button_width, button_height,
                         "Main Menu", (0, 0, 100), (0, 0, 150))
        }
        
    def handle_event(self, event):
        """Handle events based on current state"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if self.state == GameState.PLAYING:
                    self.state = GameState.PAUSED
                elif self.state == GameState.PAUSED:
                    self.state = GameState.PLAYING
                    
        if self.state == GameState.MENU:
            return self._handle_menu_events(event)
        elif self.state == GameState.PAUSED:
            self._handle_pause_events(event)
        elif self.state == GameState.GAME_OVER:
            self._handle_game_over_events(event)
        return True
            
    def _handle_menu_events(self, event):
        """Handle menu state events"""
        for button_name, button in self.menu_buttons.items():
            if button.handle_event(event):
                if button_name == "start":
                    self.state = GameState.PLAYING
                elif button_name == "calibrate":
                    self.state = GameState.CALIBRATING
                    self.calibration_start = pygame.time.get_ticks()
                elif button_name == "quit":
                    return False
        return True
        
    def _handle_pause_events(self, event):
        """Handle pause state events"""
        for button_name, button in self.pause_buttons.items():
            if button.handle_event(event):
                if button_name == "resume":
                    self.state = GameState.PLAYING
                elif button_name == "menu":
                    self.state = GameState.MENU
                    
    def _handle_game_over_events(self, event):
        """Handle game over state events"""
        for button_name, button in self.game_over_buttons.items():
            if button.handle_event(event):
                if button_name == "retry":
                    self.state = GameState.PLAYING
                    self.score = 0
                elif button_name == "menu":
                    self.state = GameState.MENU
                    
    def update(self):
        """Update game state"""
        if self.state == GameState.CALIBRATING:
            current_time = pygame.time.get_ticks()
            if (current_time - self.calibration_start) / 1000 >= self.calibration_time:
                self.state = GameState.PLAYING
                
    def draw(self, surface):
        """Draw UI elements based on current state"""
        if self.state == GameState.MENU:
            self._draw_menu(surface)
        elif self.state == GameState.PAUSED:
            self._draw_pause(surface)
        elif self.state == GameState.GAME_OVER:
            self._draw_game_over(surface)
        elif self.state == GameState.CALIBRATING:
            self._draw_calibration(surface)
        elif self.state == GameState.LEVEL_COMPLETE:
            self._draw_level_complete(surface)
        elif self.state == GameState.VICTORY:
            self._draw_victory(surface)
            
    def _draw_menu(self, surface):
        """Draw menu screen"""
        surface.fill(BLACK)
        font = pygame.font.Font(None, 74)
        title = font.render("Scream Game", True, WHITE)
        title_rect = title.get_rect(center=(self.screen_width//2, 100))
        surface.blit(title, title_rect)
        
        for button in self.menu_buttons.values():
            button.draw(surface)
            
    def _draw_pause(self, surface):
        """Draw pause screen"""
        s = pygame.Surface((self.screen_width, self.screen_height))
        s.set_alpha(128)
        s.fill(BLACK)
        surface.blit(s, (0,0))
        
        font = pygame.font.Font(None, 74)
        text = font.render("PAUSED", True, WHITE)
        text_rect = text.get_rect(center=(self.screen_width//2, 100))
        surface.blit(text, text_rect)
        
        for button in self.pause_buttons.values():
            button.draw(surface)
            
    def _draw_game_over(self, surface):
        """Draw game over screen"""
        s = pygame.Surface((self.screen_width, self.screen_height))
        s.set_alpha(128)
        s.fill(BLACK)
        surface.blit(s, (0,0))
        
        font = pygame.font.Font(None, 74)
        text = font.render("GAME OVER", True, WHITE)
        text_rect = text.get_rect(center=(self.screen_width//2, 100))
        surface.blit(text, text_rect)
        
        score_font = pygame.font.Font(None, 48)
        score_text = score_font.render(f"Score: {self.score}", True, WHITE)
        score_rect = score_text.get_rect(center=(self.screen_width//2, 200))
        surface.blit(score_text, score_rect)
        
        for button in self.game_over_buttons.values():
            button.draw(surface)
            
    def _draw_calibration(self, surface):
        """Draw calibration screen"""
        surface.fill(BLACK)
        
        font = pygame.font.Font(None, 48)
        text = font.render("Calibrating Microphone...", True, WHITE)
        text_rect = text.get_rect(center=(self.screen_width//2, 200))
        surface.blit(text, text_rect)
        
        time_left = self.calibration_time - (pygame.time.get_ticks() - self.calibration_start) / 1000
        if time_left > 0:
            time_text = font.render(f"Time left: {time_left:.1f}s", True, WHITE)
            time_rect = time_text.get_rect(center=(self.screen_width//2, 300))
            surface.blit(time_text, time_rect)
            
    def _draw_level_complete(self, surface):
        """Draw level complete screen"""
        s = pygame.Surface((self.screen_width, self.screen_height))
        s.set_alpha(128)
        s.fill(BLACK)
        surface.blit(s, (0,0))
        
        font = pygame.font.Font(None, 74)
        text = font.render("Level Complete!", True, WHITE)
        text_rect = text.get_rect(center=(self.screen_width//2, self.screen_height//2))
        surface.blit(text, text_rect)
        
    def _draw_victory(self, surface):
        """Draw victory screen"""
        surface.fill(BLACK)
        
        font = pygame.font.Font(None, 74)
        text = font.render("Victory!", True, WHITE)
        text_rect = text.get_rect(center=(self.screen_width//2, 200))
        surface.blit(text, text_rect)
        
        score_font = pygame.font.Font(None, 48)
        score_text = score_font.render(f"Final Score: {self.score}", True, WHITE)
        score_rect = score_text.get_rect(center=(self.screen_width//2, 300))
        surface.blit(score_text, score_rect)
        
        if self.score > self.high_score:
            self.high_score = self.score
            high_score_text = score_font.render("New High Score!", True, (255, 215, 0))
            high_score_rect = high_score_text.get_rect(center=(self.screen_width//2, 400))
            surface.blit(high_score_text, high_score_rect) 