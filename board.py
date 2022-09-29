import pygame


class Base:
    TITLE = "Dots learn to Survive"
    RESOLUTION = (500, 500)
    POPULATION = 100

    # Colors
    WHITE = "#ffffff"
    BLACK = "#000000"
    GREEN = "#00FF00"
    RED = "#FF0000"


class Board(Base):
    def __init__(self):
        self.WIDTH, self.HEIGHT = self.RESOLUTION
        self.BACKGROUND_COLOR = self.WHITE

        pygame.init()

        pygame.display.set_caption(self.TITLE)
        self.surface = pygame.display.set_mode(self.RESOLUTION)

        self.background = pygame.Surface(self.RESOLUTION)
        self.clear()

    def translate(self, x: int, y: int):
        """ Converts the board coordinates into pygame ones """
        return x + self.WIDTH / 2, -1 * y + self.HEIGHT / 2

    def clear(self):
        """ Clears the board """
        self.background.fill(pygame.Color(self.BACKGROUND_COLOR))
        self.surface.blit(self.background, (0, 0))

    @staticmethod
    def update():
        """ Updates the board"""
        pygame.display.update()

    def show_text(self, text: str, pos: tuple):
        """ Creates and displays text on the board"""
        font = pygame.font.Font('freesansbold.ttf', 20)
        text = font.render(text, True, self.BLACK)
        textRect = text.get_rect()

        textRect.centerx = self.translate(*pos)[0] + textRect.size[0]/2
        textRect.normalize()
        self.surface.blit(text, textRect)

    def show_points(self, points: list):
        """ Displays points on the board"""
        for point in points:
            pygame.draw.circle(self.surface, point.color, self.translate(*point.pos), point.radius)
