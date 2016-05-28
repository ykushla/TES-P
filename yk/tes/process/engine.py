import datetime
import time

from yk.tes.objects.entryparams import EntryParams
from yk.tes.objects.scheme import Scheme
from yk.tes.process.trafficgenerator import TrafficGenerator


class Engine:

    def __init__(self, scheme: Scheme, params: EntryParams, timeout):
        self.car_list = []
        self.scheme = scheme
        self.timeout = timeout
        self.generator = TrafficGenerator(scheme, params, timeout)

        self.handler_list = []

    def move_cars(self):
        for car in self.car_list:
            if not car.move(self.timeout):
                self.car_list.remove(car)
                del car

    def generate_new_cars(self):
        new_car_list = self.generator.generate()
        if new_car_list is not None and len(new_car_list) > 0:
            self.car_list.extend(new_car_list)

    def log_cars(self):
        if len(self.car_list) > 0:
            for car in self.car_list:
                log("dirr: %s, segm: %s, pos: %s" % (car.direction, car.current_segment, car.position_in_segment))
        else:
            log("")

    def run(self):
        try:
            while True:
                self.move_cars()
                self.log_cars()
                self.generate_new_cars()

                self.call_handlers()

                time.sleep(self.timeout / 1000)

        except Exception as e:
            print(e)

    def register_handler(self, handler):
        self.handler_list.append(handler)

    def call_handlers(self):
        for handler in self.handler_list:
            handler.engine_cycle_call(self)


def log(msg):
    print(str(datetime.datetime.now().time()) + ": " + msg)

