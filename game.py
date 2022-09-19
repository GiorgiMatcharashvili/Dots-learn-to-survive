import pygame


class Game:
    def __init__(self, name, resolution, bck_color):
        self.resolution = resolution
        self.bck_color = bck_color

        pygame.init()

        pygame.display.set_caption(name)
        self.surface = pygame.display.set_mode(self.resolution)

        self.background = pygame.Surface(self.resolution)
        self.background.fill(pygame.Color(self.bck_color))

        self.surface.blit(self.background, (0, 0))

    def clear(self):
        self.background.fill(pygame.Color(self.bck_color))
        self.surface.blit(self.background, (0, 0))

    def text(self, text):
        font = pygame.font.Font('freesansbold.ttf', 20)
        text = font.render(text, True, "#000000")
        textRect = text.get_rect()
        textRect.center = (72, 10)
        textRect.normalize()
        self.surface.blit(text, textRect)
