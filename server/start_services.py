import argparse
import subprocess


# Constant definitions
DEFAULT_IP_ADDRESS = '127.0.0.1'
DEFAULT_PORT = 8080
WEATHER_SESSION_NAME = 'ServerWeatherSession'
WEBSERVER_SESSION_NAME = 'WebServerSession'
ELECTROVALVE_SESSION_NAME = 'ElectrovalveControllerSession'
WEATHER_SERVICE_NAME = 'weather'
WEBSERVER_SERVICE_NAME = 'webserver'
ELECTROVALVE_SERVICE_NAME = 'electrovalve'

# Function definitions
def arguments_parser():
    parser = argparse.ArgumentParser(description='Starts all web-server services')
    parser.add_argument('service_names', metavar='SERVICE_NAME', type=str, nargs='+',
                        choices=[WEATHER_SERVICE_NAME, WEBSERVER_SERVICE_NAME,
                                 ELECTROVALVE_SERVICE_NAME, 'all'],
                        help='Name of all web-server services to start. Options are: ' +
                        '{}, {}, {}, {}'.format(WEATHER_SERVICE_NAME, WEBSERVER_SERVICE_NAME,
                                                ELECTROVALVE_SERVICE_NAME, 'all'))
    parser.add_argument('-i', '--ip_address', metavar='X.X.X.X', type=str, nargs=1,
                        help='IP address to launch the web-server on',
                        default=[DEFAULT_IP_ADDRESS, ])
    parser.add_argument('-p', '--port', metavar='N', type=int, nargs=1,
                        help='IP port to launch the web-server on',
                        default=[DEFAULT_PORT, ])
    args = parser.parse_args()

    for service_name in args.service_names:
        if (service_name not in (WEATHER_SERVICE_NAME,
                                 WEBSERVER_SERVICE_NAME,
                                 ELECTROVALVE_SERVICE_NAME,
                                 'all')):
            raise ValueError('Unknown service was found: \'{}\''.format(service_name))

    return args


def system_checks():
    print('System checks:')
    try:
        output = subprocess.run(['screen', '-v'], stdout=subprocess.PIPE)
    except FileNotFoundError:
        raise SystemError('Screen is not installed in this environment')
    print(' - Detected screen: {}'.format(output.stdout.decode('utf-8').strip()))


def main(args):
    print('Starting requested services:')
    if (WEATHER_SERVICE_NAME in args.service_names or 'all' in args.service_names):
        print(' - Starting weather service')
        output = subprocess.run(['screen', '-ls'], stdout=subprocess.PIPE)
        if (WEATHER_SESSION_NAME in output.stdout.decode('utf-8').strip()):
            print('  - Weather service already running')
        else:
            subprocess.Popen(['screen', '-S', WEATHER_SESSION_NAME, '-d', '-m',
                              'python', 'scripts/weather.py'],
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if (WEBSERVER_SERVICE_NAME in args.service_names or 'all' in args.service_names):
        host_address = "{}:{}".format(args.ip_address[0], args.port[0])
        print(' - Starting html server at {}'.format(host_address))
        output = subprocess.run(['screen', '-ls'], stdout=subprocess.PIPE)
        if (WEBSERVER_SESSION_NAME in output.stdout.decode('utf-8').strip()):
            print('  - Html server already running')
        else:
            subprocess.Popen(['screen', '-S', WEBSERVER_SESSION_NAME, '-d', '-m',
                              'python', 'manage.py', 'runserver', host_address])
    if (ELECTROVALVE_SERVICE_NAME in args.service_names or 'all' in args.service_names):
        host_address = "{}:{}".format(args.ip_address[0], args.port[0])
        print(' - Starting electrovalve controller')
        output = subprocess.run(['screen', '-ls'], stdout=subprocess.PIPE)
        if (ELECTROVALVE_SESSION_NAME in output.stdout.decode('utf-8').strip()):
            print('  - Electrovalve controller already running')
        else:
            subprocess.Popen(['screen', '-S', ELECTROVALVE_SESSION_NAME, '-d', '-m',
                              'python', 'scripts/electrovalve_controller.py'])
    print('Done')

if (__name__ == '__main__'):
    args = arguments_parser()
    system_checks()
    main(args)
