# Spinning Wheel Game

A Python-based spinning wheel game that allows you to input a list of names, spin the wheel, and land on a random name. The selected name is removed from the pool until all names have been chosen, ensuring fairness. Once all names are selected, the pool is reset automatically.

## Features

- **Customizable Name List**: Add any number of names to the wheel by modifying the list in the script.
- **Fair Selection**: Names are not repeated until all names have been selected.
- **Colorful Segments**: The wheel is divided into vibrant segments, each displaying a name.
- **Interactive Spinning**: Spin the wheel with a simple keypress and enjoy a smooth slowing animation.
- **Random Landing**: Each spin is completely random, ensuring unbiased results.

---

## Installation

### Requirements

- Python 3.x
- Pygame library

### Steps

1. Clone the repository or download the project:
   ```bash
   git clone https://github.com/your-repository/spinning-wheel-game.git
   cd spinning-wheel-game
   ```

2. Install the required library:
   ```bash
   pip install pygame
   ```

3. Run the game:
   ```bash
   python spinning_wheel.py
   ```

---

## How to Play

1. Press **Space** to spin the wheel.
2. Watch the wheel spin and slow down, eventually landing on a name.
3. The name that the wheel lands on will be displayed at the bottom of the screen.
4. Continue spinning until all names have been chosen.
5. Once all names are selected, the list resets automatically.

---

## Controls

- **Space**: Spin the wheel.
- **Esc**: Exit the game.

---

## Customization

### Name List

You can edit the list of names directly in the script. Locate the `ALL_NAMES` variable in the code and replace the default names with your desired list.

Example:
```python
ALL_NAMES = [
    "Alice", "Bob", "Charlie", "David", "Eve", "Frank", "Grace", "Hannah",
    "Isaac", "Jack", "Karen", "Liam", "Mia", "Nina", "Oscar", "Paul",
    "Quinn", "Rachel", "Steve", "Tina", "Uma", "Victor", "Wendy", "Xander", "Zoe"
]
```

You can add as many names as you like, but the visual appearance might get cramped if too many names are added.

---

### Segment Colors

The colors of the wheel segments can be customized by modifying the `COLORS` list in the script. Colors are defined as RGB tuples.

Default colors:
```python
COLORS = [
    (255, 69, 0),    # OrangeRed
    (30, 144, 255),  # DodgerBlue
    (34, 139, 34),   # ForestGreen
    (255, 215, 0),   # Gold
    (238, 130, 238), # Violet
    (106, 90, 205),  # SlateBlue
    (255, 105, 180), # HotPink
    (72, 61, 139),   # DarkSlateBlue
]
```

Add or modify the colors as desired.

---

### Spin Speed and Friction

Adjust the initial speed and friction of the spinning wheel to change how it behaves.

- **Spin Speed**: Modify the `random.uniform(10, 15)` function in the script to change the initial spin speed range.
- **Friction**: Adjust the `SPIN_DECAY` value (default is `0.98`) to control how quickly the wheel slows down. A value closer to `1.0` makes the wheel spin longer.

---

## Example Name List

The default name list includes 25 entries:
```
Alice, Bob, Charlie, David, Eve, Frank, Grace, Hannah, Isaac, Jack, Karen,
Liam, Mia, Nina, Oscar, Paul, Quinn, Rachel, Steve, Tina, Uma, Victor,
Wendy, Xander, Zoe
```

You can replace this with any names of your choice.

---

## Future Enhancements

Here are some potential enhancements you can add to the game:

- Save the list of winners to a file.
- Add sound effects for spinning and winner announcements.
- Allow customization of the wheel size, font, and segment spacing.
- Add a graphical user interface (GUI) to input names directly.

---

## License

This project is licensed under the GPLv3 License.

---

Enjoy your spinning wheel game! 🎉


