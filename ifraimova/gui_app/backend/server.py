"""
Flask backend server for Dolphin Echolocation GUI Application
Simplified version without SocketIO for better compatibility
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import numpy as np
import sys
import os

# Add parent directory to path to import dolphin module
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

try:
    from dolphin import DolphinEcholocation, sphere_function, rastrigin_function, rosenbrock_function
except ImportError as e:
    print(f"Error importing dolphin module: {e}")
    print(f"Current path: {os.getcwd()}")
    print(f"Sys path: {sys.path}")
    sys.exit(1)

app = Flask(__name__)
CORS(app)

# Global state for optimization
optimization_state = {
    'optimizer': None,
    'function_name': 'sphere',
    'parameters': {}
}

# Available test functions
FUNCTIONS = {
    'sphere': {
        'func': sphere_function,
        'bounds': (-100, 100),
        'name': 'Sphere Function',
        'formula': 'f(x) = Σ(xi²)'
    },
    'rastrigin': {
        'func': rastrigin_function,
        'bounds': (-5.12, 5.12),
        'name': 'Rastrigin Function',
        'formula': 'f(x) = 10n + Σ(xi² - 10cos(2πxi))'
    },
    'rosenbrock': {
        'func': rosenbrock_function,
        'bounds': (-5, 10),
        'name': 'Rosenbrock Function',
        'formula': 'f(x) = Σ(100(xi+1 - xi²)² + (1-xi)²)'
    }
}


class SteppableDolphinEcholocation(DolphinEcholocation):
    """Extended Dolphin Echolocation that supports step-by-step execution"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initialized = False
        
    def initialize(self):
        """Initialize population without running optimization"""
        self.initialize_population()
        self.initialized = True
        
        if self.convergence_curve:
            self.convergence_history.append(self.best_fitness)
            self.pp_history.append(self.pp_initial)
            self.cf_history.append(0.0)
        
        if self.track_positions:
            positions = np.array([d.position for d in self.dolphins])
            self.position_history.append(positions.copy())
        
        return self.get_state()
    
    def step(self):
        """Execute one iteration of the algorithm"""
        if not self.initialized:
            return None
        
        if self.iteration_count >= self.max_iterations:
            return None
        
        iteration = self.iteration_count
        
        # Calculate PP
        pp = self.calculate_pp(iteration)
        
        # Calculate accumulative fitness
        af_values = self.calculate_accumulative_fitness(iteration)
        af_sum = np.sum(af_values)
        if af_sum > 0:
            af_normalized = af_values / af_sum
        else:
            af_normalized = np.ones(self.population_size) / self.population_size
        
        # Update each dolphin
        for idx, dolphin in enumerate(self.dolphins):
            self.update_dolphin_position(dolphin, iteration, af_normalized[idx])
            fitness = dolphin.evaluate(self.objective_function)
            self.function_evaluations += 1
            
            if fitness < self.best_fitness:
                self.best_fitness = fitness
                self.best_position = dolphin.position.copy()
        
        # Update history
        if self.convergence_curve:
            self.convergence_history.append(self.best_fitness)
            self.pp_history.append(pp)
            cf = self.calculate_convergence_factor()
            self.cf_history.append(cf)
        
        if self.track_positions:
            positions = np.array([d.position for d in self.dolphins])
            self.position_history.append(positions.copy())
        
        self.iteration_count += 1
        
        return self.get_state()
    
    def get_state(self):
        """Get current state of optimization"""
        return {
            'iteration': self.iteration_count,
            'best_fitness': float(self.best_fitness),
            'best_position': self.best_position.tolist() if self.best_position is not None else None,
            'agent_positions': [[float(x) for x in d.position] for d in self.dolphins],
            'agent_fitness': [float(d.fitness) for d in self.dolphins],
            'convergence_history': [float(x) for x in self.convergence_history],
            'pp': float(self.calculate_pp(self.iteration_count - 1)) if self.iteration_count > 0 else float(self.pp_initial),
            'completed': self.iteration_count >= self.max_iterations
        }


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'ok', 'message': 'Server is running'})


