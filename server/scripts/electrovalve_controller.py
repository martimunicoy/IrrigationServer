import threading
import time
import django
import os
import sys
from datetime import datetime, timedelta
from dateutil import rrule
try:
    NO_RPI = False
    import RPi.GPIO as GPIO
except ImportError:
    NO_RPI = True
# import logging as log

# derive location to django project setting.py
proj_path = os.path.split(os.path.abspath(os.path.dirname(__file__)))[0]
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.settings")
sys.path.append(proj_path)
os.chdir(proj_path)
django.setup()

# Load models from server
from scheduleManager.models import ProgramStatus, IrrigationHour, CycleSettings


QUERY_FREQUENCY = int(1)  # 1 second
MAX_SLOTS = 6


class Electrovalve(object):

    def __init__(self, pin=27, gap=15):
        self._pin = pin
        self._gap = gap
        self._initial_setup()
        self.set_as_closed()
        # log.info(co.ELECTROVALVE_CONFIG.format(str(self.pin)))

    @property
    def pin(self):
        return self._pin

    @property
    def gap(self):
        return self._gap

    @property
    def status(self):
        return self._status

    @property
    def ready(self):
        return self._ready

    def _initial_setup(self):
        if NO_RPI:
            return
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.output(self.pin, GPIO.LOW)

    def set_as_open(self):
        self._ready = True
        self._status = 'open'

    def set_as_closed(self):
        self._ready = True
        self._status = 'closed'

    def set_as_moving(self):
        self._ready = False
        self._status = 'moving'

    def open(self):
        if self.ready:
            if self.status == 'closed':
                if NO_RPI:
                    print(' - Open electrovalve')
                else:
                    GPIO.output(self.pin, GPIO.HIGH)
                time.sleep(self.gap)
            self.set_as_open()
        elif self.status == 'moving':
            if not NO_RPI:
                GPIO.output(self.pin, GPIO.HIGH)
            time.sleep(self.gap)

    def close(self):
        if self.ready:
            if self.status == 'open':
                if NO_RPI:
                    print(' - Close electrovalve')
                else:
                    GPIO.output(self.pin, GPIO.LOW)
                time.sleep(self.gap)
            self.set_as_closed()
        elif self.status == 'moving':
            if NO_RPI:
                print(' - Moving electrovalve')
            else:
                GPIO.output(self.pin, GPIO.LOW)
            time.sleep(self.gap)

    def move(self, times=1):
        self.set_as_moving()
        if self.status == 'open':
            self.close()
        for _ in xrange(times):
            self.open()
            self.close()


class Cycle(object):
    def __init__(self, electrovalve, current_slot=1,
                 slot_times=[60, 60, 60, 60, 60, 60],
                 slot_actives=[False, False, False, False, False, False]):
        self._electrovalve = electrovalve
        self._current_slot = current_slot
        self._slot_times = slot_times
        self._slot_actives = slot_actives

    NUMBER_OF_SLOTS = 6

    @property
    def electrovalve(self):
        return self._electrovalve

    @property
    def current_slot(self):
        return self._current_slot

    @property
    def slot_times(self):
        return self._slot_times

    @property
    def slot_actives(self):
        return self._slot_actives

    def set_current_slot(self, current_slot):
        self._current_slot = current_slot

    def set_slot_times(self, slot_times):
        self._slot_times = slot_times

    def set_slot_actives(self, slot_actives):
        self._slot_actives = slot_actives

    def set_next_slot(self):
        self._current_slot += 1
        if self.current_slot >= self.NUMBER_OF_SLOTS:
            self._current_slot = 0

    def run(self):
        for _ in range(0, self.NUMBER_OF_SLOTS):
            slot = self._current_slot
            slot_time = self.slot_times[slot]
            slot_active = self.slot_actives[slot]
            if slot_active:
                self.electrovalve.open()
                time.sleep(slot_time)
                self.electrovalve.close()
            self.set_next_slot()


