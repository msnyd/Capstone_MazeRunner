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



Main simulation module for MazeRunner.
 
Implements:
    REQ-6.1: Configurable FPS
    REQ-6.2: Speed multiplier (1x-20x)
    REQ-6.3: SPACE pause/resume
    REQ-6.4: R key reset
    REQ-6.5: N key force evolution
    REQ-6.6: F key fast mode
    REQ-6.7: +/- speed adjustment
    REQ-6.8: ESC return to menu
    REQ-6.9: Auto-evolution triggers
    REQ-6.10: Best-ever fitness tracking
    
    REQ-7.1: Agent rendering (circles)
    REQ-7.2: Fitness-based coloring
    REQ-7.3: Selected agent highlight
    REQ-7.4: HUD display
    REQ-7.5: PAUSED text
    REQ-7.6: FAST MODE text
    REQ-7.7: Controls reference

"""

import pygame
import math
import numpy as np

from config import Config 
from src.agent import agent
from maze import Maze
from src.agent.agent import Agent
from src.agent.raycaster import WideRaycaster
from src.agent.raycaster import CornerRaycaster
from src.neural.neural_network import NeuralNetwork
from src.population import Population
from menu_screen import run_menu
from setting_screen import run_settings
from network_popup import NetworkPopup


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


class Simulation:
    def __init__(self, screen, config):
        """
        Initialize simulation with screen, config, maze, and population.
        
        Implements: REQ-6.1, REQ-6.10
        """
        self.screen = screen
        self.config = config
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 28)
        self.font_large = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 22)
        self.selected_agent = None

        # Load maze
        maze_file = f"src/maze_{config.difficulty}.json"
        self.maze = Maze(maze_file)
        
        # Get start/goal positions
        self.start_x, self.start_y = self.maze.start
        self.goal_x, self.goal_y = self.maze.goal
        
        # Calculate max distance for fitness normalization
        self.max_distance = math.sqrt(SCREEN_WIDTH**2 + SCREEN_HEIGHT**2)

        # Create population
        self.population = Population(self.config.population_size, self.start_x, self.start_y, NN_SHAPE)

        # Simulation state
        self.paused = False
        self.fast_mode = False
        self.step_count = 0
        self.sim_speed = 1

        # Stats
        self.best_ever_fitness = 0.0

        self.net_popup = NetworkPopup(SCREEN_WIDTH, SCREEN_HEIGHT)
        selected_agent = None


        # Print startup info
        print("=" * 50)
        print("NEUROEVOLUTION MAZE NAVIGATOR")
        print("=" * 50)
        print(f"Population: {self.config.population_size}")
        print(f"Network: {NN_SHAPE}")
        print(f"Max steps: {self.config.max_steps}")
        print("=" * 50)

    def run_simulation(self):
        """
        Main simulation loop: handle events, update agents, render.
        
        Implements: REQ-6.2 through REQ-6.9, REQ-7.1 through REQ-7.7
        """
        running = True
        while running:
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                # Handle popup close events
                if self.net_popup.visible:
                    if event.type == pygame.KEYDOWN:
                        if event.key in (pygame.K_ESCAPE, pygame.K_b):
                            self.net_popup.hide()
                            self.selected_agent = None
                            self.paused = False
                            continue
                    # Mouse events fall through to agent selection below
                
                # Keyboard events (when popup is NOT visible)
                if event.type == pygame.KEYDOWN and not self.net_popup.visible:
                    if event.key == pygame.K_ESCAPE:
                        return  # Return to menu
                    
                    elif event.key == pygame.K_SPACE:
                        self.paused = not self.paused
                        print("PAUSED" if self.paused else "RESUMED")
                    
                    elif event.key == pygame.K_r:
                        self.population.reset()
                        self.step_count = 0
                        self.selected_agent = None
                        print("Generation reset")
                    
                    elif event.key == pygame.K_n:
                        self.population.calculate_fitness(self.goal_x, self.goal_y, self.max_distance)
                        self.population.evolve(ELITE_COUNT, MUTATION_RATE, MUTATION_STRENGTH)
                        self.step_count = 0
                        self.selected_agent = None
                        print(f"Forced evolution to gen {self.population.generation}")
                    
                    elif event.key == pygame.K_f:
                        self.fast_mode = not self.fast_mode
                        print(f"Fast mode: {'ON' if self.fast_mode else 'OFF'}")
                    
                    elif event.key in (pygame.K_PLUS, pygame.K_EQUALS):
                        self.sim_speed = min(self.sim_speed + 1, 20)
                        print(f"Speed: {self.sim_speed}x")
                    
                    elif event.key == pygame.K_MINUS:
                        self.sim_speed = max(self.sim_speed - 1, 1)
                        print(f"Speed: {self.sim_speed}x")

                # Mouse click - works whether popup is open or not
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left click
                        mouse_x, mouse_y = event.pos
                        
                        # Check if clicked on any agent
                        clicked_agent = None
                        for agent in self.population.agents:
                            if agent.alive:
                                dist = math.sqrt((mouse_x - agent.x)**2 + (mouse_y - agent.y)**2)
                                if dist <= agent.radius + 5:
                                    clicked_agent = agent
                                    break
                        
                        if clicked_agent:
                            self.selected_agent = clicked_agent
                            self.net_popup.show(clicked_agent)
                            # self.paused = True
                            print(f"Viewing agent - Fitness: {clicked_agent.fitness:.1f}")
                        elif self.net_popup.visible:
                            # Clicked empty space - close popup
                            self.net_popup.hide()
                            self.selected_agent = None
                            self.paused = False

            # Update simulation
            if not self.paused:
                for _ in range(self.sim_speed):
                    # Update all agents
                    any_active, is_stagnant = self.population.update(self.maze, self.goal_x, self.goal_y)
                    self.step_count += 1

                    # Check if generation is over
                    if not any_active or self.step_count >= self.config.max_steps or is_stagnant:
                        # Calculate fitness
                        if is_stagnant:
                            print(f" -> stagnation detected, ending early at step {self.step_count}")
                        self.population.calculate_fitness(self.goal_x, self.goal_y, self.max_distance)
                        
                        
                        # Track best ever
                        if self.population.best_fitness > self.best_ever_fitness:
                            self.best_ever_fitness = self.population.best_fitness
                        
                        # Print stats
                        stats = self.population.get_stats()
                        print(f"Gen {stats['generation']:3d}: "
                              f"Best={stats['best_fitness']:7.1f}, "
                              f"Avg={stats['avg_fitness']:6.1f}, "
                              f"Reached={stats['reached_goal']}")
                        
                        # Evolve
                        self.population.evolve(self.config.elite_count, self.config.mutation_rate, self.config.mutation_strength)
                        self.step_count = 0
                        break

            # ============== RENDERING ==============
            # Background
            self.screen.fill((40, 40, 40))

            # Draw maze
            self.maze.draw(self.screen)

            # Draw agents (skip in fast mode)
            if not self.fast_mode:
                for agent in self.population.agents:
                    if agent.alive:
                        x, y = int(agent.x), int(agent.y)

                        if agent == self.selected_agent:
                            pygame.draw.circle(self.screen, (255, 255, 0), (x, y), agent.radius + 5, 3)
                            color = (255, 255, 100)
                        elif agent.fitness > 0:
                            green = min(255, int(agent.fitness * 2))
                            color = (100, green, 100)
                        else:
                            color = (100, 100, 255)


                        pygame.draw.circle(self.screen, color, (x, y), agent.radius)
                        
                        # Direction line
                        dx = math.cos(agent.direction) * 15
                        dy = math.sin(agent.direction) * 15
                        pygame.draw.line(self.screen, (255, 255, 255), 
                                       (x, y), (x + dx, y + dy), 2)

                # Draw rays for best agent
                best = self.population.get_best()
                if best and best.alive:
                    self.population.raycaster.draw(self.screen, best.x, best.y,
                                             best.direction, self.maze.walls)
                    


            # ============== UI ==============
            stats = self.population.get_stats()
            y = 10
            
            info_lines = [
                f"Generation: {stats['generation']}",
                f"Alive: {stats['alive']}/{self.config.population_size}",
                f"Reached Goal: {stats['reached_goal']}",
                f"Step: {self.step_count}/{self.config.max_steps}",
                "",
                f"Best Fitness: {stats['best_fitness']:.1f}",
                f"Avg Fitness: {stats['avg_fitness']:.1f}",
                f"Best Ever: {self.best_ever_fitness:.1f}",
                "",
                f"Speed: {self.sim_speed}x",
            ]
            
            for line in info_lines:
                if line:
                    text = self.font.render(line, True, (255, 255, 255))
                    self.screen.blit(text, (10, y))
                y += 25

            # Mode indicators
            if self.fast_mode:
                text = self.font_large.render("FAST MODE", True, (255, 255, 0))
                self.screen.blit(text, (SCREEN_WIDTH // 2 - 70, 10))

            if self.paused:
                text = self.font_large.render("PAUSED", True, (255, 100, 100))
                self.screen.blit(text, (SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2))

            # Controls
            controls = "SPACE:Pause | R:Reset | N:Evolve | F:Fast | +/-:Speed | ESC:Menu"
            text = self.font.render(controls, True, (150, 150, 150))
            self.screen.blit(text, (10, SCREEN_HEIGHT - 30))

            if self.net_popup.visible:
                self.net_popup.draw(self.screen, self.goal_x, self.goal_y)

            pygame.display.flip()
            self.clock.tick(FPS)

        # If running is False, quit
        pygame.quit()
        exit()


def main():
    # Pygame setup
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Neuroevolution Maze Navigator")
    

    while True:
        state = run_menu(screen, config)
        if state == "start":
            sim = Simulation(screen, config)
            sim.run_simulation()
        elif state == "settings":
            run_settings(screen, config)
        elif state == "quit":
            break

    pygame.quit()


if __name__ == "__main__":
    main()
