import json
import sys
import os


def resource_path(relative_path):
    """Get path to resource, works for dev and PyInstaller"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), relative_path)

class Config:
    def __init__(self, file_path="config.json"):
        self.file_path = file_path
        with open(resource_path(file_path), "r") as file:
            self.data = json.load(file)
        
        self._load_attributes()

    def _load_attributes(self):
        data = self.data
        # Display settings
        self.refresh_rate = data["Display"]["refresh_rate"]
        self.screen_width = data["Display"]["width"]
        self.screen_height = data["Display"]["height"]

        # Population settings
        self.population_size = data["Population"]["size"]
        self.max_steps = data["Population"]["max_steps"]

        # Neural network settings
        self.nn_input_size = data["Neural_Network"]["input_size"]
        self.nn_hidden_size = data["Neural_Network"]["hidden_size"]
        self.nn_output_size = data["Neural_Network"]["output_size"]

        # Genetic algorithm settings
        self.elite_count = data["Genetic_Algorithm"]["elite_count"]
        self.mutation_rate = data["Genetic_Algorithm"]["mutation_rate"]
        self.mutation_strength = data["Genetic_Algorithm"]["mutation_strength"]

        self.difficulty = data["difficulty"]

    def save(self):
        if hasattr(sys, '_MEIPASS'):
            print("Settings cannot be saved in bundled mode")
            return
        # Push the updated values back into JSON structure
        self.data["Population"]["size"] = self.population_size
        self.data["Population"]["max_steps"] = self.max_steps

        self.data["Genetic_Algorithm"]["elite_count"] = self.elite_count
        self.data["Genetic_Algorithm"]["mutation_rate"] = self.mutation_rate
        self.data["Genetic_Algorithm"]["mutation_strength"] = self.mutation_strength
        
        self.data["difficulty"] = self.difficulty

        with open(self.file_path, "w") as file:
            json.dump(self.data, file, indent=4)
