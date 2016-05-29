from math import sqrt


class Point:
    # Point class for coordinates structure

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __hash__(self):
        return (str(self.x) + " " + str(self.y)).__hash__();

    def __eq__(self, other):
        return (self.x == other.x) and (self.y == other.y)

def get_distance_between_points(p1: Point, p2: Point):
    # calculates distance between two points

    return sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2)

