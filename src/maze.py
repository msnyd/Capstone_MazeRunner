import json
import pygame


class Maze:
    def __init__(self, json_file):
        self.walls = []
        self.start = None
        self.goal = None

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

    def check_collision(self, rect):
        for wall in self.walls:
            if rect.colliderect(wall):
                return True
        return False
