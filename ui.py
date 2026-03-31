import pygame

class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = pygame.font.SysFont(None, 36)

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        hovered = self.rect.collidepoint(mouse_pos)

        fill_color = (151, 33, 235) if hovered else (151, 33, 235) # Same fill color, but we can adjust brightness if needed
        border_color = (250, 255, 173) if hovered else (196, 131, 242) # Lighter border on hover

        pygame.draw.rect(screen, fill_color, self.rect, border_radius=8)
        if hovered:
            pygame.draw.rect(screen, border_color, self.rect, 3, border_radius=8) # Thicker border on hover
        else:
            pygame.draw.rect(screen, border_color, self.rect, 2, border_radius=8)

        text_surface = self.font.render(self.text, True, (255, 255, 255))
        text_x = self.rect.x + (self.rect.width - text_surface.get_width()) // 2
        text_y = self.rect.y + (self.rect.height - text_surface.get_height()) // 2
        screen.blit(text_surface, (text_x, text_y))

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)
