from yk.tes.objects.point import Point

from yk.data.frame import Frame
from yk.tes.objects.segment import Segment


class Scheme:
    # transportation scheme class

    def __init__(self, frame):  # type: Frame
        # default and main constructor

        # create the internal lists
        self.segment_list = []
        self.initial_segments = {}
        self.terminal_segment_list = []
        self.segment_list_by_start_point = {}
        self.segment_list_by_end_point = {}
        self.directions = set()

        # build the scheme object from the Frame
        for item in frame.items:
            name = item["Name"]
            x1 = item["X1"]
            y1 = item["Y1"]
            x2 = item["X2"]
            y2 = item["Y2"]
            velocity = item["Velocity"]  # type: str
            direction = item["Direction"]  # type: str

            # add the direction subset to the general direction set
            if direction:
                self.directions = self.directions | set(direction.split(","))

            # creation and adding of a new segment
            start_point = Point(x1, y1)
            end_point = Point(x2, y2)
            segment = Segment(name, start_point, end_point, direction, velocity)
            self.segment_list.append(segment)

            # fills in auxiliary dictionaries

            local_segment_list = self.segment_list_by_start_point.get(start_point)
            if local_segment_list is None:
                local_segment_list = []
                self.segment_list_by_start_point[start_point] = local_segment_list
            local_segment_list.append(segment)

            local_segment_list = self.segment_list_by_end_point.get(end_point)
            if local_segment_list is None:
                local_segment_list = []
                self.segment_list_by_end_point[end_point] = local_segment_list
            local_segment_list.append(segment)

        # links segments between each other, adding to the terminal and initial lists
        # check on the directions definitions
        for segment in self.segment_list:  # type: Segment

            local_segment_list = self.segment_list_by_start_point.get(segment.end_point)
            if local_segment_list is None:
                segment.set_terminal()
                self.terminal_segment_list.append(segment)
            else:
                for segment2 in local_segment_list:  # type: Segment

                    # check if all segments on crossings have a defined direction
                    if len(local_segment_list) > 1 and (not segment2.direction):
                        raise Exception("""Segment (name: \"%s\"; points: %f, %f, %f, %f) must have a direction
                        definition!""" % (segment2.name, segment2.start_point.x, segment2.start_point.y,
                                                           segment2.end_point.x, segment2.end_point.y))

                    segment.next_segment_list.append(segment2)
                    segment2.prev_segment_list.append(segment)

            if not self.segment_list_by_end_point.__contains__(segment.start_point):
                if not segment.name:
                    raise Exception("Initial segment (points: %f, %f, %f, %f) must have a name definition!" %
                                    (segment.start_point.x, segment.start_point.y,
                                     segment.end_point.x, segment.end_point.y))

                segment.set_initial()
                self.initial_segments[segment.name] = segment

    def get_boundary_points(self):
        # returns the boundary points which represent the rectangle in which the entire scheme cna be placed

        minx, maxx, miny, maxy = 0, 0, 0, 0

        for segment in self.segment_list:  # type: Segment
            minx = min(minx, segment.start_point.x, segment.end_point.x)
            miny = min(miny, segment.start_point.y, segment.end_point.y)
            maxx = max(maxx, segment.start_point.x, segment.end_point.x)
            maxy = max(maxy, segment.start_point.y, segment.end_point.y)

        return [Point(minx, miny), Point(maxx, miny), Point(minx, maxy), Point(maxx, maxy)]
