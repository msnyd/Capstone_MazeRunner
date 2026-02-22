from src.agent.agent import Agent
from src.agent.raycaster import WideRaycaster
from src.neural.neural_network import NeuralNetwork
from typing import List, Tuple
import math


class Population:
    def __init__(self, size: int, start_x: float, start_y: float, 
                 nn_shape: Tuple[int, ...] = (6, 8, 1)):
        """
        Creates a population of agents.
        All agents start at the same starting point of the maze.
        
        :param size: The total amount of agents in the population.
        :param start_x: starting x coordinate
        :param start_y: starting y coordinate
        """
        self.size = size
        self.start_x = start_x
        self.start_y = start_y
        self.nn_shape = nn_shape

        self.agents: List[Agent] = []
        for _ in range(size):
            agent = Agent(start_x, start_y, direction=0.0)
            agent.brain = NeuralNetwork(self.nn_shape)
            self.agents.append(agent)


        # Shared WideRaycaster for all agents
        self.raycaster = WideRaycaster(max_range=150)

        # Will keep track of which generation the population is on.
        self.generation = 1

        # If we decide that agents die, this will keep track.
        self.generation = 1
        self.alive_count = size
        self.best_fitness = 0.0
        self.avg_fitness = 0.0

    def update(self, maze, goal_x, goal_y, sensor_range=150):
        """
        Update all the agents within the population.
        Returns True if there is ANY agent that is still alive.
        
        :param maze: Maze object
        :param goal_x: X coordinate of goal
        :param goal_y: Y coordinate of goal
        :param sensor_range: Max sensor distance for raycaster
        """
        any_alive = False

        for agent in self.agents:
            if agent.alive and not agent.reached_goal:
                agent.update(maze, goal_x, goal_y, sensor_range, self.raycaster)
                any_alive = True
            
        self.alive_count = sum(i.alive for i in self.agents)
        return any_alive

    def draw(self, screen, draw_best_only=False):
        """
        Draws all agents onto the screen.
        """
        if draw_best_only:
            best = self.get_best()
            if best:
                best.draw(screen)
        else:
            for agent in self.agents:
                if agent.alive:
                    agent.draw(screen)
    

    def draw_rays(self, screen, best_only=True):
        """Draw raycaster visualization for the best agent"""
        if best_only:
            best = self.get_best()
            if best and best.alive:
                self.raycaster.draw(screen, best.x, best.y, best.direction, [])
            
            else:
                for agent in self.agents:
                    if agent.alive:
                        self.raycaster.draw(screen, agent.x, agent.y, agent.direction, [])
        
    
    def reset(self):
        """
        Reset all agents back to the starting position.
        """
        for agent in self.agents:
            agent.reset()
        self.alive_count = self.size
    
    def calculate_fitness(self, goal_x: float, goal_y: float, max_distance: float):
        """
        Assigns a fitness score based on the distance to the goal.
        """
        for agent in self.agents:
            dist = agent.distance_to(goal_x, goal_y)
            normalized_dist = dist / max_distance
            fitness = (1 - normalized_dist) ** 2 * 100

            if agent.reached_goal: #fat bonus for reaching goal
                fitness += 1000
                fitness += max(0, 500 - agent.steps_taken)  # faster = better

            agent.fitness = fitness

        fitnesses = [a.fitness for a in self.agents]
        self.best_fitness = max(fitnesses)
        self.avg_fitness = sum(fitnesses) / len(fitnesses)

    def get_best(self) -> Agent:
        """Returns the agent with the highest fitness"""
        return max(self.agents, key=lambda a: a.fitness)

    def get_sorted(self) -> List[Agent]:
        """
        Returns a list of agents sorted by fitness"""
        return sorted(self.agents, key=lambda a: a.fitness, reverse=True)
    
    def is_generation_over(self):
        """
        Checks if all agents either died or reached the goal.
        """
        return all((not a.alive) or a.reached_goal for a in self.agents)

    def get_stats(self) -> dict:
        """
        Returns current gen stats
        """
        reached = sum(a.reached_goal for a in self.agents)
        return {
            'generation': self.generation,
            'alive': self.alive_count,
            'reached_goal': reached,
            'best_fitness': self.best_fitness,
            'avg_fitness': self.avg_fitness
        }
    def evolve(self, elite_count: int = 5, mutation_rate: float =0.1, mutation_strength=0.3):
        """
        Create next generation using GA

        Args:
            elite_count: Number of top agents to keep unchanged
            mutation_rate: probability of mutating each gene
            mutation_strength: stdev of mutation noise
        """
        sorted_agents = self.get_sorted()

        new_agents: List[Agent] = []

        #Elitism - keep top performers
        for i in range(elite_count):
            agent = Agent(self.start_x, self.start_y, direction=0.0)
            agent.brain = sorted_agents[i].brain.copy()
            new_agents.append(agent)

        # Fill rest with offspring
        while len(new_agents) < self.size:
            parent1 = self._tournament_select(sorted_agents)
            parent2 = self._tournament_select(sorted_agents)
            assert parent1.brain is not None, "Parent1 has no brain"
            assert parent2.brain is not None, "Parent2 has no brain"

            child_brain = NeuralNetwork.crossover(parent1.brain, parent2.brain)

            child_brain.mutate(mutation_rate, mutation_strength)

            child_agent = Agent(self.start_x, self.start_y, direction=0.0)
            child_agent.brain = child_brain
            new_agents.append(child_agent)

        self.agents = new_agents
        self.generation += 1
        self.alive_count = self.size

    def _tournament_select(self, sorted_agents: List[Agent], tournament_size: int = 3) -> Agent:
        """Select one agent using tournament selection"""
        import random
        contestants = random.sample(sorted_agents, min(tournament_size, len(sorted_agents)))
        return max(contestants, key=lambda a: a.fitness)
    
    def __repr__(self):
        return (f"Population(size={self.size}, gen={self.generation}, "
                f"alive={self.alive_count}, best={self.best_fitness:.1f})")
