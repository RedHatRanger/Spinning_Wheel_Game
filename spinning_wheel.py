import pygame
import math
import random
import sys

# --- Configuration ---
NUM_NAMES = 25   # Set how many names to include
WIDTH, HEIGHT = 800, 600
FPS = 60

# List your names here (exactly NUM_NAMES entries if you like)
ALL_NAMES = [
    "Alice", "Bob", "Charlie", "David", "Eve", "Frank", "Grace", "Hannah",
    "Isaac", "Jack", "Karen", "Liam", "Mia", "Nina", "Oscar", "Paul",
    "Quinn", "Rachel", "Steve", "Tina", "Uma", "Victor", "Wendy", "Xander", "Zoe"
]

# Colors to cycle through (feel free to add or remove)
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

# --- Initialization ---
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Spinning Wheel Game")
clock = pygame.time.Clock()

# A basic font for text (can also use SysFont if you wish)
font = pygame.font.Font(None, 36)

# For convenience, pre-calculate center
center_x, center_y = WIDTH // 2, HEIGHT // 2
radius = 250  # Radius of the wheel

# Prepare name pools
remaining_names = ALL_NAMES[:NUM_NAMES]  # The current active pool
used_names = []                          # Used since last reset

# Rotation parameters
angle_offset = 0.0       # Current rotation angle in degrees
spin_speed = 0.0         # How many degrees per frame we rotate
SPIN_DECAY = 0.98        # Friction multiplier each frame
MIN_SPIN_SPEED = 0.5     # Threshold to stop spinning
winner = None            # Name that landed last
spinning = False         # Are we currently spinning?

def draw_wheel(names, angle):
    """
    Draw the wheel with equal segments for each name.
    `angle` is in degrees, representing how much the wheel is rotated.
    A pointer at the top (i.e., -90 degrees in standard math) will choose the segment.
    """
    num_segments = len(names)
    if num_segments == 0:
        return

    # Convert degrees to radians for math functions
    angle_rad = math.radians(angle)

    # Each segment's angular size in radians
    segment_angle = 2 * math.pi / num_segments

    for i, name in enumerate(names):
        # Starting angle (in radians) for this segment
        start_angle = i * segment_angle + angle_rad
        # Ending angle
        end_angle = start_angle + segment_angle

        # Pick a color
        color = COLORS[i % len(COLORS)]

        # Draw the segment as a polygon “fan” (center + radial points)
        points = [ (center_x, center_y) ]
        steps = 30  # Number of points along the arc to create smooth edges
        for step in range(steps + 1):
            theta = start_angle + (end_angle - start_angle) * (step / steps)
            x = center_x + radius * math.cos(theta)
            y = center_y + radius * math.sin(theta)
            points.append((x, y))

        pygame.draw.polygon(screen, color, points)

        # Draw the name in the middle of the segment
        text_angle = (start_angle + end_angle) / 2
        text_x = center_x + (radius * 0.6) * math.cos(text_angle)
        text_y = center_y + (radius * 0.6) * math.sin(text_angle)
        text_surface = font.render(name, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(text_x, text_y))
        screen.blit(text_surface, text_rect)

def pick_winner(names, final_angle):
    """
    Pick which segment is 'up' at the top after spinning stops.
    By default, the pointer is at -90 degrees (straight up).
    """
    if not names:
        return None

    num_segments = len(names)
    # Normalize the angle to [0..360)
    adjusted_angle = (final_angle + 90) % 360  # Add 90 because the pointer is at -90 degrees
    # Each segment covers an equal slice
    segment_size = 360 / num_segments
    # Find which segment index is chosen
    index = int(adjusted_angle // segment_size) % num_segments
    return names[index]

def reset_pools():
    """If all names are used, repopulate the remaining_names from used_names."""
    global remaining_names, used_names
    if len(remaining_names) == 0:
        remaining_names = used_names[:]
        used_names = []

def main():
    global angle_offset, spin_speed, spinning, winner, remaining_names, used_names

    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                # Press Esc to quit
                if event.key == pygame.K_ESCAPE:
                    running = False

                # Press Space to spin (only if not already spinning)
                elif event.key == pygame.K_SPACE and not spinning:
                    spinning = True
                    winner = None
                    # Random spin speed between 10-15 degrees/frame
                    spin_speed = random.uniform(10, 15)

        # Update
        if spinning:
            angle_offset += spin_speed
            spin_speed *= SPIN_DECAY

            # If speed is below threshold, stop spinning
            if spin_speed < MIN_SPIN_SPEED:
                spinning = False
                final = angle_offset % 360
                winner = pick_winner(remaining_names, final)
                if winner is not None:
                    used_names.append(winner)
                    remaining_names.remove(winner)
                    reset_pools()

        # Draw
        screen.fill((255, 255, 255))  # white background
        draw_wheel(remaining_names, angle_offset)

        # Draw an indicator (pointer) at the top (center_x, center_y - radius)
        pointer_length = 30
        pygame.draw.polygon(
            screen, (255, 0, 0),
            [
                (center_x, center_y - (radius + pointer_length)),
                (center_x - 10, center_y - radius),
                (center_x + 10, center_y - radius)
            ]
        )

        # Draw winner text if we have one
        if winner:
            text_surface = font.render(f"Winner: {winner}", True, (255, 0, 0))
            rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT - 50))
            screen.blit(text_surface, rect)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
