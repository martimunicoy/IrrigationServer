import datetime
import constants as co
import logging as log
import threading
import sys
from time import sleep
from mailing import Mail


class Schedule(object):

    def __init__(self, sch_dir, test=False, sim=False):
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


class Timer(object):

    def __init__(self, interval, function, args=[]):
        self.interval = interval
        self.function = function
        self.args = args
        self.thread = threading.Thread(target=self.run)
        self.thread.daemon = False
        self.interface = args[2]

    def start(self):
        self.cancel = False
        self.thread.start()

    def run(self):
        wait(self.interval, self.exit)
        if not self.cancel:
            self.function(*self.args)

    def exit(self):
        return self.cancel


class Hour(object):

    def __init__(self, hour, minute=0, second=0):
        self.hour = hour
        self.minute = minute
        self.second = second

        self.datetime = datetime.datetime(1993, 1, 12, self.hour, self.minute,
                                          self.second)
        self.time = self.datetime.time()
        self.running = False

    def lag(self):
        return seconds_from_now(self.datetime)

    def lag_time(self):
        return seconds_to_time(self.lag())

    def start_run(self):
        self.running = True

    def end_run(self):
        self.running = False


class TemporaryHandler(object):

    def __init__(self, name=co.TEMP_FILE):
        self.name = name
        self.position = 1

        try:
            with open(self.name) as f:
                for line in f:
                    line = line.strip()
                    if line.startswith(co.TEMP_KEY1):
                        self.position = int(line.split(" ")[1])

        except IOError:
            log.warning(co.NO_TEMP_FILE)

    def save(self):
        f = open(self.name, 'w')
        f.write(co.TEMP_KEY1 + ' ' + str(self.position))
        f.close()


def today():
    return datetime.datetime.now().replace(microsecond=0)


def initiate_timer(schedule, electrovalve, interface, test=False, sim=False):
    schedule.next_timer(electrovalve, interface)
    if test:
        print co.TEST_WARNING
        log.info(co.TEST_WARNING)


def water(schedule, electrovalve, interface, test, sim):
    def exit():
        return interface.stop

    schedule.next_hour().running = True
    water_cycle = get_water_cycle(schedule)
    for interval in water_cycle:
        electrovalve.open()
        wait(interval, exit)
        electrovalve.close()
        if interface.stop:
            break
        sleep(co.GAP)
    schedule.next_hour().running = False

    if not interface.stop:
        log.info(co.IRRIGATION_SUCCESS)
        try:
            mymail = Mail(schedule)
            mymail.send_success()
            log.info(co.SEND_MAIL)
        except Exception:
            log.error(co.MAIL_ERROR)
    elif interface.exit:
        log.info(co.IRRIGATION_EXIT)
        sys.exit(0)

    if test:
        sys.exit(0)

    # schedule.timer = None
    interface.stop = False
    initiate_timer(schedule, electrovalve, interface, test, sim)


def get_water_cycle(schedule):
    index = schedule.temporary_handler.position - 1
    water_cycle = schedule.cycle[index:] + schedule.cycle[:index]
    return water_cycle


def seconds_from_now(hour):
    h1 = hour.replace(1993, 1, 12)
    h2 = (today()).replace(1993, 1, 12)
    lag = (h1 - h2).total_seconds()
    if lag <= 0:
        lag += co.SECONDS_ONE_DAY
    return int(lag)


def seconds_to_time(seconds):
    time = str(datetime.timedelta(seconds=seconds))
    return time


def abs(num):
    if num < 0:
        return -num
    else:
        return num


def exit(interface):
    return interface.stop


def wait(secs, exit):
    while (not exit()) and (secs > 0):
        sleep(1)
        secs -= 1


def current_hour():
    time = (today() + datetime.timedelta(seconds=10)).time()
    return Hour(time.hour, time.minute, time.second)
