import os
import pygame
import random
import math
import numpy as np
from typing import List, Dict, Tuple

# Constants
SCREEN_WIDTH = 1800
SCREEN_HEIGHT = 1000
BLACK_HOLE_MASS = 40 * 10**15
BLACK_HOLE_RADIUS = 25
GRAVITATIONAL_CONSTANT = 6.67430e-11
SPEED_OF_LIGHT = 299792458
THETA = 8.8 * 10**26
SCALE_FACTOR = 10000
TIME_STEP = 0.003
PARTICLE_COUNT = 200

def initialize_particles() -> List[Dict[str, float]]:
    """Initialize particles with random positions, velocities, and masses."""
    particles = []
    for _ in range(PARTICLE_COUNT):
        pradius = random.uniform(2, 8)
        mass = random.uniform(2 * 10**8, 4 * 10**15)
        particles.append({
            "x": random.randint(0, SCREEN_WIDTH),
            "y": random.randint(0, SCREEN_HEIGHT),
            "vx": random.uniform(-10, 10),
            "vy": random.uniform(-10, 10),
            "mass": mass,
            "radius": pradius,
            "color": (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),
            "trail": []
        })
    return particles

def update_particle(particle: Dict[str, float], black_hole_x: float, black_hole_y: float) -> None:
    """Update the position and velocity of a particle."""
    dx = black_hole_x - particle["x"]
    dy = black_hole_y - particle["y"]
    r = math.sqrt(dx**2 + dy**2)
    a = GRAVITATIONAL_CONSTANT * BLACK_HOLE_MASS / r**2
    particle["vx"] += a * dx / r * TIME_STEP
    particle["vy"] += a * dy / r * TIME_STEP
    particle["x"] += particle["vx"] * TIME_STEP / SCALE_FACTOR
    particle["y"] += particle["vy"] * TIME_STEP / SCALE_FACTOR
    particle["trail"].append((particle["x"], particle["y"]))

def draw_particle(screen: pygame.Surface, particle: Dict[str, float]) -> None:
    """Draw a particle and its trail on the screen."""
    pygame.draw.circle(screen, particle["color"], (int(particle["x"]), int(particle["y"])), int(particle["radius"]))
    for i in range(1, len(particle["trail"])):
        pygame.draw.aaline(screen, particle["color"], particle["trail"][i - 1], particle["trail"][i])

def main() -> None:
    """Main function to run the simulation."""
    # Set SDL to use the dummy audio driver, which doesn't require a sound card
    os.environ["SDL_AUDIODRIVER"] = "dummy"
    
    # Initialize Pygame
    pygame.init()
    
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    particles = initialize_particles()
    black_hole_x, black_hole_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))
        pygame.draw.circle(screen, (255, 255, 255), (black_hole_x, black_hole_y), BLACK_HOLE_RADIUS)

        for particle in particles:
            update_particle(particle, black_hole_x, black_hole_y)
            draw_particle(screen, particle)

        pygame.display.flip()
        clock.tick(60)  # Limit to 60 frames per second

    pygame.quit()

if __name__ == "__main__":
    main()
