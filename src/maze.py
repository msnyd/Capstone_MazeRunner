import json
import pygame
import src.maze

class Maze:
    def __init__(self, json_file):
        self.walls = []
        self.start = (0, 0)
        self.goal = (0, 0)

        self.load_from_json(json_file)

    def load_from_json(self, json_file):
        with open(json_file, "r") as f:
            data = json.load(f)

        for wall in data["walls"]:
            rect = pygame.Rect(
                wall["x"],
                wall["y"],
                wall["width"],
                wall["height"]
            )
            self.walls.append(rect)

        self.start = (
            data["start"]["x"],
            data["start"]["y"]
        )

        self.goal = (
            data["goal"]["x"],
            data["goal"]["y"]
        )

    def draw(self, screen):
        for wall in self.walls:
            pygame.draw.rect(screen, (0, 0, 0), wall)

        pygame.draw.circle(screen, (0, 255, 0), self.start, 8)
        pygame.draw.circle(screen, (255, 0, 0), self.goal, 8)

    def check_collision(self, x, y, radius):
        #create a bounding box for the circle
        agent_rect = pygame.Rect(
            x - radius,
            y - radius,
            radius * 2,
            radius * 2
        )
        for wall in self.walls:
            if agent_rect.colliderect(wall):
                return True
        return False
    


