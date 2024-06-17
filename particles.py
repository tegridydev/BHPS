import random
import math

def initialize_particles():
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

def update_particle(particle):
    dx = SCREEN_WIDTH // 2 - particle["x"]
    dy = SCREEN_HEIGHT // 2 - particle["y"]
    r = math.sqrt(dx**2 + dy**2)
    a = GRAVITATIONAL_CONSTANT * BLACK_HOLE_MASS / r**2
    particle["vx"] += a * dx / r * TIME_STEP
    particle["vy"] += a * dy / r * TIME_STEP
    particle["x"] += particle["vx"] * TIME_STEP
    particle["y"] += particle["vy"] * TIME_STEP
    particle["trail"].append((particle["x"], particle["y"]))