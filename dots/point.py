import math
from board import Base


class Point(Base):
    def __init__(self, x: int, y: int, status: int):
        self.pos = (x, y)
        self.status = status

        if status == -1:
            # Bad point
            self.color = self.RED
            self.radius = 5

        elif status == 0:
            # Regular point
            self.color = self.BLACK
            self.radius = 4

        elif status == 1:
            # Good point
            self.radius = 5
            self.color = self.GREEN

    @property
    def dist_to_border(self):
        """ returns the closest distance from the point to border """
        border_points = [
            (self.pos[0], self.RESOLUTION[1] / 2),
            (self.pos[0], -1 * (self.RESOLUTION[1] / 2)),
            (self.RESOLUTION[0] / 2, self.pos[1]),
            (-1 * (self.RESOLUTION[0] / 2), self.pos[1]),
        ]
        closest_to_border = min([math.dist(self.pos, each) for each in border_points])

        return closest_to_border
