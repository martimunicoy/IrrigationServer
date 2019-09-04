import constants as co
import threading
import timing
import sys
import RPi.GPIO as GPIO


class TerminalInterface(object):

    def __init__(self, schedule, electrovalve, statusbulb, test=False,
                 sim=False):
        self.thread = threading.Thread(target=self.run, args=())
        self.thread.daemon = False
        self.schedule = schedule
        self.electrovalve = electrovalve
        self.statusbulb = statusbulb
        self.test = test
        self.sim = sim
        if not self.test:
            self.thread.start()
            print co.WELCOME
        self.exit = False
        self.stop = False

    def run(self):
        try:
            com = raw_input('\n>>> ')
            parsed_com = com.split(" ")
            key = co.COMMAND_LIST[parsed_com[0]]

            # EXIT
            if key == 1 and len(parsed_com) == 1:
                if self.schedule.timer is not None:
                    self.schedule.timer.cancel = True
                    self.schedule.temporary_handler.save()
                    self.stop = True
                    self.exit = True
                    self.statusbulb.close()
                    sys.exit(0)

            # HELP
            elif key == 2 and len(parsed_com) == 1:
                print co.HELP
                print co.COMMAND_LIST
                print co.COMMAND_HELP

            # SCHEDULE
            elif key == 3 and len(parsed_com) == 1:
                print co.SCHEDULE.format(timing.today().replace(microsecond=0))
                for hour in self.schedule.hours:
                    if hour.running:
                        remaining = 'Running...'
                    else:
                        remaining = hour.lag_time()
                    print "    {}            {}".format(hour.time, remaining)

            # STATUS
            elif key == 4 and len(parsed_com) == 1:
                if self.schedule.next_hour().running:
                    print co.SCHEDULE_RUNNING.format(
                        self.schedule.next_hour().time,
                        self.schedule.remaining_time_run())
                elif self.electrovalve.moving:
                    print co.MOVING
                else:
                    print co.NEXT_RUN.format(
                        self.schedule.next_hour().lag_time())

            # CYCLE
            elif key == 5 and len(parsed_com) == 1:
                print co.CYCLE_INFO
                for output, tm in zip(co.CYCLE_OUTPUTS, self.schedule.cycle):
                    print "{}         {}".format(output, tm)

            # MOVE (INT)
            elif key == 6 and len(parsed_com) == 2:
                moves_num = int(parsed_com[1])
                duration = moves_num * co.GAP * co.GAP + co.GAP
                next_hour = self.schedule.next_hour()
                if (next_hour.lag() < duration) or\
                   (next_hour.running) or (self.electrovalve.moving):
                    print co.MOVE_ERROR
                else:
                    print co.MOVE_SUCCESS.format(moves_num)
                    moves = threading.Thread(target=self.electrovalve.move,
                                             args=(moves_num, self))
                    moves.daemon = False
                    moves.start()

            # STOP
            elif key == 7 and len(parsed_com) == 1:
                if (self.electrovalve.moving) or\
                   (self.schedule.next_hour().running):
                    self.stop = True
                    print co.JOB_STOPPED
                else:
                    print co.NOTHING_TO_STOP

            # POSITION
            elif key == 8 and len(parsed_com) == 1:
                print co.CURRENT_POSITION.format(
                    self.schedule.temporary_handler.position)

            # ADD_HOUR
            elif key == 9 and len(parsed_com) == 2:
                if parsed_com[1] == 'now':
                    new_hour = timing.current_hour()
                else:
                    new_hour = timing.Hour(*map(int, parsed_com[1].split(":")))
                accept = True
                for hour in self.schedule.hours:
                    difference = timing.abs(
                        (hour.datetime - new_hour.datetime).total_seconds())
                    if difference <= self.schedule.seconds_run:
                        accept = False
                if accept:
                    print co.HOUR_ADDED
                    self.schedule.add_hour(new_hour)
                else:
                    print co.HOUR_NOT_ADDED

            # REMOVE_HOUR
            elif key == 10 and len(parsed_com) == 2:
                old_hour = timing.Hour(*map(int, parsed_com[1].split(":")))
                for hour in self.schedule.hours:
                    if old_hour.datetime == hour.datetime:
                        self.schedule.remove_hour(old_hour)
                        print co.HOUR_REMOVED
                        break
                else:
                    print co.HOUR_NOT_REMOVED

            else:
                raise KeyError

        except (EOFError, KeyError, IndexError, ValueError):
            print co.WRONG_COMMAND

        self.run()


class StatusBulb(object):

    def __init__(self, pin=17):
        self.pin = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.output(self.pin, GPIO.LOW)

    def open(self):
        GPIO.output(self.pin, GPIO.HIGH)

    def close(self):
        GPIO.output(self.pin, GPIO.LOW)
