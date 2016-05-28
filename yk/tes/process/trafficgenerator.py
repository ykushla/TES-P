import random

from yk.tes.objects.car import Car
from yk.tes.objects.entryparams import EntryParam
from yk.tes.objects.entryparams import EntryParams
from yk.tes.objects.scheme import Scheme


class TrafficGenerator:
    MSEC_PROB_RATE = 1 / 60 / 1000

    def __init__(self, scheme: Scheme, params: EntryParams, timeout):
        self.scheme = scheme
        self.params = params
        self.timeout = timeout

    def generate(self):
        car_list = None
        random.seed()

        for param in self.params:  # type: EntryParam
            prob = param.prob * TrafficGenerator.MSEC_PROB_RATE * self.timeout
            if prob > random.random():
                car = Car(param.direction, self.scheme.initial_segments[param.entry_name])
                if car_list is None:
                    car_list = []
                car_list.append(car)

        return car_list
