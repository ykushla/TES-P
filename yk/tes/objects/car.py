from yk.tes.objects.segment import Segment


class Car:
    # represent a transportation unit (Car)

    # constants for calculation optimization
    RATE_1_3600 = 1 / 3600
    RATE_3600 = 3600

    def __init__(self, direction, starting_segment: Segment):
        self.direction = direction
        self.current_segment = starting_segment
        self.position_in_segment = 0

    def move(self, msec_passed) -> bool:
        # performs the movement of the Car in the defined scheme
        # msec_passed = amount of time in milliseconds passed from the last move
        # this parameter actually equals to the process cycle delay (thread timeout)
        # returns false if went out of scheme

        if self.current_segment is None:
            return False

        while msec_passed > 0:

            # calculation of a predicted path covered during the msec_passed time
            projected_distance = self.current_segment.velocity * Car.RATE_1_3600 * msec_passed

            # calcualtion of the remaining distance on the current segment
            remaining_distance = self.current_segment.length - self.position_in_segment

            if projected_distance < remaining_distance:
                # movement in scope of the current segment

                self.position_in_segment += projected_distance
                msec_passed = 0

            else:
                # movement out of scope of the current segment

                # check if there is no segment to move
                if self.current_segment.is_terminal:
                    self.current_segment = None
                    return False

                # look for the next segment to move
                next_segment_found = False
                for next_segment in self.current_segment.next_segment_list:  # type: Segment

                    # check if there is a segment with the needed direction
                    # or if there is a single segment to go
                    if (len(self.current_segment.next_segment_list) == 1) or (not next_segment.direction) or \
                            next_segment.direction.__contains__(self.direction):

                        # calculate the estimated remaining time on the current segment
                        msec_on_segment = remaining_distance / self.current_segment.velocity * Car.RATE_3600

                        # total time on move reduction
                        msec_passed -= msec_on_segment

                        # segment change
                        self.current_segment = next_segment
                        self.position_in_segment = 0
                        next_segment_found = True
                        break

                # if no next segment found - an exceptional situation = error in scheme
                if not next_segment_found:
                    raise Exception("Needed segment by direction not found!")

        return True

    def x(self):
        # returns the absolute x coordinate of the car

        return self.current_segment.start_point.x + \
               (self.current_segment.end_point.x - self.current_segment.start_point.x) * \
               self.position_in_segment / self.current_segment.length

    def y(self):
        # returns the absolute y coordinate of the car

        return self.current_segment.start_point.y + \
               (self.current_segment.end_point.y - self.current_segment.start_point.y) * \
               self.position_in_segment / self.current_segment.length

