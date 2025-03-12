import pygame
import json
from config.settings import *

class Platform:
    def __init__(self, x, y, width, height, platform_type="normal"):
        self.rect = pygame.Rect(x, y, width, height)
        self.type = platform_type
        self.color = self._get_color()
        
    def _get_color(self):
        colors = {
            "normal": (100, 100, 100),
            "bounce": (0, 255, 0),
            "spike": (255, 0, 0),
            "moving": (0, 255, 255)
        }
        return colors.get(self.type, (100, 100, 100))
        
    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        
class MovingPlatform(Platform):
    def __init__(self, x, y, width, height, move_distance, speed):
        super().__init__(x, y, width, height, "moving")
        self.start_x = x
        self.start_y = y
        self.move_distance = move_distance
        self.speed = speed
        self.direction = 1
        self.distance_moved = 0
        
    def update(self):
        if abs(self.distance_moved) >= self.move_distance:
            self.direction *= -1
            
        movement = self.speed * self.direction
        self.rect.x += movement
        self.distance_moved += movement

class Level:
    def __init__(self, level_data):
        self.platforms = []
        self.moving_platforms = []
        self.spawn_point = (100, 100)
        self.exit_point = None
        self.background = None
        self.load_level(level_data)
        
    def load_level(self, level_data):
        """Load level from dictionary data"""
        # Set spawn and exit points
        self.spawn_point = tuple(level_data.get("spawn_point", (100, 100)))
        self.exit_point = tuple(level_data.get("exit_point", (700, 100)))
        
        # Load platforms
        for platform_data in level_data.get("platforms", []):
            if platform_data.get("type") == "moving":
                platform = MovingPlatform(
                    platform_data["x"],
                    platform_data["y"],
                    platform_data["width"],
                    platform_data["height"],
                    platform_data.get("move_distance", 100),
                    platform_data.get("speed", 2)
                )
                self.moving_platforms.append(platform)
            else:
                platform = Platform(
                    platform_data["x"],
                    platform_data["y"],
                    platform_data["width"],
                    platform_data["height"],
                    platform_data.get("type", "normal")
                )
                self.platforms.append(platform)
                
    def update(self):
        """Update level elements"""
        for platform in self.moving_platforms:
            platform.update()
            
    def draw(self, surface):
        """Draw all level elements"""
        # Draw background
        surface.fill(BLACK)
        
        # Draw platforms
        for platform in self.platforms + self.moving_platforms:
            platform.draw(surface)
            
        # Draw exit point
        if self.exit_point:
            pygame.draw.rect(surface, GREEN, 
                           pygame.Rect(self.exit_point[0], self.exit_point[1], 30, 30))

class LevelManager:
    def __init__(self):
        self.levels = []
        self.current_level_index = 0
        self.load_levels()
        
    def load_levels(self):
        """Load all level data"""
        # Example level data - in a real game, this would be loaded from files
        level_data = [
            {
                "spawn_point": [100, 450],
                "exit_point": [700, 450],
                "platforms": [
                    {"x": 0, "y": 500, "width": 800, "height": 100, "type": "normal"},
                    {"x": 300, "y": 400, "width": 200, "height": 20, "type": "normal"},
                    {"x": 100, "y": 300, "width": 200, "height": 20, "type": "normal"},
                    {"x": 500, "y": 300, "width": 200, "height": 20, "type": "normal"},
                    {"x": 300, "y": 200, "width": 200, "height": 20, "type": "moving",
                     "move_distance": 200, "speed": 3}
                ]
            },
            {
                "spawn_point": [100, 450],
                "exit_point": [700, 150],
                "platforms": [
                    {"x": 0, "y": 500, "width": 800, "height": 100, "type": "normal"},
                    {"x": 200, "y": 400, "width": 100, "height": 20, "type": "bounce"},
                    {"x": 400, "y": 300, "width": 100, "height": 20, "type": "normal"},
                    {"x": 600, "y": 200, "width": 200, "height": 20, "type": "normal"},
                    {"x": 300, "y": 350, "width": 50, "height": 10, "type": "spike"}
                ]
            }
        ]
        
        self.levels = [Level(data) for data in level_data]
        
    def get_current_level(self):
        """Get the current level"""
        return self.levels[self.current_level_index]
        
    def has_next_level(self):
        """Check if there is a next level available"""
        return self.current_level_index < len(self.levels) - 1
        
    def next_level(self):
        """Advance to the next level"""
        if self.has_next_level():
            self.current_level_index += 1
            return True
        return False
        
    def reset_level(self):
        """Reset the current level"""
        self.levels[self.current_level_index] = Level(
            self._get_level_data(self.current_level_index)
        )
        
    def _get_level_data(self, index):
        """Get the level data for the specified index"""
        # In a real game, this would load from a file
        level_data = [
            {
                "spawn_point": [100, 450],
                "exit_point": [700, 450],
                "platforms": [
                    {"x": 0, "y": 500, "width": 800, "height": 100, "type": "normal"},
                    {"x": 300, "y": 400, "width": 200, "height": 20, "type": "normal"},
                    {"x": 100, "y": 300, "width": 200, "height": 20, "type": "normal"},
                    {"x": 500, "y": 300, "width": 200, "height": 20, "type": "normal"},
                    {"x": 300, "y": 200, "width": 200, "height": 20, "type": "moving",
                     "move_distance": 200, "speed": 3}
                ]
            },
            {
                "spawn_point": [100, 450],
                "exit_point": [700, 150],
                "platforms": [
                    {"x": 0, "y": 500, "width": 800, "height": 100, "type": "normal"},
                    {"x": 200, "y": 400, "width": 100, "height": 20, "type": "bounce"},
                    {"x": 400, "y": 300, "width": 100, "height": 20, "type": "normal"},
                    {"x": 600, "y": 200, "width": 200, "height": 20, "type": "normal"},
                    {"x": 300, "y": 350, "width": 50, "height": 10, "type": "spike"}
                ]
            }
        ]
        return level_data[index] 