class ServerStatus(object):
    class Program(object):
        def __init__(self, time, weekday):
            self._time = time
            self._weekday = weekday

        WEEKDAY_TO_RRULE = {'Monday': rrule.MO,
                            'Tuesday': rrule.TU,
                            'Wednesday': rrule.WE,
                            'Thursday': rrule.TH,
                            'Friday': rrule.FR,
                            'Saturday': rrule.SA,
                            'Sunday': rrule.SU}

        @property
        def time(self):
            return self._time

        @property
        def weekday(self):
            return self._weekday

        def __hash__(self):
            return hash((self.time.hour, self.time.minute, self.time.second,
                         self.weekday))

        def __eq__(self, other):
            if not isinstance(other, type(self)):
                return False
            return (self.time.hour, self.time.minute, self.time.second,
                    self.weekday) == (other.time.hour, other.time.minute,
                                      other.time.second, other.weekday)

        def __ne__(self, other):
            return not self.__eq__(other)

        def __lt__(self, other):
            return self.get_delay() < other.get_delay()

        def __str__(self):
            return '{} {}'.format(self.weekday, self.time)

        def __repr__(self):
            return self.__str__()

        def get_date(self):
            start = datetime.now()
            # start = start
            rule = rrule.rrule(
                dtstart=start, freq=rrule.HOURLY,
                byweekday=[self.WEEKDAY_TO_RRULE[self.weekday]])

            date = rule.between(start, start + timedelta(days=7), inc=True)[0]
            date = date.replace(hour=self.time.hour, minute=self.time.minute,
                                second=self.time.second)

            return date

        def get_delay(self):
            now = datetime.now()
            date = self.get_date()
            if date < now:
                date += timedelta(days=7)
            return (date - now).total_seconds()

    SLOT_TIMES = ['slot1_time', 'slot2_time', 'slot3_time', 'slot4_time',
                  'slot5_time', 'slot6_time']

    SLOT_ACTIVES = ['slot1_active', 'slot2_active', 'slot3_active',
                    'slot4_active', 'slot5_active', 'slot6_active']

    def _get_program_status(self):
        return ProgramStatus.objects.all().values()[0]

    def _get_programs(self):
        programs = []
        for obj in IrrigationHour.objects.all():
            hour = obj.hour
            weekdays = [i.name for i in obj.get_week_days().all()]
            for weekday in weekdays:
                programs.append(self.Program(hour, weekday))
        return programs

    def _get_cycle_settings(self):
        return CycleSettings.objects.all().values()[0]

    @property
    def is_running(self):
        return self._get_program_status()['running']

    @property
    def current_slot(self):
        return self._get_program_status()['current_slot']

    @property
    def programs(self):
        return self._get_programs()

    @property
    def slot_times(self):
        cycle_settings = self._get_cycle_settings()
        return [cycle_settings[i] for i in self.SLOT_TIMES]

    @property
    def slot_actives(self):
        cycle_settings = self._get_cycle_settings()
        return [cycle_settings[i] for i in self.SLOT_ACTIVES]


class Handler(object):
    def __init__(self, cycle):
        self._cycle = cycle
        self._electrovalve = cycle.electrovalve
        self._apply_state()

    @ property
    def cycle(self):
        return self._cycle

    @ property
    def electrovalve(self):
        return self._electrovalve

    def feed(self, *args):
        self._feed(*args)


class StatusHandler(Handler):
    def __init__(self, cycle, current_running_status):
        self._current_running_status = current_running_status
        super().__init__(cycle)

    @ property
    def current_running_status(self):
        return self._current_running_status

    def _apply_state(self):
        if self.current_running_status:
            self.electrovalve.open()
        else:
            self.electrovalve.close()

    def _feed(self, running_status):
        if running_status != self.current_running_status:
            self._current_running_status = running_status
            self._apply_state()


