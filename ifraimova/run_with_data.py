"""
Script to run Dolphin Echolocation algorithm with input data and save results.
This demonstrates the complete workflow: input → processing → output
"""

import numpy as np
import json
import time
from datetime import datetime
from dolphin import DolphinEcholocation, sphere_function, rastrigin_function, rosenbrock_function

def save_results_to_file(results, filename):
    filepath = f"../iodata/{filename}"
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("DOLPHIN ECHOLOCATION ALGORITHM - EXECUTION RESULTS\n")
        f.write("=" * 80 + "\n\n")
        
        f.write(f"Execution Date: {results['timestamp']}\n")
        f.write(f"Function: {results['function_name']}\n")
        f.write(f"Dimension: {results['dimension']}\n")
        f.write(f"Population Size: {results['population_size']}\n")
        f.write(f"Max Iterations: {results['max_iterations']}\n\n")
        
        f.write("-" * 80 + "\n")
        f.write("RESULTS\n")
        f.write("-" * 80 + "\n\n")
        
        f.write(f"Best Fitness: {results['best_fitness']:.10e}\n\n")
        
        f.write("Best Position:\n")
        for i, val in enumerate(results['best_position']):
            f.write(f"  x[{i}] = {val:.10e}\n")
        
        f.write(f"\nExecution Time: {results['execution_time']:.4f} seconds\n")
        f.write(f"Function Evaluations: {results['function_evaluations']}\n\n")
        
        f.write("-" * 80 + "\n")
        f.write("CONVERGENCE HISTORY (First 20 and Last 10 iterations)\n")
        f.write("-" * 80 + "\n\n")
        
        history = results['convergence_history']
        for i in range(min(20, len(history))):
            f.write(f"Iteration {i:3d}: {history[i]:.10e}\n")
        
        if len(history) > 30:
            f.write("...\n")
            for i in range(len(history) - 10, len(history)):
                f.write(f"Iteration {i:3d}: {history[i]:.10e}\n")
        
        f.write("\n" + "=" * 80 + "\n")
        f.write("END OF RESULTS\n")
        f.write("=" * 80 + "\n")
    
    print(f"Results saved to: {filepath}")

def run_optimization_test():
    print("=" * 80)
    print("DOLPHIN ECHOLOCATION ALGORITHM - TEST RUN")
    print("=" * 80)
    print()
    
    test_configs = [
        {
            'name': 'Sphere Function Test',
            'function': sphere_function,
            'function_name': 'Sphere',
            'dimension': 10,
            'bounds': [(-100, 100)] * 10,
            'population_size': 30,
            'max_iterations': 100,
            'output_file': 'results_sphere.txt'
        },
        {
            'name': 'Rastrigin Function Test',
            'function': rastrigin_function,
            'function_name': 'Rastrigin',
            'dimension': 10,
            'bounds': [(-5.12, 5.12)] * 10,
            'population_size': 30,
            'max_iterations': 100,
            'output_file': 'results_rastrigin.txt'
        },
        {
            'name': 'Rosenbrock Function Test',
            'function': rosenbrock_function,
            'function_name': 'Rosenbrock',
            'dimension': 10,
            'bounds': [(-5, 10)] * 10,
            'population_size': 30,
            'max_iterations': 100,
            'output_file': 'results_rosenbrock.txt'
        }
    ]
    
    all_results = []
    
    for config in test_configs:
        print(f"\n{'=' * 80}")
        print(f"Running: {config['name']}")
        print(f"{'=' * 80}\n")
        
        de = DolphinEcholocation(
            objective_function=config['function'],
            dimension=config['dimension'],
            bounds=config['bounds'],
            population_size=config['population_size'],
            max_iterations=config['max_iterations']
        )
        
        start_time = time.time()
        best_position, best_fitness, convergence_history = de.optimize()
        execution_time = time.time() - start_time
        
        results = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'function_name': config['function_name'],
            'dimension': config['dimension'],
            'population_size': config['population_size'],
            'max_iterations': config['max_iterations'],
            'best_fitness': best_fitness,
            'best_position': best_position.tolist(),
            'execution_time': execution_time,
            'function_evaluations': de.function_evaluations,
            'convergence_history': convergence_history
        }
        
        save_results_to_file(results, config['output_file'])
        
        all_results.append(results)
        
        print(f"\n {config['name']} completed!")
        print(f"   Best fitness: {best_fitness:.10e}")
        print(f"   Execution time: {execution_time:.4f} seconds")
    
    print(f"\n{'=' * 80}")
    print("Creating summary file...")
    print(f"{'=' * 80}\n")
    
    summary_file = "../iodata/results_summary.txt"
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("DOLPHIN ECHOLOCATION ALGORITHM - SUMMARY OF ALL TESTS\n")
        f.write("=" * 80 + "\n\n")
        f.write(f"Execution Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Total Tests Run: {len(all_results)}\n\n")
        
        f.write("-" * 80 + "\n")
        f.write("PERFORMANCE COMPARISON\n")
        f.write("-" * 80 + "\n\n")
        
        f.write(f"{'Function':<15} {'Best Fitness':<20} {'Time (s)':<12} {'Evaluations':<12}\n")
        f.write("-" * 80 + "\n")
        
        for result in all_results:
            f.write(f"{result['function_name']:<15} "
                   f"{result['best_fitness']:<20.6e} "
                   f"{result['execution_time']:<12.4f} "
                   f"{result['function_evaluations']:<12}\n")
        
        f.write("\n" + "=" * 80 + "\n")
        f.write("DETAILED RESULTS\n")
        f.write("=" * 80 + "\n\n")
        
        for result in all_results:
            f.write(f"\n{result['function_name']} Function:\n")
            f.write(f"  Best Fitness: {result['best_fitness']:.10e}\n")
            f.write(f"  Execution Time: {result['execution_time']:.4f} seconds\n")
            f.write(f"  Function Evaluations: {result['function_evaluations']}\n")
            f.write(f"  Final Convergence: {result['convergence_history'][-1]:.10e}\n")
            f.write(f"  Improvement: {result['convergence_history'][0]:.6e} → {result['convergence_history'][-1]:.6e}\n")
        
        f.write("\n" + "=" * 80 + "\n")
        f.write("END OF SUMMARY\n")
        f.write("=" * 80 + "\n")
    
    print(f"Summary saved to: {summary_file}")
    
    print(f"\n{'=' * 80}")
    print("ALL TESTS COMPLETED SUCCESSFULLY!")
    print(f"{'=' * 80}\n")
    print(f"Results saved in iodata/ folder:")
    for config in test_configs:
        print(f"  - {config['output_file']}")
    print(f"  - results_summary.txt")
    print()

if __name__ == "__main__":
    run_optimization_test()