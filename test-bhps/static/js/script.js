document.addEventListener('DOMContentLoaded', () => {
    const canvas = document.getElementById('simulationCanvas');
    const ctx = canvas.getContext('2d');
    let animationFrameId;
    let isSimulationRunning = false;

    function adjustCanvasSize() {
        canvas.width = window.innerWidth * 0.8;
        canvas.height = window.innerHeight * 0.8;
    }

    function drawParticles(particles) {
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        for (const particle of particles) {
            ctx.beginPath();
            ctx.arc(particle.x, particle.y, particle.radius, 0, 2 * Math.PI);
            ctx.fillStyle = `rgb(${particle.color[0]}, ${particle.color[1]}, ${particle.color[2]})`;
            ctx.fill();

            for (let i = 1; i < particle.trail.length; i++) {
                ctx.beginPath();
                ctx.moveTo(particle.trail[i - 1].x, particle.trail[i - 1].y);
                ctx.lineTo(particle.trail[i].x, particle.trail[i].y);
                ctx.strokeStyle = `rgb(${particle.color[0]}, ${particle.color[1]}, ${particle.color[2]})`;
                ctx.stroke();
            }
        }
    }

    function updateParticles(particles, blackHoleX, blackHoleY) {
        for (const particle of particles) {
            const dx = blackHoleX - particle.x;
            const dy = blackHoleY - particle.y;
            const r = Math.sqrt(dx ** 2 + dy ** 2);
            const a = (6.67430e-11 * 40 * 10 ** 15) / (r ** 2);
            particle.vx += a * dx / r * 0.003;
            particle.vy += a * dy / r * 0.003;
            particle.x += particle.vx * 0.003;
            particle.y += particle.vy * 0.003;
            particle.trail.push({ x: particle.x, y: particle.y });
            if (particle.trail.length > 50) {
                particle.trail.shift();
            }
        }
    }

    function initializeSimulation() {
        adjustCanvasSize();
        const particles = [];
        for (let i = 0; i < 200; i++) {
            const x = Math.random() * canvas.width;
            const y = Math.random() * canvas.height;
            const vx = (Math.random() - 0.5) * 20;
            const vy = (Math.random() - 0.5) * 20;
            const radius = Math.random() * 5 + 2;
            const color = [Math.random() * 255, Math.random() * 255, Math.random() * 255];
            particles.push({ x, y, vx, vy, radius, color, trail: [] });
        }

        function animateSimulation() {
            updateParticles(particles, canvas.width / 2, canvas.height / 2);
            drawParticles(particles);
            animationFrameId = requestAnimationFrame(animateSimulation);
        }

        animateSimulation();
        return particles;
    }

    function startSimulation() {
        if (!isSimulationRunning) {
            particles = initializeSimulation();
            isSimulationRunning = true;
        }
    }

    function stopSimulation() {
        if (isSimulationRunning) {
            cancelAnimationFrame(animationFrameId);
            isSimulationRunning = false;
        }
    }

    document.getElementById('startButton').addEventListener('click', startSimulation);
    document.getElementById('stopButton').addEventListener('click', stopSimulation);
    window.addEventListener('resize', adjustCanvasSize);
});