// Simulation parameters (default values)
let particleCount = 100;
let initialVelocityRange = { min: -1, max: 1 };

// Canvas setup
const canvas = document.getElementById('simulationCanvas');
const ctx = canvas.getContext('2d');

// Adjust canvas dimensions based on viewport
function adjustCanvasSize() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
}

// Particle class
class Particle {
    constructor(x, y, vx, vy) {
        this.x = x;
        this.y = y;
        this.vx = vx;
        this.vy = vy;
        this.color = `rgb(${Math.random() * 255}, ${Math.random() * 255}, ${Math.random() * 255})`; // Random color
    }

    // Update particle position
    update() {
        this.x += this.vx;
        this.y += this.vy;

        // Bounce off edges
        if (this.x < 0 || this.x > canvas.width) {
            this.vx *= -1;
        }
        if (this.y < 0 || this.y > canvas.height) {
            this.vy *= -1;
        }
    }

    // Draw particle on canvas
    draw() {
        ctx.beginPath();
        ctx.arc(this.x, this.y, 3, 0, Math.PI * 2);
        ctx.fillStyle = this.color;
        ctx.fill();
    }
}

// Array to hold particles
let particles = [];

// Initialize particles
function initParticles() {
    particles = [];
    for (let i = 0; i < particleCount; i++) {
        const x = Math.random() * canvas.width;
        const y = Math.random() * canvas.height;
        const vx = initialVelocityRange.min + Math.random() * (initialVelocityRange.max - initialVelocityRange.min);
        const vy = initialVelocityRange.min + Math.random() * (initialVelocityRange.max - initialVelocityRange.min);
        particles.push(new Particle(x, y, vx, vy));
    }
}

// Update particles and draw on canvas
function updateAndDraw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    particles.forEach(particle => {
        particle.update();
        particle.draw();
    });
    requestAnimationFrame(updateAndDraw);
}

// Initialize simulation
function initializeSimulation() {
    adjustCanvasSize();
    initParticles();
    updateAndDraw();
}

// Handle window resize
window.addEventListener('resize', adjustCanvasSize);

// Start simulation when the DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    initializeSimulation();
});

// Function to update parameters from HTML
function updateParameters(count, velocityMin, velocityMax) {
    particleCount = count;
    initialVelocityRange.min = velocityMin;
    initialVelocityRange.max = velocityMax;

    // Reinitialize particles with updated parameters
    initParticles();
}
