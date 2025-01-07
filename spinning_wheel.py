import pygame
import math
import random
import sys

# --- Configuration ---
NUM_NAMES = 10   # Number of names on the wheel at a time
WIDTH, HEIGHT = 800, 600
FPS = 60

# All names pool (full list of names to rotate into the wheel)
ALL_NAMES = [
    "Alice", "Bob", "Charlie", "David", "Eve", "Frank", "Grace", "Hannah",
    "Isaac", "Jack", "Karen", "Liam", "Mia", "Nina", "Oscar", "Paul",
    "Quinn", "Rachel", "Steve", "Tina"
]

# Colors to cycle through
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

# A basic font for text
font = pygame.font.Font(None, 36)

# For convenience, pre-calculate center
center_x, center_y = WIDTH // 2, HEIGHT // 2
radius = 250  # Radius of the wheel

# Prepare name pools
current_names = random.sample(ALL_NAMES, NUM_NAMES)  # Names currently on the wheel
remaining_pool = [name for name in ALL_NAMES if name not in current_names]  # Remaining pool

# Rotation parameters
angle_offset = 0.0       # Current rotation angle in degrees
spin_speed = 0.0         # How many degrees per frame we rotate
SPIN_DECAY = 0.99        # Friction multiplier each frame
MIN_SPIN_SPEED = 0.5     # Threshold to stop spinning
winner = None            # Name that landed last
spinning = False         # Are we currently spinning?

def draw_wheel(names, angle):
    """
    Draw the wheel with equal segments for each name.
    `angle` is in degrees, representing how much the wheel is rotated.
    We rotate the drawing by -90° so that segment 0 is physically at the top.
    """
    num_segments = len(names)
    if num_segments == 0:
        return

    # Convert degrees to radians for math functions and shift by -90° (pi/2)
    angle_rad = math.radians(angle) - (math.pi / 2)

    # Each segment's angular size in radians
    segment_angle = 2 * math.pi / num_segments

    for i, name in enumerate(names):
        # Starting angle (in radians) for this segment
        start_angle = i * segment_angle + angle_rad
        # Ending angle
        end_angle = start_angle + segment_angle

        # Pick a color
        color = COLORS[i % len(COLORS)]

        # Draw the segment as a polygon (center + radial points)
        points = [(center_x, center_y)]
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
    Determine which name is at the top under the pointer.
    Since we rotated the wheel so wedge 0 is at angle=0 at the top,
    we only do a half-wedge shift so the pointer lands in the middle of the wedge.
    """
    if not names:
        return None

    num_segments = len(names)
    segment_size = 360 / num_segments

    # Just shift by half a segment so we land in the wedge’s center
    adjusted_angle = (final_angle + segment_size / 2) % 360

    index = int(adjusted_angle // segment_size) % num_segments
    return names[index]

def update_wheel(winner):
    """
    Remove the winner from the current wheel and add a new name from the remaining pool,
    if available.
    """
    global current_names, remaining_pool

    if winner in current_names:
        current_names.remove(winner)
    
    if remaining_pool:
        new_name = random.choice(remaining_pool)
        current_names.append(new_name)
        remaining_pool.remove(new_name)

def main():
    global angle_offset, spin_speed, spinning, winner, current_names, remaining_pool

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
                winner = pick_winner(current_names, final)
                if winner is not None:
                    update_wheel(winner)

        # Draw
        screen.fill((255, 255, 255))  # white background
        draw_wheel(current_names, angle_offset)

        # Draw an indicator (pointer) at the top
        pointer_length = 30
        pygame.draw.polygon(
            screen, (255, 0, 0),
            [
                (center_x, center_y - (radius + pointer_length)), # top point
                (center_x - 10, center_y - radius),               # left corner
                (center_x + 10, center_y - radius)                # right corner
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
