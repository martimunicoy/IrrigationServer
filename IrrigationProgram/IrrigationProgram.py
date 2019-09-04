import constants as co
import logging as log
from electrovalve import Electrovalve
from terminal_interface import TerminalInterface, StatusBulb
from optparse import OptionParser
from time import sleep

class IrrigationProgram(object):
    def __init__(self, args_dict):
        args_dict = args_dict
        mystatusbulb = StatusBulb()
        self.__is_running = False
        self.__is_watering = False

        # Set up logger
        self._logger_set_up()

    @property
    def is_running(self):
        return self.__is_running

    @property
    def is_watering(self):
        return self.__is_watering

    def _logger_set_up(self):
        log_dir = self.args_dict['log_dir']
        if log_dir is None:
            log_dir = 'IrrigationProgram.log'
        log_level = self.args_dict['log_level']
        if log_level is None:
            log_level = 'INFO'
        log.basicConfig(filename=log_dir, level=log_level,
                        format='%(asctime)s %(message)s')
        log.info(co.SEPARATOR)
        log.info(co.MAIN_INFO)

    def run(self):
        mystatusbulb.open()
        self.__is_running = True

        self._recursive_loop()

    def _recursive_loop(self):
        if(self.time_to_water):
            self._water()
            return self._recursive_loop()

        sleep(1)

        if (self.is_running):
            return self._recursive_loop()

    def _water(self):
        def exit():
            return interface.stop

        self.__is_watering = True

        water_cycle = get_water_cycle(schedule)
        for interval in water_cycle:
            electrovalve.open()
            wait(interval, exit)
            electrovalve.close()
            if interface.stop:
                break
            sleep(co.GAP)
        schedule.next_hour().running = False

        self.__is_watering = False


class Schedule(object):
    def __init__(self, sch_dir=None):
        self.sch_dir = sch_dir
        self.test = test
        self.sim = sim
        self.timer = None
        self.seconds_run = 0
        self.temporary_handler = TemporaryHandler()
        self.hours = []
        self.electrovalve = None
        self.interface = None

        if self.test:
            log.debug(co.SCHEDULE_TEST)
            self.timetable = [(today() + datetime.timedelta(seconds=1)).time()]
            self.cycle = co.TEST_CYCLE
        elif self.sch_dir is None:
            log.info(co.SCHEDULE_DIR)
            self.timetable = co.TIMETABLE
            self.cycle = co.CYCLE
        else:
            self.parser()

        for interval in self.cycle:
            self.seconds_run += co.GAP + interval

        for time in self.timetable:
            self.add_hour(time)

    def parser(self):
        log.info(co.SCHEDULE_PARSER.format(self.sch_dir))
        with open(self.sch_dir) as f:
            for line in f:
                line = line.strip()
                if line.startswith('CYCLE'):
                    self.cycle = map(int, line.split(" ")[1:])
                elif line.startswith('TIMETABLE'):
                    hours = [hour.split(",") for hour in line.split(" ")[1:]]
                    self.timetable = []
                    for hour in hours:
                        self.timetable.append(datetime.time(*map(int, hour)))

    def add_hour(self, time):
        try:
            hour = time.hour
            minute = time.minute
            second = time.second
        except AttributeError:
            new_time = datetime.time(*map(int, time))
            hour = new_time.hour
            minute = new_time.minute
            second = new_time.second
        self.hours.append(Hour(hour, minute, second))
        self.reset_timer()

    def remove_hour(self, time):
        for hour in self.hours:
            if hour.datetime == time.datetime:
                self.hours.remove(hour)
        self.reset_timer()

    def reset_timer(self):
        # Sort Hour list by lag time from lower to higher
        self.hours.sort(key=lambda x: x.lag())
        # Restart Timer
        if self.timer is not None:
            self.timer.cancel = True
            sleep(1.1)
            self.next_timer(self.electrovalve, self.interface)

    def next_hour(self):
        return self.hours[0]

    def next_timer(self, electrovalve, interface):
        # Sort Hour list by lag time from lower to higher
        self.hours.sort(key=lambda x: x.lag())
        next_hour = self.next_hour()
        log.debug(co.CYCLE_DEBUG.format(next_hour.lag()))
        self.timer = Timer(next_hour.lag(), water, args=(
            self, electrovalve, interface, self.test, self.sim))
        self.electrovalve = electrovalve
        self.interface = interface
        self.timer.start()
        self.log_info()

    def remaining_time_run(self):
        h1 = self.next_hour().datetime
        h2 = today().replace(1993, 1, 12)
        progress = (h2 - h1).total_seconds()
        total = self.seconds_run
        remaining = total - progress
        return int(remaining)

    def log_info(self):
        time_now = today().replace(microsecond=0)
        sch_str = ""
        for hour in self.hours:
                    sch_str += "\n    {}            {}".format(
                        hour.time, hour.lag_time())
        cyc_str = ""
        for output, tm in zip(co.CYCLE_OUTPUTS, self.cycle):
            cyc_str += "\n{}         {}".format(output, tm)
        log.info(co.SCHEDULE.format(time_now) + sch_str + "\n" +
                 co.CYCLE_INFO + cyc_str)

    def update_position(self):
        position = self.temporary_handler.position
        if position < 6:
            position += 1
        else:
            position = 1
        self.temporary_handler.position = position


def args_parser():
    parser = OptionParser()
    parser.add_option("-f", "--file", dest="sch_dir",
                      help="directory of the Schedule file",
                      metavar="FILE_DIRECTORY")
    parser.add_option("-l", "--log", dest="log_level",
                      help="set the logging level",
                      metavar="DEBUG, INFO, WARNING, ERROR, CRITICAL")
    parser.add_option("-d", "--log_dir", dest="log_dir",
                      help="directory of the log file",
                      metavar="FILE_DIRECTORY")
    args_dict = parser.parse_args()[0].__dict__

    return args_dict


def main():

    args_dict = args_parser()
    program = IrrigationProgram(args_dict)
    program.run()


if __name__ == "__main__":
    main()
