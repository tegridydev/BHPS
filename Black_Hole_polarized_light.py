import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Set up the screen
screen_size = (1800, 1000)
screen = pygame.display.set_mode(screen_size)

# Define the black hole
black_hole_pos = (900, 500)
black_hole_radius = 40
black_hole_mass = 1.989 * 10**7
event_horizon_radius = 2 * black_hole_radius

# Define the photons
photons = []
for i in range(200):
    photons.append({
        "pos": (1800, i*6),
        "velocity": (-2, 0),
        "color": (5, 45, 5),
        "trail": []
    })

# Define the gravitational constant
G = 0.01

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    screen.fill((0, 0, 0))

    # Draw the black hole
    pygame.draw.circle(screen, (0, 0, 0), black_hole_pos, event_horizon_radius, 0) 
    pygame.draw.circle(screen, (0, 0, 0), black_hole_pos, black_hole_radius, 1) 

    # Update the photons
    for photon in photons:
        # Calculate the distance between the photon and the black hole
        distance = math.sqrt((photon["pos"][0] - black_hole_pos[0])**2 + (photon["pos"][1] - black_hole_pos[1])**2)

        # Check if the photon is within the event horizon
        if distance < event_horizon_radius:
            # The photon is within the event horizon and will be captured by the black hole
            photon["color"] = (234, 180, 80)
        else:
            # The photon is outside the event horizon and will continue to move under the influence of gravity
            force = G * black_hole_mass / distance**2
            force_direction = math.atan2(black_hole_pos[1] - photon["pos"][1], black_hole_pos[0] - photon["pos"][0])

            # Update the velocity of the photon
            scaling_factor = 0.1
            photon["velocity"] = (photon["velocity"][0] + scaling_factor * force * math.cos(force_direction), photon["velocity"][1] + scaling_factor * force * math.sin(force_direction))

            # Update the position of the photon
            photon["pos"] = (photon["pos"][0] + photon["velocity"][0], photon["pos"][1] + photon["velocity"][1])

            # Add the current position to the trail
            photon["trail"].append(photon["pos"])

            # Draw the photon
            pygame.draw.circle(screen, photon["color"], (int(photon["pos"][0]), int(photon["pos"][1])), 2)

            # Draw the trail
            for i in range(1, len(photon["trail"])):
                pygame.draw.aaline(screen, photon["color"], photon["trail"][i-1], photon["trail"][i])

    # Update the screen
    pygame.display.update()

# Quit Pygame
pygame.quit()