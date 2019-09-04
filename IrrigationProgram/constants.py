import datetime

TIMETABLE = (datetime.time(7)), datetime.time(19)

CYCLE = (900, 600, 600, 10, 10, 600)

CYCLE_OUTPUTS = ('Garden   ', 'Sideways ', 'Backyard ', 'Empty    ',
                 'Empty    ', 'Frontyard')

TEST_CYCLE = (10, 10, 10, 10, 10, 10)

GAP = 10
SECONDS_ONE_DAY = 86400

WELCOME = "Irrigation Program working\n--------------------------\n" +\
    " Enter any command below:"

WRONG_COMMAND = "Command not found. Type help to see a\n" +\
    "list of all the available commands."

COMMAND_LIST = {"": 0,
                "exit": 1,
                "help": 2,
                "schedule": 3,
                "status": 4,
                "cycle": 5,
                "move": 6,
                "stop": 7,
                "position": 8,
                "add_hour": 9,
                "remove_hour": 10}

COMMAND_HELP = ("...")

HELP = "List of commands:\n"

MOVING = 'Currently, the irrigation distributor is being moved'

SCHEDULE_RUNNING = "There is an irrigation program currently running:\n" +\
    " Started at: {}\n Remaining time: {}"

SCHEDULE = "\nSchedule:\n---------\nDate and time: {}\n\n" +\
    "Irrigation hours:    Remaining time:"

TEST_WARNING = "Testing all six water outputs..."

NEXT_RUN = "\nNext irrigation program running in:\n {}"

CYCLE_INFO = "\nIrrigation cycle:\n-----------------\n\n" +\
    "Output:    Irrigation time(s):"

MAIL = 'raspberrymunicoy@gmail.com'

MAIL_PSSWD = '447-Kyc-VqP-epy'

MAIL_MSG = 'Raspberry Pi activated the electrovalve successfully on {}.' +\
    ' More information about the irrigation schedule can be found below:\n'

MAIL_ENDING = '\n\nRaspberry Pi.'

MAIL_SUBJECT = 'Irrigation Notification'

MAIL_ERROR = 'No mail could be sent due to an unknown error.'

SEPARATOR = ''.center(40, '-')

MAIN_INFO = "Starting Irrigation Program"

CYCLE_DEBUG = "Creating a timer with a delay of {} seconds"

SCHEDULE_TEST = "Created a Schedule for testing."

SCHEDULE_DIR = "No input file found. Using default values for the Schedule."

SCHEDULE_PARSER = 'Reading Schedule information from file {}.'

ELECTROVALVE_SIMULATION = 'Electrovalve simulated.'

ELECTROVALVE_CONFIG = 'Electrovalve configurated on pin {}'

ELECTROVALVE_ON = 'Electrovalve turned on'

ELECTROVALVE_OFF = 'Electrovalve turned off'

IRRIGATION_SUCCESS = 'The Irrigation Program completed the irrigation cycle' +\
    'succesfully'

IRRIGATION_EXIT = 'The irrigation cycle was finished before its completion' +\
    'by a user call'

SEND_MAIL = 'An email was sent to the direction: {} telling' +\
    'that the irrigation was successfully performed'.format(MAIL)

MOVE_ERROR = 'This action was forbidden due to a current run scheduled before.'

MOVE_SUCCESS = 'Moving the Irrigation Distributor {} times'

TEMP_FILE = '.irprogram.tmp'

NO_TEMP_FILE = 'Warning! No temporary file found. Using default irrigation' +\
    'sequence'

TEMP_KEY1 = 'LAST_POSITION'

CURRENT_POSITION = 'The current position of the irrigation device is {}'

NOTHING_TO_STOP = 'At this time, there are no jobs to stop'

JOB_STOPPED = 'The current job has been stopped'

HOUR_ADDED = 'The hour was successfully added to the schedule'

HOUR_NOT_ADDED = 'The hour was not added to the schedule because it\n' +\
    'interferes with hours scheduled before'

HOUR_REMOVED = 'The hour was successfully removed from the schedule'

HOUR_NOT_REMOVED = 'The chosen hour could not be removed because it\n' +\
    'does not belong to the schedule yet'
