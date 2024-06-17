from flask import Flask, render_template, request
from bhps.main import ParticleSimulation
from bhps.config import SCREEN_WIDTH, SCREEN_HEIGHT, BLACK_HOLE_MASS, BLACK_HOLE_RADIUS, GRAVITATIONAL_CONSTANT, TIME_STEP, PARTICLE_COUNT

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/simulation')
def simulation():
    simulation = ParticleSimulation()
    image_bytes = simulation.run_simulation()
    return send_file(image_bytes, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)