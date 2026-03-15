import json

class Config:
    def __init__(self, file_path="config.json"):
        with open(file_path, "r") as file:
            data = json.load(file)

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