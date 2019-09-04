import RPi.GPIO as GPIO
import logging as log
import constants as co
import timing
import time


class Electrovalve(object):

    def __init__(self, schedule, pin=27, sim=False, test=False):
        self.sim = sim
        self.pin = pin
        self.schedule = schedule
        if self.sim:
            log.info(co.ELECTROVALVE_SIMULATION)
            return
        self.moving = False
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.output(self.pin, GPIO.LOW)
        log.info(co.ELECTROVALVE_CONFIG.format(str(self.pin)))

    def open(self):
        if self.sim:
            return
        GPIO.output(self.pin, GPIO.HIGH)
        log.debug(co.ELECTROVALVE_ON)
        self.schedule.update_position()

    def close(self):
        if self.sim:
            return
        GPIO.output(self.pin, GPIO.LOW)
        log.debug(co.ELECTROVALVE_OFF)

    def move(self, times, interface):
        def exit():
            return interface.stop

        self.moving = True
        for i in xrange(times):
            self.open()
            timing.wait(co.GAP, exit)
            self.close()
            if interface.stop:
                break
            time.sleep(co.GAP)
        self.moving = False
        interface.stop = False
