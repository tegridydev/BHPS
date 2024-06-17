import random
import math
from io import BytesIO
from PIL import Image, ImageDraw

class ParticleSimulation:
    def __init__(self):
        self.SCREEN_WIDTH = 1350
        self.SCREEN_HEIGHT = 750
        self.BLACK_HOLE_MASS = 40 * 10**15
        self.BLACK_HOLE_RADIUS = 25
        self.GRAVITATIONAL_CONSTANT = 6.67430e-11
        self.TIME_STEP = 0.003
        self.PARTICLE_COUNT = 200

    def initialize_particles(self):
        """Initialize particles with random positions, velocities, and masses."""
        particles = []
        for _ in range(self.PARTICLE_COUNT):
            pradius = random.uniform(2, 8)
            mass = random.uniform(2 * 10**8, 4 * 10**15)
            particles.append({
                "x": random.randint(0, self.SCREEN_WIDTH),
                "y": random.randint(0, self.SCREEN_HEIGHT),
                "vx": random.uniform(-10, 10),
                "vy": random.uniform(-10, 10),
                "mass": mass,
                "radius": pradius,
                "color": (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),
                "trail": []
            })
        return particles

    def update_particle(self, particle, black_hole_x, black_hole_y):
        """Update the position and velocity of a particle."""
        dx = black_hole_x - particle["x"]
        dy = black_hole_y - particle["y"]
        r = math.sqrt(dx**2 + dy**2)
        a = self.GRAVITATIONAL_CONSTANT * self.BLACK_HOLE_MASS / r**2
        particle["vx"] += a * dx / r * self.TIME_STEP
        particle["vy"] += a * dy / r * self.TIME_STEP
        particle["x"] += particle["vx"] * self.TIME_STEP
        particle["y"] += particle["vy"] * self.TIME_STEP
        particle["trail"].append((particle["x"], particle["y"]))

    def run_simulation(self):
        """Run the simulation and return the screen as an image."""
        particles = self.initialize_particles()
        black_hole_x, black_hole_y = self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2

        for _ in range(60):  # Run the simulation for 60 frames
            for particle in particles:
                self.update_particle(particle, black_hole_x, black_hole_y)
        
        # Create an in-memory image
        image = Image.new('RGB', (self.SCREEN_WIDTH, self.SCREEN_HEIGHT), (0, 0, 0))
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

# Example usage (if running standalone)
if __name__ == '__main__':
    simulation = ParticleSimulation()
    image_bytes = simulation.run_simulation()
    # Optionally save or display image_bytes as needed
