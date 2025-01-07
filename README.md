# Spinning_Wheel_Game
This game will choose a random name

# Spinning Wheel Game

A Python-based spinning wheel game where you can load 25 (or more) names into the wheel. When spun, the wheel lands on a random name, and that name is removed from the active pool. Once all names are selected, the pool is reset, ensuring each name is chosen only once per cycle.

## Features

- **Customizable Name List**: You can manually load any number of names into the wheel.
- **Random Selection**: The spinning and landing mechanism is completely random.
- **Fairness**: A name will not be selected again until all other names in the pool have been chosen.
- **Colorful Segments**: Each name is displayed in a vibrant, rotating pie segment.
- **Interactive Animation**: Spin the wheel by pressing the space bar.

## Requirements

- Python 3.x
- `pygame` library

## Installation

1. Clone the repository or download the source code:
   ```bash
   git clone https://github.com/your-repository/spinning-wheel-game.git
   cd spinning-wheel-game
