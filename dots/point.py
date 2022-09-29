from board import Base


class Point(Base):
    def __init__(self, x: int, y: int, status: int, border_distance: float = None):
        self.pos = (x, y)
        self.status = status
        self.border_distance = border_distance

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
