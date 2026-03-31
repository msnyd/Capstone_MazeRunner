import pygame

def run_settings(screen, config):
    font = pygame.font.Font(None, 36)
    font_large = pygame.font.Font(None, 48)
    clock = pygame.time.Clock()

    SCREEN_WIDTH = config.screen_width
    SCREEN_HEIGHT = config.screen_height

    # (Label, attribute_name, step size, min value, max value)

    settings = [
        ("Population Size", "population_size", 10, 10, 1000),
        ("Max Steps", "max_steps", 50, 50, 5000),
        ("Elite Count", "elite_count", 1, 0, config.population_size),
        ("Mutation Rate", "mutation_rate", 0.01, 0.0, 1.0),
        ("Mutation Strength", "mutation_strength", 0.01, 0.0, 5.0),
        ("Difficulty", "difficulty", ["easy", "medium", "hard", "very_hard"]),
    ]

    selected = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "menu"
            
            # Change selected settings Up/Down
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(settings)
                
                if event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(settings)

                # Right to increase value
                if event.key == pygame.K_RIGHT:
                    label, attr, *params = settings[selected]
                    if attr == "difficulty":
                        options = params[0]
                        current = getattr(config, attr)
                        idx = options.index(current)
                        new_idx = (idx + 1) % len(options)
                        setattr(config, attr, options[new_idx])
                    else:
                        step, min_val, max_val = params
                        current_value = getattr(config, attr)
                        new_value = min(max_val, current_value + step)
                        setattr(config, attr, new_value)

                # Left to decrease value
                if event.key == pygame.K_LEFT:
                    label, attr, *params = settings[selected]
                    if attr == "difficulty":
                        options = params[0]
                        current = getattr(config, attr)
                        idx = options.index(current)
                        new_idx = (idx - 1) % len(options)
                        setattr(config, attr, options[new_idx])
                    else:
                        step, min_val, max_val = params
                        current_value = getattr(config, attr)
                        new_value = max(min_val, current_value - step)
                        setattr(config, attr, new_value)

                # Save and return to menu
                if event.key == pygame.K_RETURN:
                    config.save()
                    return "menu"
                
                # Cancel (NO SAVING)
                if event.key == pygame.K_ESCAPE:
                    return "menu"
                
        # Draw
        # Background gradient
        for y in range(SCREEN_HEIGHT):
            r = int(20 + (y / SCREEN_HEIGHT) * 30)
            g = int(20 + (y / SCREEN_HEIGHT) * 20)
            b = int(40 + (y / SCREEN_HEIGHT) * 40)
            pygame.draw.line(screen, (r, g, b), (0, y), (SCREEN_WIDTH, y))
        
        # Semi-transparent overlay for settings panel
        panel_rect = pygame.Rect((SCREEN_WIDTH - 500) // 2, 100, 500, 400)
        pygame.draw.rect(screen, (0, 0, 0, 180), panel_rect)  # Semi-transparent black
        pygame.draw.rect(screen, (100, 100, 150), panel_rect, 3)  # Border
        
        # Title with shadow
        title_shadow = font_large.render("Settings", True, (0, 0, 0))
        screen.blit(title_shadow, ((SCREEN_WIDTH - title_shadow.get_width()) // 2 + 2, 111))
        title = font_large.render("Settings", True, (255, 255, 255))
        screen.blit(title, ((SCREEN_WIDTH - title.get_width()) // 2, 110))

        # Settings items
        item_height = 45
        item_width = 400
        start_y = 160
        
        for i, (label, attr, *params) in enumerate(settings):
            value = getattr(config, attr)

            if attr == "difficulty":
                display_value = value
            elif isinstance(value, float):
                display_value = f"{value:.2f}"
            else:
                display_value = str(value)

            # Item background
            item_rect = pygame.Rect((SCREEN_WIDTH - item_width) // 2, start_y + i * item_height, item_width, item_height - 5)
            
            if i == selected:
                # Selected item - bright highlight
                pygame.draw.rect(screen, (151, 33, 235), item_rect, border_radius=8)
                pygame.draw.rect(screen, (150, 180, 255), item_rect, 2, border_radius=8)
                text_color = (255, 255, 255)
                value_color = (255, 255, 100)
            else:
                # Normal item - subtle background
                pygame.draw.rect(screen, (60, 60, 80), item_rect, border_radius=8)
                pygame.draw.rect(screen, (120, 120, 140), item_rect, 1, border_radius=8)
                text_color = (220, 220, 220)
                value_color = (180, 180, 200)

            # Label text
            label_text = font.render(label, True, text_color)
            screen.blit(label_text, (((SCREEN_WIDTH - label_text.get_width()) // 2) - 50, start_y + i * item_height + 10))
            
            # Value text (right-aligned)
            value_text = font.render(display_value, True, value_color)
            value_x = ((SCREEN_WIDTH - value_text.get_width()) // 2) + 150
            screen.blit(value_text, (value_x, start_y + i * item_height + 10))

        # Instructions at bottom
        instructions_text = "Use UP/DOWN to select, LEFT/RIGHT to change, ENTER to save, ESC to cancel"
        instructions_surface = font.render(instructions_text, True, (200, 200, 220))
        instructions_x = (SCREEN_WIDTH - instructions_surface.get_width()) // 2
        instructions_y = SCREEN_HEIGHT - 150

        instructions_bg = pygame.Rect(instructions_x - 15, instructions_y - 8,
                                      instructions_surface.get_width() + 30,
                                      instructions_surface.get_height() + 16)
        pygame.draw.rect(screen, (0, 0, 0, 180), instructions_bg, border_radius=8)
        pygame.draw.rect(screen, (120, 120, 150), instructions_bg, 2, border_radius=8)

        screen.blit(instructions_surface, (instructions_x, instructions_y))

        pygame.display.update()
        clock.tick(60)