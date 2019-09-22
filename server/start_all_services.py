import argparse
import subprocess


# Constant definitions
DEFAULT_IP_ADDRESS = '127.0.0.1'
DEFAULT_PORT = 8080


# Function definitions
def arguments_parser():
    parser = argparse.ArgumentParser(description='Starts all web-server services')
    parser.add_argument('-I', '--ip_address', metavar='X.X.X.X', type=str, nargs=1,
                        help='IP address to launch the web-server on',
                        default=[DEFAULT_IP_ADDRESS, ])
    parser.add_argument('-p', '--port', metavar='N', type=int, nargs=1,
                        help='IP address to launch the web-server on',
                        default=[DEFAULT_PORT, ])
    args = parser.parse_args()
    return args


def main(args):
    print('Starting all web-server services:')
    print(' - Starting weather service')
    subprocess.Popen(['python', 'scripts/weather.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    host_address = "{}:{}".format(args.ip_address[0], args.port[0])
    print(' - Starting html server at {}'.format(host_address))
    subprocess.Popen(['python', 'manage.py', 'runserver', host_address])


if (__name__ == '__main__'):
    args = arguments_parser()
    main(args)
