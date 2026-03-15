"""
Neuroevolution Maze Navigator

Controls:
    SPACE   - Pause/Resume
    R       - Reset generation
    N       - Force next generation
    F       - Toggle fast mode
    +/=     - Speed up
    -       - Slow down
    ESC     - Quit
"""

import pygame
import math
from config import Config 
from src.maze import Maze
from src.agent.agent import Agent
from src.agent.raycaster import WideRaycaster
from src.neural.neural_network import NeuralNetwork
from src.population import Population

# ============== CONFIGURATION ==============
config = Config()

SCREEN_WIDTH = config.screen_width
SCREEN_HEIGHT = config.screen_height
FPS = config.refresh_rate

# Population settings
POPULATION_SIZE = config.population_size
MAX_STEPS = config.max_steps

# Neural network: 6 inputs (5 sensors + goal angle), 8 hidden, 1 output (turn)b n
NN_SHAPE = (config.nn_input_size, config.nn_hidden_size, config.nn_output_size)

# Genetic algorithm
ELITE_COUNT = config.elite_count
MUTATION_RATE = config.mutation_rate
MUTATION_STRENGTH = config.mutation_strength
# ===========================================


def main():
    # Pygame setup
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Neuroevolution Maze Navigator")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 28)
    font_large = pygame.font.Font(None, 36)

    # Load maze
    maze = Maze("src/maze/test_maze.json")
    
    # Get start/goal positions
    start_x, start_y = maze.start
    goal_x, goal_y = maze.goal
    
    # Calculate max distance for fitness normalization
    max_distance = math.sqrt(SCREEN_WIDTH**2 + SCREEN_HEIGHT**2)

    # Create population
    population = Population(POPULATION_SIZE, start_x, start_y, NN_SHAPE)

    # Simulation state
    running = True
    paused = False
    fast_mode = False
    step_count = 0
    sim_speed = 1

    # Stats
    best_ever_fitness = 0.0

    # Print startup info
    print("=" * 50)
    print("NEUROEVOLUTION MAZE NAVIGATOR")
    print("=" * 50)
    print(f"Population: {POPULATION_SIZE}")
    print(f"Network: {NN_SHAPE}")
    print(f"Max steps: {MAX_STEPS}")
    print("=" * 50)

    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                
                elif event.key == pygame.K_SPACE:
                    paused = not paused
                    print("PAUSED" if paused else "RESUMED")
                
                elif event.key == pygame.K_r:
                    population.reset()
                    step_count = 0
                    print("Generation reset")
                
                elif event.key == pygame.K_n:
                    # Force evolution
                    population.calculate_fitness(goal_x, goal_y, max_distance)
                    population.evolve(ELITE_COUNT, MUTATION_RATE, MUTATION_STRENGTH)
                    step_count = 0
                    print(f"Forced evolution to gen {population.generation}")
                
                elif event.key == pygame.K_f:
                    fast_mode = not fast_mode
                    print(f"Fast mode: {'ON' if fast_mode else 'OFF'}")
                
                elif event.key in (pygame.K_PLUS, pygame.K_EQUALS):
                    sim_speed = min(sim_speed + 1, 20)
                    print(f"Speed: {sim_speed}x")
                
                elif event.key == pygame.K_MINUS:
                    sim_speed = max(sim_speed - 1, 1)
                    print(f"Speed: {sim_speed}x")

        # Update simulation
        if not paused:
            for _ in range(sim_speed):
                # Update all agents
                any_active = population.update(maze, goal_x, goal_y)
                step_count += 1

                # Check if generation is over
                if not any_active or step_count >= MAX_STEPS:
                    # Calculate fitness
                    population.calculate_fitness(goal_x, goal_y, max_distance)
                    
                    # Track best ever
                    if population.best_fitness > best_ever_fitness:
                        best_ever_fitness = population.best_fitness
                    
                    # Print stats
                    stats = population.get_stats()
                    print(f"Gen {stats['generation']:3d}: "
                          f"Best={stats['best_fitness']:7.1f}, "
                          f"Avg={stats['avg_fitness']:6.1f}, "
                          f"Reached={stats['reached_goal']}")
                    
                    # Evolve
                    population.evolve(ELITE_COUNT, MUTATION_RATE, MUTATION_STRENGTH)
                    step_count = 0
                    break

        # ============== RENDERING ==============
        # Background
        screen.fill((40, 40, 40))

        # Draw maze
        maze.draw(screen)

        # Draw agents (skip in fast mode)
        if not fast_mode:
            for agent in population.agents:
                if agent.alive:
                    x, y = int(agent.x), int(agent.y)
                    
                    # Color: blue (new) -> green (high fitness)
                    if agent.fitness > 0:
                        green = min(255, int(agent.fitness * 2))
                        color = (100, green, 100)
                    else:
                        color = (100, 100, 255)
                    
                    pygame.draw.circle(screen, color, (x, y), agent.radius)
                    
                    # Direction line
                    dx = math.cos(agent.direction) * 15
                    dy = math.sin(agent.direction) * 15
                    pygame.draw.line(screen, (255, 255, 255), 
                                   (x, y), (x + dx, y + dy), 2)

            # Draw rays for best agent
            best = population.get_best()
            if best and best.alive:
                population.raycaster.draw(screen, best.x, best.y,
                                         best.direction, maze.walls)

        # ============== UI ==============
        stats = population.get_stats()
        y = 10
        
        info_lines = [
            f"Generation: {stats['generation']}",
            f"Alive: {stats['alive']}/{POPULATION_SIZE}",
            f"Reached Goal: {stats['reached_goal']}",
            f"Step: {step_count}/{MAX_STEPS}",
            "",
            f"Best Fitness: {stats['best_fitness']:.1f}",
            f"Avg Fitness: {stats['avg_fitness']:.1f}",
            f"Best Ever: {best_ever_fitness:.1f}",
            "",
            f"Speed: {sim_speed}x",
        ]
        
        for line in info_lines:
            if line:
                text = font.render(line, True, (255, 255, 255))
                screen.blit(text, (10, y))
            y += 25

        # Mode indicators
        if fast_mode:
            text = font_large.render("FAST MODE", True, (255, 255, 0))
            screen.blit(text, (SCREEN_WIDTH // 2 - 70, 10))

        if paused:
            text = font_large.render("PAUSED", True, (255, 100, 100))
            screen.blit(text, (SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2))

        # Controls
        controls = "SPACE:Pause | R:Reset | N:Evolve | F:Fast | +/-:Speed | ESC:Quit"
        text = font.render(controls, True, (150, 150, 150))
        screen.blit(text, (10, SCREEN_HEIGHT - 30))

        pygame.display.flip()
        clock.tick(FPS)

    # Cleanup
    print("\n" + "=" * 50)
    print(f"Final generation: {population.generation}")
    print(f"Best ever fitness: {best_ever_fitness:.1f}")
    print("=" * 50)
    
    pygame.quit()


if __name__ == "__main__":
    main()