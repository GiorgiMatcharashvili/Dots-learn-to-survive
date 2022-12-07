import pygame
from board import Board
from dots import Dots


def run():
    board = Board()
    dots = Dots(board)

    is_running = True

    while is_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False

        board.clear()

        board.show_points(dots.good_points + dots.bad_points)

        board.show_points(dots.objs)

        dots.move()

        pygame.display.update()


if __name__ == "__main__":
    run()
