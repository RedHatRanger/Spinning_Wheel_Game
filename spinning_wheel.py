import pygame
import math
import random
import sys

# --- Configuration ---
NUM_NAMES = 10
WIDTH, HEIGHT = 800, 600
FPS = 60

ALL_NAMES = [
    "Alice", "Bob", "Charlie", "David", "Eve", "Frank", "Grace", "Hannah",
    "Isaac", "Jack", "Karen", "Liam", "Mia", "Nina", "Oscar", "Paul",
    "Quinn", "Rachel", "Steve", "Tina"
]

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

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Spinning Wheel Game")
clock = pygame.time.Clock()

font = pygame.font.Font(None, 36)

center_x, center_y = WIDTH // 2, HEIGHT // 2
radius = 250

# Pool setup
current_names = random.sample(ALL_NAMES, NUM_NAMES)
remaining_pool = [n for n in ALL_NAMES if n not in current_names]

# Spin parameters
angle_offset = 0.0
spin_speed = 0.0
SPIN_DECAY = 0.99
MIN_SPIN_SPEED = 0.5

# Game state
winner = None          # The last chosen winner
pending_winner = None  # We only remove this from current_names on the next spin
spinning = False

def draw_wheel(names, angle_degs):
    """
    Draw the wheel so wedge 0 is physically at the top when angle_degs=0.
    We do this by subtracting 90° from the wheel’s angle in radians.
    """
    num_segments = len(names)
    if num_segments == 0:
        return

    angle_rad = math.radians(angle_degs) - math.pi / 2
    segment_angle = 2 * math.pi / num_segments

    for i, name in enumerate(names):
        start_angle = angle_rad + i * segment_angle
        end_angle = start_angle + segment_angle
        color = COLORS[i % len(COLORS)]

        # Draw the wedge as a polygon (center + points along arc)
        points = [(center_x, center_y)]
        steps = 30
        for step in range(steps + 1):
            theta = start_angle + (end_angle - start_angle) * (step / steps)
            x = center_x + radius * math.cos(theta)
            y = center_y + radius * math.sin(theta)
            points.append((x, y))

        pygame.draw.polygon(screen, color, points)

        # Draw the name roughly in the middle of the wedge
        mid_angle = (start_angle + end_angle) / 2
        text_x = center_x + (radius * 0.6) * math.cos(mid_angle)
        text_y = center_y + (radius * 0.6) * math.sin(mid_angle)
        text_surf = font.render(name, True, (0, 0, 0))
        text_rect = text_surf.get_rect(center=(text_x, text_y))
        screen.blit(text_surf, text_rect)

def pick_winner(names, final_angle):
    """
    Figure out which wedge is at the top. Because we subtracted 90° in draw_wheel,
    angle=0 means wedge 0 is exactly at top. We add half a wedge to land in the middle.
    """
    if not names:
        return None

    num_segments = len(names)
    seg_size = 360 / num_segments

    # Shift half a wedge so pointer lands in the middle
    adjusted_angle = (final_angle + seg_size / 2) % 360

    index = int(adjusted_angle // seg_size)
    return names[index]

def update_wheel(winner_name):
    """
    Actually remove the old winner from current_names and add a new one.
    (We call this right before we spin again, not immediately after picking.)
    """
    global current_names, remaining_pool

    if winner_name in current_names:
        current_names.remove(winner_name)
    if remaining_pool:
        new_name = random.choice(remaining_pool)
        remaining_pool.remove(new_name)
        current_names.append(new_name)

def main():
    global angle_offset, spin_speed, spinning
    global winner, pending_winner

    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

                elif event.key == pygame.K_SPACE:
                    # 1) If the wheel is not spinning yet:
                    if not spinning:
                        # Remove the *previous* winner's wedge (only now)
                        if pending_winner:
                            update_wheel(pending_winner)
                            pending_winner = None

                        # Start a new spin
                        spinning = True
                        winner = None
                        spin_speed = random.uniform(10, 15)

        if spinning:
            angle_offset += spin_speed
            spin_speed *= SPIN_DECAY
            if spin_speed < MIN_SPIN_SPEED:
                spinning = False
                final_angle = angle_offset % 360
                winner = pick_winner(current_names, final_angle)
                # Store the winner so we remove them next time user spins
                if winner:
                    pending_winner = winner

        # Drawing
        screen.fill((255, 255, 255))
        draw_wheel(current_names, angle_offset)

        # Draw pointer at the top
        pointer_length = 30
        pygame.draw.polygon(
            screen, (255, 0, 0),
            [
                (center_x, center_y - (radius + pointer_length)),
                (center_x - 10, center_y - radius),
                (center_x + 10, center_y - radius)
            ]
        )

        # Show winner
        if winner:
            txt = font.render(f"Winner: {winner}", True, (255, 0, 0))
            rect = txt.get_rect(center=(WIDTH // 2, HEIGHT - 50))
            screen.blit(txt, rect)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
