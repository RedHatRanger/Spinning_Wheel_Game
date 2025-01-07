import pygame
import math
import random
import sys

# --- Configuration ---
WIDTH, HEIGHT = 800, 600
FPS = 60
NUM_SEGMENTS = 8     # How many slices (segments) you want
RADIUS = 250
SPIN_DECAY = 0.98    # friction multiplier each frame
MIN_SPIN_SPEED = 0.5 # threshold to stop spinning

SEGMENT_NAMES = [
    "Alice", "Bob", "Charlie", "David",
    "Eve", "Frank", "Grace", "Hannah"
]

# Colors for segments
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
pygame.display.set_caption("Center-Pointer Spinning Wheel")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

# Center of the screen
cx, cy = WIDTH // 2, HEIGHT // 2

# Rotation parameters
angle_offset = 0.0
spin_speed = 0.0
spinning = False
winner = None

# Tracking used/remaining logic (if you want a no-repeat cycle):
remaining_names = SEGMENT_NAMES[:]
used_names = []


def draw_wheel(names, angle):
    """
    Draw the wheel with equal segments for each name.
    The wheel is rotated by `angle` degrees.
    """
    if not names:
        return

    # Each slice covers an equal fraction of 360 degrees
    num_segments = len(names)
    segment_angle_deg = 360 / num_segments
    angle_rad = math.radians(angle)

    for i, name in enumerate(names):
        start_angle = i * segment_angle_deg
        end_angle = start_angle + segment_angle_deg

        # Convert to radians and add angle_offset
        start_rad = math.radians(start_angle) + angle_rad
        end_rad   = math.radians(end_angle)   + angle_rad

        # Pick a color
        color = COLORS[i % len(COLORS)]

        # Build a list of points (fan) to draw each segment
        points = [(cx, cy)]
        steps = 30  # how many points to create a smooth arc
        for step in range(steps + 1):
            t = start_rad + (end_rad - start_rad) * (step / steps)
            x = cx + RADIUS * math.cos(t)
            y = cy + RADIUS * math.sin(t)
            points.append((x, y))

        pygame.draw.polygon(screen, color, points)

        # Text: place near the middle of the segment’s arc
        mid_angle = (start_rad + end_rad) / 2
        text_x = cx + (RADIUS * 0.6) * math.cos(mid_angle)
        text_y = cy + (RADIUS * 0.6) * math.sin(mid_angle)
        text_surf = font.render(name, True, (0, 0, 0))
        text_rect = text_surf.get_rect(center=(text_x, text_y))
        screen.blit(text_surf, text_rect)


def draw_pointer_from_center():
    """
    Draw a pointer that starts from the center of the wheel
    and points straight up (towards negative y).
    """
    # The pointer is a simple arrow with some width
    pointer_length = RADIUS + 50  # extends beyond the wheel
    arrow_width = 10

    # Tip of the arrow (straight up from center)
    tip_x = cx
    tip_y = cy - pointer_length

    # Left edge of arrow base
    left_x = cx - arrow_width
    left_y = cy

    # Right edge of arrow base
    right_x = cx + arrow_width
    right_y = cy

    # Draw a filled triangle
    pygame.draw.polygon(
        screen,
        (255, 0, 0),  # red arrow
        [(cx, cy), (left_x, left_y), (tip_x, tip_y), (right_x, right_y)],
    )


def pick_winner(names, final_angle):
    """
    Determine which name is chosen when the wheel stops.
    We treat 'straight up' as the pointer position: -90 degrees.
    So we shift final_angle by +90 to see which slice is at 0 deg.
    """
    if not names:
        return None
    num_segments = len(names)
    segment_angle = 360 / num_segments

    # Adjust the wheel angle so that top is 0 degrees
    adjusted_angle = (final_angle + 90) % 360
    index = int(adjusted_angle // segment_angle)
    return names[index]


def reset_names_if_needed():
    """
    If we've used all names, reload them from used_names.
    """
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
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE and not spinning:
                    # Start spin
                    spinning = True
                    winner = None
                    spin_speed = random.uniform(10, 15)

        # Update the spinning angle
        if spinning:
            angle_offset += spin_speed
            spin_speed *= SPIN_DECAY
            if spin_speed < MIN_SPIN_SPEED:
                spinning = False
                final = angle_offset % 360
                winner = pick_winner(remaining_names, final)
                if winner:
                    used_names.append(winner)
                    remaining_names.remove(winner)
                    reset_names_if_needed()

        # Draw background
        screen.fill((255, 255, 255))

        # Draw wheel (rotated by angle_offset)
        draw_wheel(remaining_names, angle_offset)

        # Draw the pointer from the center
        draw_pointer_from_center()

        # Show the winner at the bottom if we have one
        if winner:
            text_surf = font.render(f"Winner: {winner}", True, (255, 0, 0))
            rect = text_surf.get_rect(center=(WIDTH // 2, HEIGHT - 50))
            screen.blit(text_surf, rect)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()