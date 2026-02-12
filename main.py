import pygame
import config
from src.maze import Maze
from src.agent.agent import Agent

def main():
    #Pygame Setup
    pygame.init()
    maze = Maze("src/maze/test_maze.json")
    # maze = Maze("src/maze_layout.json")
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
        clock.tick(60)
        
        # Background
        if maze_background: 
            screen.blit(maze_background, (0,0))  
        else:
            screen.fill((255, 255, 255))  # White background to see walls
        
        maze.draw(screen)

        # Keyboard controls
        keys = pygame.key.get_pressed()
        turn = 0
        if keys[pygame.K_a]:
            turn = -0.1
        if keys[pygame.K_d]:
            turn = 0.1

        # Save position before moving
        old_x, old_y = test_dummy.x, test_dummy.y
        
        # Move
        test_dummy.move(turn, 1)
        
        # Collision check
        if maze.check_collision(test_dummy.x, test_dummy.y, test_dummy.radius):
            print(f"COLLISION at ({test_dummy.x:.1f}, {test_dummy.y:.1f})")
            test_dummy.x, test_dummy.y = old_x, old_y  # Revert position

        test_dummy.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.flip()

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
