"""Game settings and configuration"""

import pygame

# Window settings
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
FPS = 60
TITLE = "Scream Game"

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)

# Player settings
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 80
WALK_SPEED = 5
JUMP_STRENGTH = 15
DOUBLE_JUMP_STRENGTH = 12
DASH_SPEED = 15
DASH_DURATION = 0.3
GRAVITY = 0.8
MAX_FALL_SPEED = 15
FRICTION = 0.85
AIR_RESISTANCE = 0.95

# Sound settings
SAMPLE_RATE = 44100
WINDOW_SIZE = 2048git add .
HISTORY_SIZE = 10
CALIBRATION_TIME = 3  # seconds

# Intensity thresholds (will be set during calibration)
WALK_THRESHOLD = 0.3
JUMP_THRESHOLD = 0.6
DASH_THRESHOLD = 0.8

# Frequency ranges for special actions
WHISTLE_MIN_FREQ = 2000
WHISTLE_MAX_FREQ = 4000
HUM_MIN_FREQ = 100
HUM_MAX_FREQ = 400

# Platform settings
PLATFORM_COLORS = {
    'normal': (100, 100, 100),
    'bounce': (0, 255, 100),
    'moving': (100, 100, 255),
    'hazard': (255, 50, 50)
}

# Debug settings
SHOW_HITBOXES = False
SHOW_SOUND_DEBUG = False

# UI settings
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 50
BUTTON_COLOR = (50, 50, 50)
BUTTON_HOVER_COLOR = (70, 70, 70)
BUTTON_TEXT_COLOR = WHITE
BUTTON_FONT_SIZE = 32
TITLE_FONT_SIZE = 64

# Initialize pygame fonts
pygame.font.init()
try:
    GAME_FONT = pygame.font.Font(None, BUTTON_FONT_SIZE)
    TITLE_FONT = pygame.font.Font(None, TITLE_FONT_SIZE)
except pygame.error:
    print("Warning: Default font not found. Using system font.")
    GAME_FONT = pygame.font.SysFont('arial', BUTTON_FONT_SIZE)
    TITLE_FONT = pygame.font.SysFont('arial', TITLE_FONT_SIZE)

# Default Sound Thresholds
DEFAULT_NOISE_FLOOR = 0.03
DEFAULT_WALK_THRESHOLD = 0.06
DEFAULT_JUMP_THRESHOLD = 0.2
DEFAULT_DASH_THRESHOLD = 0.15

# Physics
WALL_SLIDE_SPEED = 2

# Debug
DEBUG = True
SHOW_SOUND_LEVELS = True 