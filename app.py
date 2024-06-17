import os
import random
import math
from io import BytesIO
from flask import Flask, send_file, render_template, request
from flask_bootstrap import Bootstrap
from PIL import Image, ImageDraw

# Constants
SCREEN_WIDTH = 1350
SCREEN_HEIGHT = 750
BLACK_HOLE_MASS = 40 * 10**15
BLACK_HOLE_RADIUS = 25
GRAVITATIONAL_CONSTANT = 6.67430e-11
TIME_STEP = 0.003
PARTICLE_COUNT = 200

def initialize_particles():
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

def update_particle(particle, black_hole_x, black_hole_y):
    """Update the position and velocity of a particle."""
    dx = black_hole_x - particle["x"]
    dy = black_hole_y - particle["y"]
    r = math.sqrt(dx**2 + dy**2)
    a = GRAVITATIONAL_CONSTANT * BLACK_HOLE_MASS / r**2
    particle["vx"] += a * dx / r * TIME_STEP
    particle["vy"] += a * dy / r * TIME_STEP
    particle["x"] += particle["vx"] * TIME_STEP
    particle["y"] += particle["vy"] * TIME_STEP
    particle["trail"].append((particle["x"], particle["y"]))

def run_simulation():
    """Run the simulation and return the screen as an image."""
    particles = initialize_particles()
    black_hole_x, black_hole_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2

    for _ in range(60):  # Run the simulation for 60 frames
        for particle in particles:
            update_particle(particle, black_hole_x, black_hole_y)
    
    # Create an in-memory image
    image = Image.new('RGB', (SCREEN_WIDTH, SCREEN_HEIGHT), (0, 0, 0))
    draw = ImageDraw.Draw(image)

    # Draw particles on the image
    for particle in particles:
        color = particle["color"]
        position = (int(particle["x"]), int(particle["y"]))
        radius = int(particle["radius"])
        draw.ellipse((position[0] - radius, position[1] - radius, position[0] + radius, position[1] + radius), fill=color)

    # Save image to BytesIO object
    image_bytes = BytesIO()
    image.save(image_bytes, format='PNG')
    image_bytes.seek(0)

    return image_bytes

app = Flask(__name__)
bootstrap = Bootstrap(app)

# Routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/simulation')
def simulation():
    image_bytes = run_simulation()
    return send_file(image_bytes, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
