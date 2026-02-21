"""
Демонстрация 2D визуализации алгоритма Dolphin Echolocation
Показывает движение дельфинов в пространстве поиска
"""

import numpy as np
import sys
sys.path.append('.')

from dolphin import DolphinEcholocation
from visualization_2d import (
    DEOVisualizer2D,
    sphere_2d,
    rastrigin_2d,
    rosenbrock_2d,
    ackley_2d,
    himmelblau
)


def demo_sphere_function():
    print("\n" + "=" * 80)
    print("ДЕМОНСТРАЦИЯ 1: Sphere Function")
    print("=" * 80)
    
    bounds = [(-5, 5), (-5, 5)]
    
    de = DolphinEcholocation(
        objective_function=sphere_2d,
        dimension=2,
        bounds=bounds,
        population_size=30,
        max_iterations=50,
        pp_initial=0.15,
        power=0.5,
        track_positions=True  
    )
    
    de.true_optimum = (0, 0)
    
    best_pos, best_fit, history = de.optimize()
    
    visualizer = DEOVisualizer2D(sphere_2d, bounds)
    
    print("\n Создание визуализации начального и финального состояния...")
    visualizer.visualize_optimization(de, save_path='../iodata/sphere_2d_optimization.png')
    
    print("\n Создание визуализации процесса конвергенции...")
    visualizer.visualize_convergence_process(de, save_path='../iodata/sphere_2d_convergence.png')
    
    return de, visualizer


def demo_rastrigin_function():
    print("\n" + "=" * 80)
    print("ДЕМОНСТРАЦИЯ 2: Rastrigin Function (сложная, многомодальная)")
    print("=" * 80)
    
    bounds = [(-5.12, 5.12), (-5.12, 5.12)]
    
    de = DolphinEcholocation(
        objective_function=rastrigin_2d,
        dimension=2,
        bounds=bounds,
        population_size=40,
        max_iterations=80,
        pp_initial=0.15,
        power=0.5,
        track_positions=True
    )
    
    de.true_optimum = (0, 0)
    
    best_pos, best_fit, history = de.optimize()
    
    visualizer = DEOVisualizer2D(rastrigin_2d, bounds)
    
    print("\n Создание визуализации...")
    visualizer.visualize_optimization(de, save_path='../iodata/rastrigin_2d_optimization.png')
    visualizer.visualize_convergence_process(de, save_path='../iodata/rastrigin_2d_convergence.png')
    
    return de, visualizer


def demo_himmelblau_function():
    print("\n" + "=" * 80)
    print("ДЕМОНСТРАЦИЯ 3: Himmelblau Function (4 глобальных минимума)")
    print("=" * 80)
    
    bounds = [(-5, 5), (-5, 5)]
    
    de = DolphinEcholocation(
        objective_function=himmelblau,
        dimension=2,
        bounds=bounds,
        population_size=35,
        max_iterations=60,
        pp_initial=0.15,
        power=0.5,
        track_positions=True
    )
    
    de.true_optimum = (3.0, 2.0)  
    
    best_pos, best_fit, history = de.optimize()
    
    visualizer = DEOVisualizer2D(himmelblau, bounds)
    
    print("\n Создание визуализации...")
    visualizer.visualize_optimization(de, save_path='../iodata/himmelblau_2d_optimization.png')
    visualizer.visualize_convergence_process(de, save_path='../iodata/himmelblau_2d_convergence.png')
    
    return de, visualizer


