"""
Agent class for capstone mazerunner.

Each agent has:
- Position (x, y) in the maze
- Direction (radians, 0 = facing right, increases counterclockwise)
A neural net brain that controls movement
sensors that detect maze walls via raycasting
"""

import math
import numpy as np
import pygame

class Agent:
    def __init__(self, x: float, y:float, direction: float, radius: float = 8.0):
        #position and orientation
        self.x = x
        self.y = y
        self.direction = direction
        self.radius = radius

        # store starting position for reset
        self.start_x = x
        self.start_y = y
        self.start_direction = direction
        
        #movement params
        self.speed = 3.0
        self.turn_rate = 0.15

        #state tracking
        self.alive = True
        self.reached_goal = False
        self.steps_taken = 0
        self.fitness = 0.0

        #neural net (assigned later)
        self.brain = None

        #sensor data (popululated by raycaster)
        self.sensor_distances = []
        self.sensor_angles = []

    @property
    def position(self):
        """Return position as (x, y) tuple."""
        return (self.x, self.y)
    
    @property
    def direction_vector(self):
        """Return unit vector of current direction."""
        return (math.cos(self.direction), math.sin(self.direction))
    
    def reset(self):
        """Reset agent to initial state."""
        self.x = self.start_x
        self.y = self.start_y
        self.direction = self.start_direction
        self.alive = True
        self.reached_goal = False
        self.steps_taken = 0
        self.fitness = 0.0
        self.sensor_distances = []

    def set_brain(self, neural_network):
        """Assign a neural net brain to the agent."""
        self.brain = neural_network

    def think(self, goal_x: float, goal_y: float, sensor_range: float) -> tuple:
        """
        Use neural net to decide movement based on sensor inputs

        args:
            goal_x: X coord of the goal
            goyal_y: Y coord of the goal
            sensor_range: Max sensor distance for normalization

        returns:
            (turn amount, speed mult) from neural net output
        """
        if self.brain is None:
            return (0.0, 1.0)  # No brain, go straight at full speed
        
        inputs = self._build_inputs(goal_x, goal_y, sensor_range)

        outputs = self.brain.forward(inputs)

        turn_amount = outputs[0] * self.turn_rate  # Scale turn by turn rate

        if len(outputs) > 1:
            speed_multiplier = (float(outputs[0]) + 1.0) / 2.0
        else:
            speed_multiplier = 1.0  # Default to full speed if no speed output
        return (turn_amount, speed_multiplier)
    
    def _build_inputs(self, goal_x: float, goal_y: float, sensor_range: float) -> np.ndarray:
        """
        Build normalized input vector for neural net

        inputs:
        - normalized sensor distances
        - angle to goal realative to curr direction

        args:
            goal_x: X coord of goal
            goal_y: Y coord of goal
            sensor_range: Max sensor distance

        returns:
            numpy array of normalized inputs
        """
        inputs = []

        #normalized sensor distances (closer = lower values)
        for dist in self.sensor_distances:
            normalized = dist / sensor_range # 0 to 1
            inputs.append(normalized)

        angle_to_goal = self._angle_to_point(goal_x, goal_y)
        
        normalized_angle = angle_to_goal / math.pi
        inputs.append(normalized_angle)

        return np.array(inputs, dtype = np.float32)
    
    def _angle_to_point(self, target_x: float, target_y: float) -> float:
        """
        calculate angle to a point relative to current direction

        returns:
            angle in radians, range [-pi, pi]
            negative = target is to the right
            positive = target is to the left
        """
        dx = target_x - self.x
        dy = target_y - self.y
        absolute_angle = math.atan2(dy, dx)

        relative_angle = absolute_angle - self.direction

        while relative_angle > math.pi:
            relative_angle -= 2 * math.pi
        while relative_angle < -math.pi:
            relative_angle += 2 * math.pi

        return relative_angle
    
    def move(self, turn_amount: float, speed_multiplier: float):
        """
        Move the target agent based on turn and speed inputs.

        args:
            turn_amount: Amount to turn (radians)
            speed_multiplier: Multiplier for base speed (0 to 1)
        """
        if not self.alive:
            return
        
        self.direction += turn_amount

        self.direction = self.direction % (2 * math.pi)

        actual_speed = self.speed * speed_multiplier
        self.x += math.cos(self.direction) * actual_speed
        self.y += math.sin(self.direction) * actual_speed

        self.steps_taken += 1

    def update(self, maze, goal_x: float, goal_y: float, sensor_range: float, raycaster):
        """
        Update agent state based on maze and goal

        args:
            maze: Maze object for collision detection
            goal_x: X coord of goal
            goal_y: Y coord of goal
            sensor_range: Max sensor distance for raycasting
        """
        if not self.alive or self.reached_goal:
            return
        
        self.sensor_distances = raycaster.cast_rays(
            self.x, self.y, self.direction, maze.walls
        )

        turn, speed = self.think(goal_x, goal_y, sensor_range)

        self.move(turn, speed)

        if maze.check_collision(self.x, self.y, self.radius):
            self.alive = False
            return False
        
        dist_to_goal = math.sqrt((self.x - goal_x) ** 2 + (self.y - goal_y) ** 2)
        if dist_to_goal < self.radius + 10:
            self.reached_goal = True
            return False
        
        return True
    
    def distance_to(self, x:float, y:float) -> float:
        """Calculate distance from agent to a point."""
        return math.sqrt((self.x - x) ** 2 + (self.y - y) ** 2)
    
    def copy(self) -> 'Agent':
        """create a copy of this agent (without brain)"""
        new_agent = Agent(
            self.start_x, 
            self.start_y, 
            self.start_direction, 
            self.radius
        )
        new_agent.speed = self.speed
        new_agent.turn_rate = self.turn_rate
        return new_agent
    
    
    def __repr__(self):
        return (f"Agent(pos=({self.x:.1f}, {self.y:.1f}), "
                f"dir={math.degrees(self.direction):.1f}°, "
                f"alive={self.alive}, "
                f"fitness={self.fitness:.2f})")
    
    def draw(self, screen):
        """Draw the agent as a circle with a direction line."""
        x = int(self.x)
        y = int(self.y)

        #Body of the agent

        pygame.draw.circle(screen, (0,0,255), (x,y), self.radius)

        #Direction line (shows where the agent is facing for visuals)
        direction_x = math.cos(self.direction) * 20 #( * 20 makes it 20 pixels long)
        direction_y = math.sin(self.direction) * 20 #( * 20 makes it 20 pixels long)

        pygame.draw.line(screen, (255, 255, 255), (x,y), (x + direction_x, y + direction_y), 2)
