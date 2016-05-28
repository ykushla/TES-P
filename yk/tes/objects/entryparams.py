from yk.data.frame import Frame
from yk.tes.objects.scheme import Scheme


class EntryParam:

    def __init__(self, entry_name, direction, probability):
        self.entry_name = entry_name
        self.direction = direction
        self.prob = probability


class EntryParams:

    def __init__(self, frame: Frame):
        self.entry_param_list = []

        for item in frame.items:
            entry_name = item["Entrance"]
            if not entry_name:
                raise Exception("Entry param entrance name missing!")

            direction = item["Direction"]  # type: str
            if not direction:
                raise Exception("Entry param direction value missing!")

            prob = item["Prob/min"]

            self.entry_param_list.append(EntryParam(entry_name, direction, prob))

    def validate_with_scheme(self, scheme: Scheme):
        for param in self.entry_param_list:  # type: EntryParam
            if not scheme.initial_segments.__contains__(param.entry_name):
                raise Exception("Segment \"%s\" is not found in the scheme!" % param.entry_name)

            if not scheme.directions.__contains__(param.direction):
                raise Exception("Direction \"%s\" is not found in the scheme!" % param.direction)

    def __iter__(self):
        return self.entry_param_list.__iter__()