def compare_power_parameters_2d():
    """
    Сравнение различных значений Power на 2D функции
    """
    print("\n" + "=" * 80)
    print("СРАВНЕНИЕ ПАРАМЕТРОВ POWER В 2D")
    print("=" * 80)
    
    import matplotlib.pyplot as plt
    
    bounds = [(-5, 5), (-5, 5)]
    powers = [0.2, 0.5, 1.0, 2.0]
    
    fig, axes = plt.subplots(2, 2, figsize=(16, 14))
    axes = axes.flatten()
    
    visualizer = DEOVisualizer2D(rastrigin_2d, bounds)
    X, Y, Z = visualizer.create_contour_plot()
    
    for idx, power in enumerate(powers):
        print(f"\n--- Тестирование с Power = {power} ---")
        
        de = DolphinEcholocation(
            objective_function=rastrigin_2d,
            dimension=2,
            bounds=bounds,
            population_size=30,
            max_iterations=50,
            pp_initial=0.15,
            power=power,
            track_positions=True
        )
        
        best_pos, best_fit, history = de.optimize()
        
        ax = axes[idx]
        contour = ax.contourf(X, Y, Z, levels=50, cmap='viridis', alpha=0.6)
        ax.contour(X, Y, Z, levels=20, colors='black', alpha=0.2, linewidths=0.5)
        
        final_positions = de.position_history[-1]
        ax.scatter(final_positions[:, 0], final_positions[:, 1],
                  c='white', s=80, edgecolors='green', linewidths=2,
                  marker='o', alpha=0.8, zorder=5)
        
        ax.scatter(best_pos[0], best_pos[1], c='lime', s=300,
                  marker='*', edgecolors='black', linewidths=2, zorder=10)
        
        ax.scatter(0, 0, c='gold', s=250, marker='*',
                  edgecolors='black', linewidths=2, zorder=10)
        
        ax.set_xlabel('X', fontsize=11)
        ax.set_ylabel('Y', fontsize=11)
        ax.set_title(f'Power = {power}\nBest f = {best_fit:.4f}',
                    fontsize=12, fontweight='bold')
        ax.grid(True, alpha=0.3)
    
    plt.suptitle('Влияние параметра Power на конвергенцию\nRastrigin Function',
                fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.savefig('../iodata/power_comparison_2d.png', dpi=300, bbox_inches='tight')
    print("\n✓ Сравнение сохранено в ../iodata/power_comparison_2d.png")
    plt.show()


def create_animation_demo():
    print("\n" + "=" * 80)
    print("СОЗДАНИЕ АНИМАЦИИ")
    print("=" * 80)
    print(" Это может занять некоторое время...")
    
    bounds = [(-5, 5), (-5, 5)]
    
    de = DolphinEcholocation(
        objective_function=sphere_2d,
        dimension=2,
        bounds=bounds,
        population_size=25,
        max_iterations=40,
        pp_initial=0.15,
        power=0.5,
        track_positions=True
    )
    
    best_pos, best_fit, history = de.optimize()
    
    visualizer = DEOVisualizer2D(sphere_2d, bounds)
    
    print("\n Создание анимации...")
    try:
        visualizer.create_animation(de, save_path='../iodata/deo_animation.gif', interval=200)
    except Exception as e:
        print(f" Не удалось создать анимацию: {e}")
        print("   Возможно, нужно установить: pip install pillow")


def main():
    print("\n" + "=" * 80)
    print("2D ВИЗУАЛИЗАЦИЯ DOLPHIN ECHOLOCATION OPTIMIZATION")
    print("Демонстрация движения дельфинов в пространстве поиска")
    print("=" * 80)
    
    np.random.seed(42)
    
    de_sphere, vis_sphere = demo_sphere_function()
    
    de_rastrigin, vis_rastrigin = demo_rastrigin_function()
    
    de_himmelblau, vis_himmelblau = demo_himmelblau_function()
    
    compare_power_parameters_2d()
    
    create_animation_demo()
    
    print("\n" + "=" * 80)
    print("ВСЕ ДЕМОНСТРАЦИИ ЗАВЕРШЕНЫ!")
    print("=" * 80)
    print("\n Созданные файлы:")
    print("   - ../iodata/sphere_2d_optimization.png")
    print("   - ../iodata/sphere_2d_convergence.png")
    print("   - ../iodata/rastrigin_2d_optimization.png")
    print("   - ../iodata/rastrigin_2d_convergence.png")
    print("   - ../iodata/himmelblau_2d_optimization.png")
    print("   - ../iodata/himmelblau_2d_convergence.png")
    print("   - ../iodata/power_comparison_2d.png")
    print("   - ../iodata/deo_animation.gif")
    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()