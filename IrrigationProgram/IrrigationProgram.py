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
            self.water()
            return self._recursive_loop()

        sleep(1)

        if (self.is_running):
            return self._recursive_loop()

    def water(self):
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
