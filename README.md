# Scream Game

A unique voice-controlled 2D platformer where your voice is the controller! Talk to walk, scream to jump, and use various vocal sounds to perform different actions.

## Features

- Voice-controlled gameplay
- Multiple levels with increasing difficulty
- Various sound-based actions:
  - Talk to walk
  - Scream to jump
  - Whistle to dash
  - Hum to crouch
- Moving platforms and obstacles
- Sound intensity visualization
- Microphone calibration system
- Score tracking and high scores

## Requirements

- Python 3.8+
- Pygame
- NumPy
- SoundDevice
- Pillow
- Scipy

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/scream-game.git
cd scream-game
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

## How to Play

1. Run the game:
```bash
python main.py
```

2. In the main menu:
   - Click "Calibrate" to adjust microphone sensitivity
   - Click "Start Game" to begin playing
   - Use ESC to pause the game

3. Voice Controls:
   - Normal talking: Move forward
   - Loud shout: Jump
   - Sharp whistle: Dash
   - Low humming: Crouch
   - Double jump available in mid-air

4. Gameplay Tips:
   - Calibrate your microphone before playing
   - Use the sound intensity meter on the right side to gauge your volume
   - Watch out for different platform types:
     - Gray: Normal platforms
     - Green: Bounce platforms
     - Red: Spike platforms (dangerous!)
     - Cyan: Moving platforms
   - Reach the green exit portal to complete each level
   - Collect points by completing levels quickly

## Development

The game is structured into several components:

- `main.py`: Main game loop and initialization
- `src/sound_processor.py`: Handles voice input processing
- `src/player.py`: Player character logic and physics
- `src/sprite_manager.py`: Handles animations and sprites
- `src/level_manager.py`: Manages levels and platforms
- `src/game_state.py`: Handles game states and UI
- `config/settings.py`: Game configuration and constants

## Contributing

Feel free to contribute to this project by:

1. Forking the repository
2. Creating a new branch for your feature
3. Submitting a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Thanks to the Pygame community for their excellent documentation
- Sound processing inspired by various audio visualization projects
- Special thanks to all contributors and testers 