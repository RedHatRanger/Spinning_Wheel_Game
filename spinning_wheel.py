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

font = pygame.font.Font(None, 36)

center_x, center_y = WIDTH // 2, HEIGHT // 2
radius = 250  # Radius of the wheel

# Prepare name pools
current_names = random.sample(ALL_NAMES, NUM_NAMES)
remaining_pool = [n for n in ALL_NAMES if n not in current_names]

# Rotation parameters
angle_offset = 0.0     # Current rotation angle in degrees
spin_speed = 0.0       # Degrees to rotate per frame
SPIN_DECAY = 0.99      # How quickly spin speed decays per frame
MIN_SPIN_SPEED = 0.5   # Threshold to stop the spin
winner = None          # Last chosen winner
spinning = False       # Are we currently spinning?

def draw_wheel(names, angle_degs):
    """
    Draw the wheel so that wedge 0 is physically at the top when angle_degs=0.
    We achieve this by subtracting 90° (pi/2) from the wheel's angle in radians.
    """
    num_segments = len(names)
    if num_segments == 0:
        return

    # Convert angle_degs to radians and shift by -90° to put segment 0 at the top
    angle_rad = math.radians(angle_degs) - math.pi / 2

    segment_angle = 2 * math.pi / num_segments

    for i, name in enumerate(names):
        start_angle = angle_rad + i * segment_angle
        end_angle = start_angle + segment_angle
        color = COLORS[i % len(COLORS)]

        # Draw the segment as a polygon (center + points along the arc)
        points = [(center_x, center_y)]
        steps = 30  # how many points for the arc's smoothness
        for step in range(steps + 1):
            theta = start_angle + (end_angle - start_angle) * (step / steps)
            x = center_x + radius * math.cos(theta)
            y = center_y + radius * math.sin(theta)
            points.append((x, y))

        pygame.draw.polygon(screen, color, points)

        # Draw the name in the middle of the segment
        mid_angle = (start_angle + end_angle) / 2
        text_x = center_x + (radius * 0.6) * math.cos(mid_angle)
        text_y = center_y + (radius * 0.6) * math.sin(mid_angle)
        text_surface = font.render(name, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(text_x, text_y))
        screen.blit(text_surface, text_rect)

def pick_winner(names, final_angle):
    """
    Determine which wedge is at the top, given that we've rotated
    the drawing so wedge 0 is at angle=0 at the top.
    
    We add half a wedge to final_angle so the pointer lands in the
    middle of the wedge, rather than on the boundary.
    """
    if not names:
        return None

    num_segments = len(names)
    segment_size = 360 / num_segments

    # Adding half a wedge shifts the pointer into the center of the wedge
    adjusted_angle = (final_angle + segment_size / 2) % 360
    index = int(adjusted_angle // segment_size)
    return names[index]

def update_wheel(chosen_name):
    """
    Remove the winner from current_names and add a new name from the pool.
    """
    global current_names, remaining_pool

    if chosen_name in current_names:
        current_names.remove(chosen_name)
    if remaining_pool:
        new_name = random.choice(remaining_pool)
        remaining_pool.remove(new_name)
        current_names.append(new_name)

def main():
    global angle_offset, spin_speed, spinning, winner

    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                # Press ESC to quit
                if event.key == pygame.K_ESCAPE:
                    running = False
                # Press SPACE to spin (only if not already spinning)
                elif event.key == pygame.K_SPACE and not spinning:
                    spinning = True
                    winner = None
                    spin_speed = random.uniform(10, 15)  # random degrees/frame

        # Spin logic
        if spinning:
            angle_offset += spin_speed
            spin_speed *= SPIN_DECAY
            if spin_speed < MIN_SPIN_SPEED:
                spinning = False
                final_angle = angle_offset % 360
                winner = pick_winner(current_names, final_angle)
                if winner:
                    update_wheel(winner)

        # Draw
        screen.fill((255, 255, 255))
        draw_wheel(current_names, angle_offset)

        # Draw the pointer at the top (red triangle)
        pointer_length = 30
        pygame.draw.polygon(
            screen, (255, 0, 0),
            [
                (center_x, center_y - (radius + pointer_length)),  # top tip
                (center_x - 10, center_y - radius),                # left
                (center_x + 10, center_y - radius)                 # right
            ]
        )

        # Show the winner at the bottom
        if winner:
            txt = font.render(f"Winner: {winner}", True, (255, 0, 0))
            rect = txt.get_rect(center=(WIDTH // 2, HEIGHT - 50))
            screen.blit(txt, rect)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
