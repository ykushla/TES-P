from yk.tes.objects.point import get_distance_between_points


class Segment:

    def __init__(self, name, start_point, end_point, direction, velocity):
        self.name = name
        self.start_point = start_point
        self.end_point = end_point
        self.direction = direction
        self.velocity = velocity;

        self.length = get_distance_between_points(start_point, end_point)

        self.is_initial = False
        self.is_terminal = False

        self.next_segment_list = []
        self.prev_segment_list = []

    def set_initial(self):
        self.is_initial = True

    def set_terminal(self):
        self.is_terminal = True

    def __str__(self):
        return "name: %s; points: (%s, %s, %s, %s); dirr: %s" % \
               (self.name, self.start_point.x, self.start_point.y, self.end_point.x, self.end_point.y,
                self.direction)

