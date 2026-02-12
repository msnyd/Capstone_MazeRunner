import pygame
import config
from src.maze import Maze
from src.agent.agent import Agent

def main():
    #Pygame Setup
    pygame.init()
    maze = Maze("src/maze_layout.json")
    screen = pygame.display.set_mode((1280,720))                    #just made the display standard HD
    pygame.display.set_caption("2D Neuroevolution Maze Runner")
    clock = pygame.time.Clock()
    running = True

    #Creating a temp agent test dummy *DELETE LATER*
    start_x, start_y = maze.start
    test_dummy = Agent(start_x, start_y, direction=0.0)
    #Creating a temp agent test dummy *DELETE LATER*

    #Error checking for temp maze background file
    try:
        maze_background = pygame.image.load('./temp_maze_background.jpg')
        maze_background = pygame.transform.scale(maze_background, (1280, 720))
    except:
        print("Warning: Could not load temp_maze_background.jpg")
        maze_background = None

    while running:
        clock.tick(60)                                                #Limit the FPS to 60, we can go lower if we need better performance.
        #Draw background if its available.
        if maze_background: 
            screen.blit(maze_background, (0,0))  
        #Fall back on black background.    
        else:
            screen.fill((0,0,0)) 
        maze.draw(screen)

        #Creating a temp agent test dummy *DELETE LATER*
        test_dummy.move(0,1)
        test_dummy.draw(screen)
        #Creating a temp agent test dummy *DELETE LATER*

    #The code below allows the user to exit the window by pressing the red x top right
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        #-----------------------------------------------
        # I believe future simulation updates go here:
        # - agent drawing
        # - neural netowrk control
        # - genetic algorithm steps
        # - maze rendering
        #------------------------------------------------

        # The flip() function updates the entire screen with all new changes that have been drawn making them visible to the user
        pygame.display.flip() 
        
    pygame.quit()

#Temp edits being made, testing linking github to VSCode.
    

if __name__ == "__main__":
    main()
