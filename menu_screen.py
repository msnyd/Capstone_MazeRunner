import pygame
from ui import Button

def run_menu(screen, config):
    screen_w, screen_h = config.screen_width, config.screen_height
    button_w, button_h = 240, 60
    button_x = (screen_w - button_w) // 2
    start_button = Button(button_x, 220, button_w, button_h, "Start Simulation")
    settings_button = Button(button_x, 300, button_w, button_h, "Settings")
    quit_button = Button(button_x, 380, button_w, button_h, "Quit")

    font_title = pygame.font.Font(None, 64)
    font_hint = pygame.font.Font(None, 24)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                if start_button.is_clicked(mouse_pos):
                    return "start"
                if settings_button.is_clicked(mouse_pos):
                    return "settings"
                if quit_button.is_clicked(mouse_pos):
                    return "quit"

        # Gradient background
        for y in range(screen_h):
            r = int(20 + (y / screen_h) * 30) 
            g = int(20 + (y / screen_h) * 20) 
            b = int(40 + (y / screen_h) * 40) 
            pygame.draw.line(screen, (r, g, b), (0, y), (screen_w, y))

        # Card panel
        panel_rect = pygame.Rect(90, 140, screen_w - 180, 360) # Centered panel
        pygame.draw.rect(screen, (0, 0, 0, 180), panel_rect, border_radius=14) # Black background
        pygame.draw.rect(screen, (100, 100, 150), panel_rect, 2, border_radius=14) # Purple Border

        # Title with shadow
        title_shadow = font_title.render("MazeRunner", True, (0, 0, 0))
        screen.blit(title_shadow, ((screen_w - title_shadow.get_width()) // 2 + 2, 160 + 2))
        title = font_title.render("MazeRunner", True, (240, 240, 255))
        screen.blit(title, ((screen_w - title.get_width()) // 2, 160))

        # Buttons
        start_button.draw(screen)
        settings_button.draw(screen)
        quit_button.draw(screen)

        # Subtitle text
        hint = "Use the buttons above to start the simulation or change the simulation settings."
        hint_surf = font_hint.render(hint, True, (200, 210, 230))
        hint_x = (screen_w - hint_surf.get_width()) // 2
        screen.blit(hint_surf, (hint_x, panel_rect.bottom + 18))

        pygame.display.update()

            
