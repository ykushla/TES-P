from yk.tes.objects.segment import Segment


class Car:

    RATE_1_3600 = 1 / 3600
    RATE_3600 = 3600

    def __init__(self, direction, starting_segment: Segment):
        self.direction = direction
        self.current_segment = starting_segment
        self.position_in_segment = 0

    def move(self, msec_passed) -> bool:
        # returns false if went out of scheme

        if self.current_segment is None:
            return False

        while msec_passed > 0:
            projected_distance = self.current_segment.velocity * Car.RATE_1_3600 * msec_passed
            remaining_distance = self.current_segment.length - self.position_in_segment
            if projected_distance < remaining_distance:
                self.position_in_segment += projected_distance
                msec_passed = 0
            else:
                if self.current_segment.is_terminal:
                    self.current_segment = None
                    return False

                next_segment_found = False
                for next_segment in self.current_segment.next_segment_list:  # type: Segment
                    if (not next_segment.direction) or next_segment.direction.__contains__(self.direction):
                        msec_on_segment = remaining_distance / self.current_segment.velocity * Car.RATE_3600
                        msec_passed -= msec_on_segment
                        self.current_segment = next_segment
                        self.position_in_segment = 0
                        next_segment_found = True
                        break

                if not next_segment_found:
                    raise Exception("Needed segment by direction not found!")

        return True

    def x(self):
        return self.current_segment.start_point.x + \
               (self.current_segment.end_point.x - self.current_segment.start_point.x) * \
               self.position_in_segment / self.current_segment.length

    def y(self):
        return self.current_segment.start_point.y + \
               (self.current_segment.end_point.y - self.current_segment.start_point.y) * \
               self.position_in_segment / self.current_segment.length

