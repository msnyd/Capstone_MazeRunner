import pygame
import config
from src.maze import Maze
from src.agent.agent import Agent
from src.agent.raycaster import WideRaycaster, SimpleRaycaster

def main():
    #Pygame Setup
    pygame.init()
    maze = Maze("src/maze/test_maze.json")
    # maze = Maze("src/maze_layout.json")
    screen = pygame.display.set_mode((1280,720))                    #just made the display standard HD
    pygame.display.set_caption("2D Neuroevolution Maze Runner")
    clock = pygame.time.Clock()
    running = True
    font = pygame.font.Font(None, 28)  # For displaying info
    raycaster = SimpleRaycaster(max_range=400.0)


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

        # Keyboard controls
        keys = pygame.key.get_pressed()
        turn = 0
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            turn = -0.1
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            turn = 0.1

        # Save position before moving
        old_x, old_y = test_dummy.x, test_dummy.y
        
        # Move
        test_dummy.move(turn, 1)
                
        # Collision check
        if maze.check_collision(test_dummy.x, test_dummy.y, test_dummy.radius):
            print(f"COLLISION at ({test_dummy.x:.1f}, {test_dummy.y:.1f})")
            test_dummy.x, test_dummy.y = old_x, old_y

        # Cast rays and get distances
        distances = raycaster.cast_rays(
            test_dummy.x, 
            test_dummy.y, 
            test_dummy.direction, 
            maze.walls
        )
        
        # Store in agent (for neural network later)
        test_dummy.sensor_distances = distances

        # Draw rays (yellow lines with red hit points)
        raycaster.draw(
            screen, 
            test_dummy.x, 
            test_dummy.y, 
            test_dummy.direction, 
            maze.walls
        )

        # Draw agent
        test_dummy.draw(screen)

        # Display sensor info (top-left corner)
        # labels = ['Far L', 'Left', 'Fwd', 'Right', 'Far R']
        labels = ['Left', 'Fwd', 'Right']
        for i, dist in enumerate(distances):
            color = (255, 0, 0) if dist < 30 else (255, 255, 255)  # Red if close to wall
            text = font.render(f"{labels[i]}: {dist:.0f}px", True, color)
            screen.blit(text, (10, 10 + i * 25))
        
        # Display agent info
        pos_text = font.render(f"Position: ({test_dummy.x:.0f}, {test_dummy.y:.0f})", True, (255, 255, 255))
        screen.blit(pos_text, (10, 650))
        
        # Display controls
        controls_text = font.render("Controls: A/D or Arrow Keys to turn", True, (100, 100, 100))
        screen.blit(controls_text, (10, 690))

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
