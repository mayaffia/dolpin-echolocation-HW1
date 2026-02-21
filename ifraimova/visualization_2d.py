"""
2D визуализация процесса оптимизации Dolphin Echolocation
Показывает движение дельфинов в пространстве поиска
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Circle
import matplotlib.cm as cm
from typing import Callable, List, Tuple


class DEOVisualizer2D:
    
    def __init__(self, objective_function: Callable, bounds: List[Tuple[float, float]]):
        self.objective_function = objective_function
        self.bounds = bounds
        self.history = [] 
        
    def create_contour_plot(self, resolution: int = 100):
        x = np.linspace(self.bounds[0][0], self.bounds[0][1], resolution)
        y = np.linspace(self.bounds[1][0], self.bounds[1][1], resolution)
        X, Y = np.meshgrid(x, y)
        
        Z = np.zeros_like(X)
        for i in range(resolution):
            for j in range(resolution):
                Z[i, j] = self.objective_function(np.array([X[i, j], Y[i, j]]))
        
        return X, Y, Z
    
    def visualize_optimization(self, 
                              de_algorithm,
                              save_path: str = None,
                              show_re: bool = True,
                              show_best_path: bool = True):

        if not hasattr(de_algorithm, 'position_history'):
            print("История позиций не сохранена. Используйте track_positions=True")
            return
        
        fig, axes = plt.subplots(1, 2, figsize=(16, 7))
        
        X, Y, Z = self.create_contour_plot()
        
        ax1 = axes[0]
        contour1 = ax1.contourf(X, Y, Z, levels=50, cmap='viridis', alpha=0.6)
        ax1.contour(X, Y, Z, levels=20, colors='black', alpha=0.2, linewidths=0.5)
     
        initial_positions = de_algorithm.position_history[0]
        ax1.scatter(initial_positions[:, 0], initial_positions[:, 1], 
                   c='white', s=100, edgecolors='red', linewidths=2,
                   marker='o', label='Начальные позиции', zorder=5)
        
        if hasattr(de_algorithm, 'true_optimum'):
            ax1.scatter(*de_algorithm.true_optimum, c='gold', s=300, 
                       marker='*', edgecolors='black', linewidths=2,
                       label='Глобальный оптимум', zorder=10)
        
        ax1.set_xlabel('X', fontsize=12)
        ax1.set_ylabel('Y', fontsize=12)
        ax1.set_title('Начальное состояние', fontsize=13, fontweight='bold')
        ax1.legend(loc='upper right')
        ax1.grid(True, alpha=0.3)
        plt.colorbar(contour1, ax=ax1, label='Fitness')
        
        ax2 = axes[1]
        contour2 = ax2.contourf(X, Y, Z, levels=50, cmap='viridis', alpha=0.6)
        ax2.contour(X, Y, Z, levels=20, colors='black', alpha=0.2, linewidths=0.5)
        
        final_positions = de_algorithm.position_history[-1]
        ax2.scatter(final_positions[:, 0], final_positions[:, 1],
                   c='white', s=100, edgecolors='green', linewidths=2,
                   marker='o', label='Финальные позиции', zorder=5)
        
        best_pos = de_algorithm.best_position
        ax2.scatter(best_pos[0], best_pos[1], c='lime', s=400,
                   marker='o', edgecolors='black', linewidths=3,
                   label=f'Лучшее решение\n(f={de_algorithm.best_fitness:.4f})',
                   zorder=10)
        
        if show_re:
            final_re = de_algorithm.re_initial * (1 - (de_algorithm.max_iterations - 1) / de_algorithm.max_iterations)
            circle = Circle((best_pos[0], best_pos[1]), final_re,
                          fill=False, edgecolor='lime', linewidth=2,
                          linestyle='--', label=f'Re финальный = {final_re:.2f}', zorder=8)
            ax2.add_patch(circle)
        
        if hasattr(de_algorithm, 'true_optimum'):
            ax2.scatter(*de_algorithm.true_optimum, c='gold', s=300,
                       marker='*', edgecolors='black', linewidths=2,
                       label='Глобальный оптимум', zorder=10)
        
        ax2.set_xlabel('X', fontsize=12)
        ax2.set_ylabel('Y', fontsize=12)
        ax2.set_title(f'Финальное состояние (итерация {de_algorithm.max_iterations})',
                     fontsize=13, fontweight='bold')
        ax2.legend(loc='upper right')
        ax2.grid(True, alpha=0.3)
        plt.colorbar(contour2, ax=ax2, label='Fitness')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Визуализация сохранена в {save_path}")
        
        plt.show()
    
    def visualize_convergence_process(self,
                                     de_algorithm,
                                     iterations_to_show: List[int] = None,
                                     save_path: str = None):
        if not hasattr(de_algorithm, 'position_history'):
            print("История позиций не сохранена")
            return
        
        if iterations_to_show is None:
            total = len(de_algorithm.position_history)
            iterations_to_show = [0, total//5, 2*total//5, 3*total//5, 4*total//5, total-1]
        
        n_plots = len(iterations_to_show)
        fig, axes = plt.subplots(2, 3, figsize=(18, 12))
        axes = axes.flatten()
        
        X, Y, Z = self.create_contour_plot()
        
        for idx, iteration in enumerate(iterations_to_show):
            ax = axes[idx]
            
            contour = ax.contourf(X, Y, Z, levels=50, cmap='viridis', alpha=0.6)
            ax.contour(X, Y, Z, levels=20, colors='black', alpha=0.2, linewidths=0.5)
            
            positions = de_algorithm.position_history[iteration]
            
            fitnesses = []
            for pos in positions:
                fitnesses.append(self.objective_function(pos))
            fitnesses = np.array(fitnesses)
            
            if fitnesses.max() > fitnesses.min():
                colors = (fitnesses - fitnesses.min()) / (fitnesses.max() - fitnesses.min())
            else:
                colors = np.ones_like(fitnesses)
            
            scatter = ax.scatter(positions[:, 0], positions[:, 1],
                               c=colors, s=100, cmap='coolwarm',
                               edgecolors='black', linewidths=1.5,
                               marker='o', zorder=5, vmin=0, vmax=1)
            
            best_idx = np.argmin(fitnesses)
            ax.scatter(positions[best_idx, 0], positions[best_idx, 1],
                      c='lime', s=300, marker='*',
                      edgecolors='black', linewidths=2, zorder=10)
            
            if iteration > 0:
                re = de_algorithm.re_initial * (1 - iteration / de_algorithm.max_iterations)
                circle = Circle((positions[best_idx, 0], positions[best_idx, 1]), re,
                              fill=False, edgecolor='lime', linewidth=1.5,
                              linestyle='--', alpha=0.7, zorder=8)
                ax.add_patch(circle)
            
            pp = de_algorithm.calculate_pp(iteration)
            
            ax.set_xlabel('X', fontsize=10)
            ax.set_ylabel('Y', fontsize=10)
            ax.set_title(f'Итерация {iteration}\nPP = {pp:.3f}, Best f = {fitnesses[best_idx]:.4f}',
                        fontsize=11, fontweight='bold')
            ax.grid(True, alpha=0.3)
        
        fig.colorbar(scatter, ax=axes, label='Нормализованный Fitness', 
                    orientation='horizontal', pad=0.05, aspect=40)
        
        plt.suptitle('Процесс конвергенции Dolphin Echolocation',
                    fontsize=16, fontweight='bold', y=0.98)
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Процесс конвергенции сохранен в {save_path}")
        
        plt.show()
    
    def create_animation(self,
                        de_algorithm,
                        save_path: str = None,
                        interval: int = 200):
        if not hasattr(de_algorithm, 'position_history'):
            print("История позиций не сохранена")
            return
        
        fig, ax = plt.subplots(figsize=(10, 8))
        
        X, Y, Z = self.create_contour_plot()
        
        contour = ax.contourf(X, Y, Z, levels=50, cmap='viridis', alpha=0.6)
        ax.contour(X, Y, Z, levels=20, colors='black', alpha=0.2, linewidths=0.5)
        plt.colorbar(contour, ax=ax, label='Fitness')

        scatter = ax.scatter([], [], c='white', s=100, edgecolors='red',
                           linewidths=2, marker='o', zorder=5)
        best_scatter = ax.scatter([], [], c='lime', s=300, marker='*',
                                 edgecolors='black', linewidths=2, zorder=10)
        
        title = ax.text(0.5, 1.05, '', transform=ax.transAxes,
                       ha='center', fontsize=12, fontweight='bold')
        
        ax.set_xlabel('X', fontsize=12)
        ax.set_ylabel('Y', fontsize=12)
        ax.grid(True, alpha=0.3)
        
        def init():
            scatter.set_offsets(np.empty((0, 2)))
            best_scatter.set_offsets(np.empty((0, 2)))
            return scatter, best_scatter, title
        
        def update(frame):
            positions = de_algorithm.position_history[frame]
            scatter.set_offsets(positions)
            
            fitnesses = np.array([self.objective_function(pos) for pos in positions])
            best_idx = np.argmin(fitnesses)
            best_scatter.set_offsets(positions[best_idx:best_idx+1])
            
            pp = de_algorithm.calculate_pp(frame)
            title.set_text(f'Итерация {frame}/{len(de_algorithm.position_history)-1} | '
                          f'PP = {pp:.3f} | Best f = {fitnesses[best_idx]:.4f}')
            
            return scatter, best_scatter, title
        
        anim = FuncAnimation(fig, update, init_func=init,
                           frames=len(de_algorithm.position_history),
                           interval=interval, blit=True, repeat=True)
        
        if save_path:
            anim.save(save_path, writer='pillow', fps=5)
            print(f"Анимация сохранена в {save_path}")
        
        plt.show()
        return anim


def sphere_2d(x):
    return x[0]**2 + x[1]**2


def rastrigin_2d(x):
    return 20 + x[0]**2 - 10*np.cos(2*np.pi*x[0]) + x[1]**2 - 10*np.cos(2*np.pi*x[1])


def rosenbrock_2d(x):
    return 100*(x[1] - x[0]**2)**2 + (1 - x[0])**2


def ackley_2d(x):
    return -20*np.exp(-0.2*np.sqrt(0.5*(x[0]**2 + x[1]**2))) - \
           np.exp(0.5*(np.cos(2*np.pi*x[0]) + np.cos(2*np.pi*x[1]))) + 20 + np.e


def himmelblau(x):
    return (x[0]**2 + x[1] - 11)**2 + (x[0] + x[1]**2 - 7)**2