class ScheduleHandler(Handler):
    def __init__(self, cycle, current_programs):
        self._programs_to_load = set(current_programs)
        self._loaded_programs = []
        self._next_program = None
        self._timer = None
        super().__init__(cycle)

    @ property
    def programs_to_load(self):
        return self._programs_to_load

    @ property
    def loaded_programs(self):
        return self._loaded_programs

    @ property
    def next_program(self):
        return self._next_program

    @ property
    def timer(self):
        return self._timer

    def _run_program(self):
        print(' - Running program')
        self.cycle.run()

        self.loaded_programs.sort()
        self._next_program = self.loaded_programs[0]
        self._set_timer()

    def _check_loading_conditions_fulfillment(self, program):
        pass

    def _check_unloading_conditions_fulfillment(self, program):
        pass

    def _add_program_to_loaded_programs(self, program):
        self._loaded_programs.append(program)
        self.loaded_programs.sort()

    def _remove_program_to_loaded_programs(self, program):
        self._loaded_programs.remove(program)

    def _set_timer(self):
        self._timer = threading.Timer(self.next_program.get_delay(),
                                      self._run_program)
        self.timer.start()

    def load_program(self, program):
        self._check_loading_conditions_fulfillment(program)
        self._add_program_to_loaded_programs(program)
        if self.next_program != self.loaded_programs[0]:
            self._next_program = self.loaded_programs[0]
            if self.timer is not None:
                self.timer.cancel()
            self._set_timer()

    def unload_program(self, program):
        self._check_unloading_conditions_fulfillment(program)
        self._remove_program_to_loaded_programs(program)
        self.timer.cancel()
        if len(self.loaded_programs) == 0:
            self.timer = None
        else:
            self._next_program = self.loaded_programs[0]
            self._set_timer()

    def _apply_state(self):
        for program_to_load in self.programs_to_load.difference(
                self.loaded_programs):
            self.load_program(program_to_load)
        for program_to_unload in set(self.loaded_programs).difference(
                self.programs_to_load):
            self.unload_program(program_to_unload)

    def _feed(self, programs):
        self._programs_to_load = set(programs)
        self._apply_state()
        print(datetime.now(), self.loaded_programs,
              self.loaded_programs[0].get_delay())
        print(self.timer)


class CycleHandler(Handler):
    def __init__(self, cycle, current_slot, slot_times, slot_actives):
        self._current_slot = current_slot
        self._slot_times = slot_times
        self._slot_actives = slot_actives
        super().__init__(cycle)

    @property
    def current_slot(self):
        return self._current_slot

    @ property
    def slot_times(self):
        return self._slot_times

    @ property
    def slot_actives(self):
        return self._slot_actives

    def _apply_state(self):
        self.cycle.set_current_slot(self.current_slot)
        self.cycle.set_slot_times(self.slot_times)
        self.cycle.set_slot_actives(self.slot_actives)

    def _feed(self, current_slot, slot_times, slot_actives):
        if current_slot != self.current_slot:
            self._current_slot = current_slot
            self.cycle.set_current_slot(self.current_slot)
        if slot_times != self.slot_times:
            self._slot_times = slot_times
            self.cycle.set_slot_times(self.slot_times)
        if slot_actives != self.slot_actives:
            self._slot_actives = slot_actives
            self.cycle.set_slot_actives(self.slot_actives)
        print(self.cycle.slot_times)
        print(self.cycle.slot_actives)
        print(self.cycle.current_slot)


class PeriodicQuery(object):
    def __init__(self, frequency=QUERY_FREQUENCY, **kargs):
        self._electrovalve = Electrovalve(**kargs)
        self._cycle = Cycle(self.electrovalve, **kargs)
        self._server_status = ServerStatus()
        self._handlers = {
            'status': StatusHandler(self.cycle,
                                    self.server_status.is_running),
            'schedule': ScheduleHandler(self.cycle,
                                        self.server_status.programs),
            'cycle': CycleHandler(self.cycle,
                                  self.server_status.current_slot,
                                  self.server_status.slot_times,
                                  self.server_status.slot_actives)}
        self._frequency = frequency
        self._thread = None

    @ property
    def electrovalve(self):
        return self._electrovalve

    @property
    def cycle(self):
        return self._cycle

    @ property
    def server_status(self):
        return self._server_status

    @ property
    def handlers(self):
        return self._handlers

    @ property
    def frequency(self):
        return self._frequency

    @ property
    def thread(self):
        return self._thread

    def start(self):
        if (self.thread is None):
            self._thread = threading.Timer(self.frequency,
                                           self._periodic_action)
            self.thread.start()

    def _get_program_status(self):
        return ProgramStatus.objects.all().values()[0]

    def _periodic_action(self):
        self.handlers['status'].feed(self.server_status.is_running)
        self.handlers['schedule'].feed(self.server_status.programs)
        self.handlers['cycle'].feed(self.server_status.current_slot,
                                    self.server_status.slot_times,
                                    self.server_status.slot_actives)
        self._thread = None
        self.start()

    def stop(self):
        self.thread.cancel()
        self._thread = None


def main():
    """ Main method """
    pq = PeriodicQuery()

    try:
        print('Starting electrovalve controller. Press Ctrl + C to exit.')
        pq.start()
        while(True):
            time.sleep(1)
    except KeyboardInterrupt:
        print()
        print('Cancelling electrovalve controller')
        pq.stop()


if __name__ == "__main__":
    main()
