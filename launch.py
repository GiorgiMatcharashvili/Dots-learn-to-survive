import pygame
from board import Board
from dots import Dots


def run():
    board = Board()
    dots = Dots(board)

    is_running = True

    while is_running:
        board.clear()

        board.show_points(dots.good_points + dots.bad_points)

        board.show_points(dots.objs)

        is_running = dots.move()

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False


if __name__ == "__main__":
    run()
    print("Program has stopped working successfully!")
