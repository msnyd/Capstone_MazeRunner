from src.agent.agent import Agent
from src.agent.raycaster import WideRaycaster

class Population:
    def __init__(self, size, start_x, start_y):
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

        self.agents = [ Agent(start_x, start_y, direction=0.0) for _ in range(size) ]

        # Shared WideRaycaster for all agents
        self.raycaster = WideRaycaster(max_range=150)

        # Will keep track of which generation the population is on.
        self.generation = 1

        # If we decide that agents die, this will keep track.
        self.alive_count = size

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

def draw(self, screen):
    """
    Draws all agents onto the screen.
    """
    for agent in self.agents:
        agent.draw(screen)

def reset(self):
    """
    Reset all agents back to the starting position.
    """
    for agent in self.agents:
        agent.reset()

def calculate_fitness(self, goal_x, goal_y):
    """
    Assigns a fitness score based on the distance to the goal.
    """
    for agent in self.agents:
        distance = agent.distance_to(goal_x, goal_y)
        agent.fitness = 1.0 / (distance + 1.0)

def is_generation_over(self):
    """
    Checks if all agents either died or reached the goal.
    """
    return all((not a.alive) or a.reached_goal for a in self.agents)

