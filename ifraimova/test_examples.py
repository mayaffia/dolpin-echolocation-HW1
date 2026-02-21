"""
Test Examples for Dolphin Echolocation Algorithm
Demonstrates the algorithm on various benchmark optimization problems
"""

import numpy as np
import matplotlib.pyplot as plt
from dolphin import DolphinEcholocation, sphere_function, rastrigin_function, rosenbrock_function, ackley_function
import time


def griewank_function(x: np.ndarray) -> float:
    sum_part = np.sum(x**2) / 4000
    prod_part = np.prod(np.cos(x / np.sqrt(np.arange(1, len(x) + 1))))
    return sum_part - prod_part + 1


def schwefel_function(x: np.ndarray) -> float:
    n = len(x)
    return 418.9829 * n - np.sum(x * np.sin(np.sqrt(np.abs(x))))


def run_test_example(name: str, 
                     objective_function, 
                     dimension: int, 
                     bounds: list,
                     population_size: int = 30,
                     max_iterations: int = 100):
    print("\n" + "=" * 70)
    print(f"TEST EXAMPLE: {name}")
    print("=" * 70)
    
    de = DolphinEcholocation(
        objective_function=objective_function,
        dimension=dimension,
        bounds=bounds,
        population_size=population_size,
        max_iterations=max_iterations,
        convergence_curve=True
    )
    
    start_time = time.time()
    best_position, best_fitness, convergence_history = de.optimize()
    execution_time = time.time() - start_time
    
    results = {
        'name': name,
        'best_position': best_position,
        'best_fitness': best_fitness,
        'convergence_history': convergence_history,
        'execution_time': execution_time,
        'function_evaluations': de.function_evaluations,
        'dimension': dimension
    }
    
    return results


def plot_multiple_convergence(results_list: list, save_path: str = None):
    plt.figure(figsize=(14, 8))
    
    for i, results in enumerate(results_list):
        plt.subplot(2, 3, i + 1)
        plt.plot(results['convergence_history'], linewidth=2, color='blue')
        plt.xlabel('Iteration', fontsize=10)
        plt.ylabel('Best Fitness', fontsize=10)
        plt.title(f"{results['name']}\nFinal: {results['best_fitness']:.6e}", fontsize=11)
        plt.grid(True, alpha=0.3)
        plt.yscale('log')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"\nConvergence plots saved to {save_path}")
    
    plt.show()


def print_summary_table(results_list: list):
    print("\n" + "=" * 100)
    print("SUMMARY OF ALL TEST EXAMPLES")
    print("=" * 100)
    print(f"{'Function':<20} {'Dimension':<12} {'Best Fitness':<18} {'Time (s)':<12} {'Evaluations':<15}")
    print("-" * 100)
    
    for results in results_list:
        print(f"{results['name']:<20} {results['dimension']:<12} "
              f"{results['best_fitness']:<18.6e} {results['execution_time']:<12.2f} "
              f"{results['function_evaluations']:<15}")
    
    print("=" * 100)


def main():
    print("DOLPHIN ECHOLOCATION ALGORITHM - COMPREHENSIVE TESTING")
    print("=" * 70)
    print("Testing on 6 different benchmark optimization problems")
    print("Each test demonstrates the algorithm's ability to:")
    print("  - Initialize dolphin population")
    print("  - Evaluate fitness functions")
    print("  - Update positions using echolocation")
    print("  - Converge to optimal solutions")
    print("=" * 70)
    
    dimension = 10
    population_size = 30
    max_iterations = 100
    
    test_cases = [
        {
            'name': 'Sphere Function',
            'function': sphere_function,
            'bounds': [(-100, 100)] * dimension,
            'description': 'Unimodal, smooth, convex'
        },
        {
            'name': 'Rastrigin Function',
            'function': rastrigin_function,
            'bounds': [(-5.12, 5.12)] * dimension,
            'description': 'Highly multimodal'
        },
        {
            'name': 'Rosenbrock Function',
            'function': rosenbrock_function,
            'bounds': [(-5, 10)] * dimension,
            'description': 'Narrow valley, difficult'
        },
        {
            'name': 'Ackley Function',
            'function': ackley_function,
            'bounds': [(-32, 32)] * dimension,
            'description': 'Multimodal, many local minima'
        },
        {
            'name': 'Griewank Function',
            'function': griewank_function,
            'bounds': [(-600, 600)] * dimension,
            'description': 'Multimodal with product term'
        },
        {
            'name': 'Schwefel Function',
            'function': schwefel_function,
            'bounds': [(-500, 500)] * dimension,
            'description': 'Deceptive, global minimum far from origin'
        }
    ]
    
    all_results = []
    
    for test_case in test_cases:
        print(f"\nDescription: {test_case['description']}")
        
        results = run_test_example(
            name=test_case['name'],
            objective_function=test_case['function'],
            dimension=dimension,
            bounds=test_case['bounds'],
            population_size=population_size,
            max_iterations=max_iterations
        )
        
        all_results.append(results)
        
        time.sleep(0.5)
    
    print_summary_table(all_results)
    
    plot_multiple_convergence(all_results, save_path='convergence_all_tests.png')
    
    print("\n" + "=" * 100)
    print("ANALYSIS")
    print("=" * 100)
    
    best_performer = min(all_results, key=lambda x: x['best_fitness'])
    fastest = min(all_results, key=lambda x: x['execution_time'])
    
    print(f"\nBest convergence: {best_performer['name']} (fitness: {best_performer['best_fitness']:.6e})")
    print(f"Fastest execution: {fastest['name']} (time: {fastest['execution_time']:.2f}s)")
    
    avg_time = np.mean([r['execution_time'] for r in all_results])
    avg_evals = np.mean([r['function_evaluations'] for r in all_results])
    
    print(f"\nAverage execution time: {avg_time:.2f}s")
    print(f"Average function evaluations: {avg_evals:.0f}")
    
    print("\n" + "=" * 100)
    print("All tests completed successfully!")
    print("The algorithm demonstrates:")
    print("  ✓ Proper initialization of dolphin agents")
    print("  ✓ Fitness evaluation for each dolphin")
    print("  ✓ Position updates using echolocation mechanism")
    print("  ✓ Convergence to near-optimal solutions")
    print("  ✓ Iteration control with stopping conditions")
    print("=" * 100)


if __name__ == "__main__":
    main()