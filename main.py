import pygame
import config
from src.maze import Maze
from src.agent.agent import Agent
from src.agent.raycaster import WideRaycaster, SimpleRaycaster
from src.population import Population

def main():
    #Pygame Setup
    pygame.init()
    maze = Maze("src/maze/test_maze.json")
    screen = pygame.display.set_mode((1280,720))                    #just made the display standard HD
    pygame.display.set_caption("2D Neuroevolution Maze Runner")
    clock = pygame.time.Clock()
    running = True
    generation_finished = False  # Track if message has been printed
    font = pygame.font.Font(None, 28)  # For displaying info
    # Setup for the Population
    start_x, start_y = maze.start
    population = Population(size=10, start_x= start_x, start_y=start_y, view_rays=True)
    goal_x, goal_y = maze.goal



    #Error checking for temp maze background file
    try:
        maze_background = pygame.image.load('./temp_maze_background.jpg')
        maze_background = pygame.transform.scale(maze_background, (1280, 720))
    except:
        print("Warning: Could not load temp_maze_background.jpg")
        maze_background = None

    while running:
        clock.tick(60)


        
        # Event handling (moved to top for responsiveness)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Background
        if maze_background: 
            screen.blit(maze_background, (0, 0))  
        else:
            screen.fill((255, 255, 255))
        
        # Draw maze
        maze.draw(screen)
        # Update and draw the Population
        population.update(maze, goal_x, goal_y)
        population.draw(screen, maze)

        # Check if the generation is complete.
        if population.is_generation_over():
            if not generation_finished:
                population.calculate_fitness(goal_x, goal_y)
                print("Generation: ", population.generation, " finished!")
                generation_finished = True
        else:
            generation_finished = False




        pygame.display.flip()
        
    pygame.quit()

        #-----------------------------------------------
        # I believe future simulation updates go here:
        # - agent drawing
        # - neural netowrk control
        # - genetic algorithm steps
        # - maze rendering
        #------------------------------------------------

        # The flip() function updates the entire screen with all new changes that have been drawn making them visible to the user        
    pygame.quit()

#Temp edits being made, testing linking github to VSCode.
    

if __name__ == "__main__":
    main()