@app.route('/api/functions', methods=['GET'])
def get_functions():
    """Get list of available test functions"""
    return jsonify({
        'functions': {
            key: {
                'name': val['name'],
                'formula': val['formula'],
                'bounds': val['bounds']
            }
            for key, val in FUNCTIONS.items()
        }
    })


@app.route('/api/initialize', methods=['POST'])
def initialize_optimization():
    """Initialize optimization with given parameters"""
    data = request.json
    
    function_name = data.get('function', 'sphere')
    dimension = data.get('dimension', 2)
    population_size = data.get('population_size', 20)
    max_iterations = data.get('max_iterations', 50)
    
    if function_name not in FUNCTIONS:
        return jsonify({'error': 'Invalid function name'}), 400
    
    func_info = FUNCTIONS[function_name]
    bounds = [func_info['bounds']] * dimension
    
    # Create optimizer
    optimizer = SteppableDolphinEcholocation(
        objective_function=func_info['func'],
        dimension=dimension,
        bounds=bounds,
        population_size=population_size,
        max_iterations=max_iterations,
        convergence_curve=True,
        track_positions=True
    )
    
    # Initialize
    state = optimizer.initialize()
    
    # Store in global state
    optimization_state['optimizer'] = optimizer
    optimization_state['function_name'] = function_name
    optimization_state['parameters'] = {
        'dimension': dimension,
        'population_size': population_size,
        'max_iterations': max_iterations,
        'bounds': func_info['bounds']
    }
    
    return jsonify({
        'status': 'initialized',
        'state': state,
        'parameters': optimization_state['parameters']
    })


@app.route('/api/step', methods=['POST'])
def step_optimization():
    """Execute one step of optimization"""
    optimizer = optimization_state.get('optimizer')
    
    if optimizer is None:
        return jsonify({'error': 'Optimizer not initialized'}), 400
    
    state = optimizer.step()
    
    if state is None:
        return jsonify({'status': 'completed', 'message': 'Optimization finished'})
    
    return jsonify({
        'status': 'success',
        'state': state
    })


@app.route('/api/reset', methods=['POST'])
def reset_optimization():
    """Reset optimization state"""
    optimization_state['optimizer'] = None
    optimization_state['function_name'] = 'sphere'
    optimization_state['parameters'] = {}
    
    return jsonify({'status': 'reset'})


@app.route('/api/evaluate_grid', methods=['POST'])
def evaluate_grid():
    """Evaluate function on a 2D grid for visualization"""
    data = request.json
    function_name = data.get('function', 'sphere')
    fixed_vars = data.get('fixed_vars', {})
    var_indices = data.get('var_indices', [0, 1])
    resolution = data.get('resolution', 50)
    
    if function_name not in FUNCTIONS:
        return jsonify({'error': 'Invalid function name'}), 400
    
    func_info = FUNCTIONS[function_name]
    func = func_info['func']
    bounds = func_info['bounds']
    
    # Create grid
    x_range = np.linspace(bounds[0], bounds[1], resolution)
    y_range = np.linspace(bounds[0], bounds[1], resolution)
    X, Y = np.meshgrid(x_range, y_range)
    
    # Get dimension from optimizer or use default
    dimension = optimization_state.get('parameters', {}).get('dimension', 2)
    
    # Evaluate function on grid
    Z = np.zeros_like(X)
    for i in range(resolution):
        for j in range(resolution):
            point = np.zeros(dimension)
            
            # Set fixed variables
            for idx, val in fixed_vars.items():
                point[int(idx)] = val
            
            # Set variable dimensions
            point[var_indices[0]] = X[i, j]
            point[var_indices[1]] = Y[i, j]
            
            Z[i, j] = func(point)
    
    return jsonify({
        'x': x_range.tolist(),
        'y': y_range.tolist(),
        'z': Z.tolist(),
        'bounds': bounds
    })


if __name__ == '__main__':
    print("=" * 70)
    print("Dolphin Echolocation GUI Server")
    print("=" * 70)
    print("Server starting on http://localhost:5000")
    print("React frontend should connect to this server")
    print("=" * 70)
    app.run(debug=True, host='0.0.0.0', port=5000)