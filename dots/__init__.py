import json
import math
from datetime import datetime as dt
from .dot import Dot
from board import Base, Board
from .point import Point
from itertools import product


class Dots(Base):
    def __init__(self, board: Board):
        self.generation = 0
        self.start_pos = (0, 0)

        self.bad_points = []
        self.good_points = []
        self.death_time = None

        self.board = board

        self.load_data()

        self.objs = [Dot(*self.start_pos) for _ in range(self.POPULATION)]

    def move(self):
        # Find all occupied good points
        occupied_points = []
        for good_point in self.good_points:
            for obj in self.objs:
                dist = math.dist(good_point.pos, obj.pos)
                if dist < 3:
                    occupied_points.append(good_point)
                    obj.winner = True
                    break

        # Move all the dots
        for obj in self.objs:
            positions = []
            for diff_obj in self.objs:
                if obj != diff_obj:
                    positions.append(Point(*diff_obj.pos, 1))
            obj.move(positions, self.bad_points, list(set(self.good_points) - set(occupied_points)))

        return self.check()

    def check(self):
        # Check if they are alive
        for obj in self.objs:
            if obj.is_dead():
                self.bad_points.append(Point(*obj.pos, -1))
                self.objs.remove(obj)
                self.death_time = dt.now()

        if not self.death_time:
            self.death_time = dt.now()

        population = len(self.objs)

        # show population
        self.board.show_text("Population: " + str(population),
                             (-1 * self.RESOLUTION[0] / 2, self.RESOLUTION[0] / 2))

        # Check if they should regenerate
        time_limit = 10 if len(self.good_points) < 20 else len(self.good_points) / 2

        time_dilation = dt.now() - self.death_time
        if float(time_dilation.total_seconds()) > time_limit:
            self.regeneration()

        # Check if it reached goal
        loser_objs = list(filter(lambda l: l if not l.winner else None, self.objs))
        if len(loser_objs) - 1 < self.GP_INDEX:
            self.generation += 1
            self.show_info()
            return False

        return True

    def show_info(self):
        print(f"GENERATION: {self.generation}")
        print(f"TIME: {(dt.now() - self.death_time).total_seconds()}")
        print(f"POPULATION: {len(self.objs)}")
        print(f"Good points count: {len(self.good_points)}, Bad points count: {len(self.bad_points)}\n")

    def regeneration(self):
        self.generation += 1
        self.save_data()

        self.show_info()

        self.objs = [Dot(*self.start_pos) for _ in range(self.POPULATION)]
        self.death_time = dt.now()

    def calculate_good_points(self):
        # Find objs worthy to become good points
        loser_objs = list(filter(lambda l: l if not l.winner else None, self.objs))
        sorted_objs = sorted(loser_objs, key=lambda l: l.dist_to_border)
        worthy_objs = []
        for each in sorted_objs:
            if each.dist_to_border in range(int(sorted_objs[0].dist_to_border),
                                            int(sorted_objs[self.GP_INDEX].dist_to_border + self.FINE_DIST)):
                worthy_objs.append(each)
            else:
                break

        # Check worthy objs
        not_good_points = set()
        not_worthy_objs = set()
        for i in list(product(worthy_objs, self.good_points)):
            obj, good_point = i[0], i[1]
            if math.dist(obj.pos, good_point.pos) <= self.FINE_DIST:
                if obj.dist_to_border > good_point.dist_to_border:
                    not_worthy_objs.add(obj)
                elif good_point.dist_to_border >= obj.dist_to_border:
                    not_good_points.add(good_point)

        self.good_points = list(set(self.good_points) - not_good_points)
        worthy_objs = list(set(worthy_objs) - not_worthy_objs)

        for obj in worthy_objs:
            self.good_points.append(Point(*obj.pos, 1))

    def save_data(self):
        with open("./data.json", "r") as f:
            data = json.load(f)

            try:
                # Add bad points
                data[str(self.POPULATION)]["bad_points"] = list({bad_point.pos for bad_point in self.bad_points})

                # Add good points
                self.calculate_good_points()
                data[str(self.POPULATION)]["good_points"] = list({good_point.pos for good_point in self.good_points})

            except KeyError:
                # Add good points
                self.calculate_good_points()
                data[self.POPULATION] = {"bad_points": [bad_point.pos for bad_point in self.bad_points],
                                         "good_points": [good_point.pos for good_point in self.good_points]}

        with open("./data.json", "w") as f:
            json.dump(data, f, indent=4)

    def load_data(self):
        with open("./data.json", "r+") as f:
            data = json.load(f)
            try:
                self.bad_points = data[str(self.POPULATION)]["bad_points"]
                self.bad_points = [Point(*bad_point, -1) for bad_point in self.bad_points]

                self.good_points = data[str(self.POPULATION)]["good_points"]
                self.good_points = [Point(*good_point, 1) for good_point in self.good_points]

            except KeyError:
                pass
