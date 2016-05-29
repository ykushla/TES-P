import datetime
import time

from yk.tes.objects.entryparams import EntryParams
from yk.tes.objects.scheme import Scheme
from yk.tes.process.trafficgenerator import TrafficGenerator


class Engine:
    # Engine class that provides the functionality for scheme traffic dynamics

    def __init__(self, scheme: Scheme, params: EntryParams, timeout):
        self.car_list = []
        self.scheme = scheme
        self.timeout = timeout
        self.generator = TrafficGenerator(scheme, params, timeout)

        # internal handler list that can be called on every engine(process) cycle(loop)
        self.handler_list = []

    def move_cars(self):
        # moves cars

        for car in self.car_list:
            if not car.move(self.timeout):
                # if false = the car went out of the scheme range and can be deleted

                self.car_list.remove(car)
                del car

    def generate_new_cars(self):
        # generation of new cars in the scheme

        new_car_list = self.generator.generate()
        if new_car_list is not None and len(new_car_list) > 0:
            self.car_list.extend(new_car_list)

    def log_cars(self):
        # logs car positions to console

        if len(self.car_list) > 0:
            for car in self.car_list:
                log("dirr: %s, segm: %s, pos: %s" % (car.direction, car.current_segment, car.position_in_segment))
        else:
            log("")

    def run(self):
        # the main Engine cycle method
        # this method should be run in a parallel process or thread

        try:
            while True:
                # infinite cycle
                # can be interrupted by exception ????

                self.move_cars()
                self.log_cars()
                self.generate_new_cars()

                # call of registered handlers (can be 0)
                self.call_handlers()

                # thread freeze for the amount of time
                # the same time is used for all the cars movement distance calcualtion
                # this is an atomic time unit
                time.sleep(self.timeout / 1000)

        except Exception as e:
            print(e)

    def register_handler(self, handler):
        # registers a new handler of the engine cycle

        self.handler_list.append(handler)

    def call_handlers(self):
        # calls of registered handlers

        for handler in self.handler_list:
            handler.engine_cycle_call(self)


def log(msg):
    print(str(datetime.datetime.now().time()) + ": " + msg)

