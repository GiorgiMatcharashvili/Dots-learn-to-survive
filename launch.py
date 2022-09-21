import random
import time

import pygame
from game import Game
from dots import Dots

SETTINGS = {
    "name": "Dots learn to Survive",
    "resolution": (500, 500),
    "bck_color": "#ffffff",
    "population": 40,
    "start_position": (250, 250),
    "dot_color": "#000000",
}


def run():
    game = Game(SETTINGS["name"], SETTINGS["resolution"], SETTINGS["bck_color"])
    dots = Dots(SETTINGS["population"], SETTINGS["start_position"], SETTINGS["dot_color"], game)

    is_running = True

    while is_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False

        game.clear()

        # Draw good and bad dots
        game.draw_good_dots(dots.good_points)
        game.draw_bad_dots(dots.bad_points)

        # Move dots
        dots.move()

        pygame.display.update()
        time.sleep(0.01)


if __name__ == "__main__":
    run()
