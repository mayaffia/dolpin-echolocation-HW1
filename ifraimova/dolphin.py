
import numpy as np
import matplotlib.pyplot as plt
from typing import Callable, Tuple, List
import time


class Dolphin:
    
    def __init__(self, dimension: int, bounds: List[Tuple[float, float]]):
        self.dimension = dimension
        self.bounds = bounds
        self.position = np.array([
            np.random.uniform(bounds[i][0], bounds[i][1]) 
            for i in range(dimension)
        ])
        self.fitness = float('inf')
        self.velocity = np.zeros(dimension)
        
    def evaluate(self, objective_function: Callable) -> float:
        self.fitness = objective_function(self.position)
        return self.fitness
    
    def update_position(self, new_position: np.ndarray):
        for i in range(self.dimension):
            self.position[i] = np.clip(new_position[i], 
                                      self.bounds[i][0], 
                                      self.bounds[i][1])


class DolphinEcholocation:
    
    def __init__(self,
                 objective_function: Callable,
                 dimension: int,
                 bounds: List[Tuple[float, float]],
                 population_size: int = 30,
                 max_iterations: int = 100,
                 convergence_curve: bool = True,
                 pp_initial: float = 0.15,
                 power: float = 0.5,
                 re_initial: float = None,
                 track_positions: bool = False):
      
        self.objective_function = objective_function
        self.dimension = dimension
        self.bounds = bounds
        self.population_size = population_size
        self.max_iterations = max_iterations
        self.convergence_curve = convergence_curve
        
     
        self.pp_initial = pp_initial 
        self.power = power 
        
        if re_initial is None:
            search_space_size = np.mean([bounds[i][1] - bounds[i][0] for i in range(dimension)])
            self.re_initial = 0.25 * search_space_size
        else:
            self.re_initial = re_initial
        
        self.dolphins = [Dolphin(dimension, bounds) for _ in range(population_size)]
        
        self.best_position = None
        self.best_fitness = float('inf')
        self.convergence_history = []
        self.pp_history = [] 
        self.cf_history = [] 
        
        self.track_positions = track_positions
        self.position_history = [] if track_positions else None
        
        self.iteration_count = 0
        self.function_evaluations = 0
        
    def initialize_population(self):
        for dolphin in self.dolphins:
            fitness = dolphin.evaluate(self.objective_function)
            self.function_evaluations += 1
            
            if fitness < self.best_fitness:
                self.best_fitness = fitness
                self.best_position = dolphin.position.copy()
    
    def calculate_pp(self, iteration: int) -> float:
        if self.max_iterations <= 1:
            return 1.0
        
        loop_i = iteration + 1
        pp = self.pp_initial + (1 - self.pp_initial) * \
             ((loop_i - 1) / (self.max_iterations - 1)) ** self.power
        
        return pp
    
    def calculate_accumulative_fitness(self, iteration: int) -> np.ndarray:
        re = self.re_initial * (1 - iteration / self.max_iterations)
        
        af = np.zeros(self.population_size)
        
        for i, dolphin_i in enumerate(self.dolphins):
            for j, dolphin_j in enumerate(self.dolphins):
                distance = np.linalg.norm(dolphin_i.position - dolphin_j.position)
                
                if distance < re:
                    influence = (1 / re) * (re - distance) if re > 0 else 0
                    
                    fitness_contribution = 1.0 / (1.0 + dolphin_j.fitness)
                    
                    af[i] += influence * fitness_contribution
        
        epsilon = 1e-10
        af = af + epsilon
        
        return af
    
    def calculate_convergence_factor(self) -> float:
        if not self.dolphins:
            return 0.0
        
        close_count = 0
        threshold = self.re_initial * 0.1 
        
        for dolphin in self.dolphins:
            distance = np.linalg.norm(dolphin.position - self.best_position)
            if distance < threshold:
                close_count += 1
        
        cf = (close_count / self.population_size) * 100
        return cf
    
    def calculate_location_quality(self, dolphin: Dolphin) -> float:
        if self.best_fitness == 0:
            return 1.0
        return 1.0 / (1.0 + dolphin.fitness / self.best_fitness)
    
    def update_dolphin_position(self, dolphin: Dolphin, iteration: int, af_value: float):
        pp = self.calculate_pp(iteration)
        
        re = self.re_initial * (1 - iteration / self.max_iterations)
        
        global_component = pp * (self.best_position - dolphin.position)
        
        random_direction = np.random.uniform(-1, 1, self.dimension)
        local_component = (1 - pp) * af_value * re * random_direction
        
        neighbor_idx = np.random.randint(0, self.population_size)
        neighbor = self.dolphins[neighbor_idx]
        social_weight = 0.1 * (1 - pp) 
        social_component = social_weight * (neighbor.position - dolphin.position)
        
        new_position = dolphin.position + global_component + local_component + social_component
        
        dolphin.update_position(new_position)
    
    def optimize(self) -> Tuple[np.ndarray, float, List[float]]:
        print("=" * 70)
        print("Enhanced Dolphin Echolocation Optimization")
        print("Based on: Kaveh & Farhoudi (2013)")
        print("=" * 70)
        print(f"Population size (NL): {self.population_size}")
        print(f"Max iterations: {self.max_iterations}")
        print(f"Dimensions: {self.dimension}")
        print(f"Initial PP (PP_1): {self.pp_initial:.2f}")
        print(f"Power parameter: {self.power:.2f}")
        print(f"Initial effective radius (Re): {self.re_initial:.4f}")
        print("-" * 70)
        
        start_time = time.time()
    
        self.initialize_population()
        
        if self.convergence_curve:
            self.convergence_history.append(self.best_fitness)
            self.pp_history.append(self.pp_initial)
            self.cf_history.append(0.0)
        
        if self.track_positions:
            positions = np.array([d.position for d in self.dolphins])
            self.position_history.append(positions.copy())
        
        print(f"Initial best fitness: {self.best_fitness:.6e}")
        
        for iteration in range(self.max_iterations):
            self.iteration_count = iteration + 1
            
            pp = self.calculate_pp(iteration)
            
            af_values = self.calculate_accumulative_fitness(iteration)
            
            af_sum = np.sum(af_values)
            if af_sum > 0:
                af_normalized = af_values / af_sum
            else:
                af_normalized = np.ones(self.population_size) / self.population_size
            
            for idx, dolphin in enumerate(self.dolphins):
                self.update_dolphin_position(dolphin, iteration, af_normalized[idx])
                
                fitness = dolphin.evaluate(self.objective_function)
                self.function_evaluations += 1
                
                if fitness < self.best_fitness:
                    self.best_fitness = fitness
                    self.best_position = dolphin.position.copy()
            
            if self.convergence_curve:
                self.convergence_history.append(self.best_fitness)
                self.pp_history.append(pp)
                cf = self.calculate_convergence_factor()
                self.cf_history.append(cf)
            
            if self.track_positions:
                positions = np.array([d.position for d in self.dolphins])
                self.position_history.append(positions.copy())
            
            if (iteration + 1) % 10 == 0 or iteration == 0:
                re_current = self.re_initial * (1 - iteration / self.max_iterations)
                print(f"Iter {iteration + 1:3d}/{self.max_iterations}: "
                      f"Best = {self.best_fitness:.6e} | "
                      f"PP = {pp:.3f} | "
                      f"Re = {re_current:.4f}")
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        print("-" * 70)
        print(f"✓ Optimization completed in {execution_time:.2f} seconds")
        print(f"✓ Total function evaluations: {self.function_evaluations}")
        print(f"✓ Final best fitness: {self.best_fitness:.6e}")
        print(f"✓ Best position: {self.best_position}")
        print("=" * 70)
        
        return self.best_position, self.best_fitness, self.convergence_history
    
    def plot_convergence(self, save_path: str = None):
        if not self.convergence_history:
            print("No convergence data to plot.")
            return
        
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle('Enhanced Dolphin Echolocation Optimization - Analysis',
                     fontsize=16, fontweight='bold')
        
        iterations = range(len(self.convergence_history))
        
        ax1 = axes[0, 0]
        ax1.plot(iterations, self.convergence_history, 'b-', linewidth=2, label='Best Fitness')
        ax1.set_xlabel('Iteration', fontsize=11)
        ax1.set_ylabel('Best Fitness (log scale)', fontsize=11)
        ax1.set_title('Convergence Curve', fontsize=12, fontweight='bold')
        ax1.grid(True, alpha=0.3)
        ax1.set_yscale('log')
        ax1.legend()
        
        ax2 = axes[0, 1]
        if self.pp_history:
            ax2.plot(iterations, self.pp_history, 'g-', linewidth=2, label='PP (Actual)')
            theoretical_pp = [self.calculate_pp(i) for i in range(len(iterations))]
            ax2.plot(iterations, theoretical_pp, 'g--', linewidth=1.5,
                    alpha=0.7, label='PP (Theoretical)')
        ax2.set_xlabel('Iteration', fontsize=11)
        ax2.set_ylabel('Predefined Probability (PP)', fontsize=11)
        ax2.set_title('PP Curve (Eq. 1 from paper)', fontsize=12, fontweight='bold')
        ax2.grid(True, alpha=0.3)
        ax2.set_ylim([0, 1.05])
        ax2.legend()
        
        ax3 = axes[1, 0]
        if self.cf_history:
            ax3.plot(iterations, self.cf_history, 'r-', linewidth=2, label='CF (Actual)')
            if self.pp_history:
                pp_percentage = [p * 100 for p in self.pp_history]
                ax3.plot(iterations, pp_percentage, 'g--', linewidth=1.5,
                        alpha=0.7, label='PP × 100')
        ax3.set_xlabel('Iteration', fontsize=11)
        ax3.set_ylabel('Convergence Factor (%)', fontsize=11)
        ax3.set_title('Convergence Factor vs PP', fontsize=12, fontweight='bold')
        ax3.grid(True, alpha=0.3)
        ax3.set_ylim([0, 105])
        ax3.legend()
        
        ax4 = axes[1, 1]
        re_values = [self.re_initial * (1 - i / max(1, self.max_iterations - 1))
                     for i in range(len(iterations))]
        ax4.plot(iterations, re_values, 'm-', linewidth=2, label='Re')
        ax4.set_xlabel('Iteration', fontsize=11)
        ax4.set_ylabel('Effective Radius (Re)', fontsize=11)
        ax4.set_title('Effective Radius Decay', fontsize=12, fontweight='bold')
        ax4.grid(True, alpha=0.3)
        ax4.legend()
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"✓ Convergence plots saved to {save_path}")
        
        plt.show()
    
    def plot_pp_curve_comparison(self, powers: List[float] = None):
        if powers is None:
            powers = [0.2, 0.5, 1.0, 2.0]
        
        plt.figure(figsize=(10, 6))
        
        iterations = np.linspace(0, self.max_iterations - 1, 100)
        
        for power in powers:
            pp_values = []
            for i in iterations:
                loop_i = i + 1
                pp = self.pp_initial + (1 - self.pp_initial) * \
                     ((loop_i - 1) / (self.max_iterations - 1)) ** power
                pp_values.append(pp)
            
            plt.plot(iterations, pp_values, linewidth=2, label=f'Power = {power}')
        
        plt.xlabel('Iteration', fontsize=12)
        plt.ylabel('Predefined Probability (PP)', fontsize=12)
        plt.title('PP Curve Comparison for Different Power Values\n' +
                 f'(PP_1 = {self.pp_initial}, Max Iterations = {self.max_iterations})',
                 fontsize=14, fontweight='bold')
        plt.grid(True, alpha=0.3)
        plt.legend(fontsize=11)
        plt.ylim([0, 1.05])
        
        plt.text(0.02, 0.98, 'Lower Power → More Exploration\nHigher Power → Faster Convergence',
                transform=plt.gca().transAxes, fontsize=10,
                verticalalignment='top', bbox=dict(boxstyle='round',
                facecolor='wheat', alpha=0.5))
        
        plt.tight_layout()
        plt.show()


def sphere_function(x: np.ndarray) -> float:
    return np.sum(x**2)


def rastrigin_function(x: np.ndarray) -> float:
    n = len(x)
    return 10 * n + np.sum(x**2 - 10 * np.cos(2 * np.pi * x))


def rosenbrock_function(x: np.ndarray) -> float:
    return np.sum(100 * (x[1:] - x[:-1]**2)**2 + (1 - x[:-1])**2)


def ackley_function(x: np.ndarray) -> float:
    n = len(x)
    sum1 = np.sum(x**2)
    sum2 = np.sum(np.cos(2 * np.pi * x))
    return -20 * np.exp(-0.2 * np.sqrt(sum1 / n)) - np.exp(sum2 / n) + 20 + np.e


if __name__ == "__main__":
    print("Dolphin Echolocation Algorithm - Test Run")
    print("=" * 60)
    
    dimension = 10
    bounds = [(-100, 100)] * dimension
    
    de = DolphinEcholocation(
        objective_function=sphere_function,
        dimension=dimension,
        bounds=bounds,
        population_size=30,
        max_iterations=100
    )
    
    best_pos, best_fit, history = de.optimize()
    de.plot_convergence()