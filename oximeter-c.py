import socket
import sys
from urllib.request import urlopen
import atexit
from signal import signal, SIGINT, SIGTERM
from time import sleep, localtime, strftime, gmtime
import argparse
#v3.0 for python 3.6
#JAN 6 2018
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
def signal_handler(signal, frame):
    print("Sending signal...")
    sock.sendall((str(signal)+" signal on "+socket.gethostname()+" at "+strftime("%Y-%m-%d %H:%M:%S", gmtime())+" GMT\n").encode())
    exit()
def exit_handler():
    print("Sending shutdown signal...")
    sock.sendall(("Daemon exit on "+socket.gethostname()+" at "+strftime("%Y-%m-%d %H:%M:%S", gmtime())+" GMT\n").encode())


parser = argparse.ArgumentParser(description="Oximeter: a program that contacts another host simply to let it know that it's alive.")
parser.add_argument("host", help="The remote computer to connect to.", type=str)
parser.add_argument("-d", help='Specifies wheter to run Oximeter Client in Daemon Mode.', action="store_true")
parser.add_argument("-t", help="Optional time in seconds between sending a pulse. Default is 3600 (one hour).", type=int)
args = parser.parse_args()
daemon = bool(args.d)
if daemon:
    atexit.register(exit_handler)
    signal(SIGINT, signal_handler)
    signal(SIGTERM, signal_handler)
if (args.host):
    host_str = args.host
if (args.t):
    sleep_int = args.t
else:
    sleep_int = 3600
    
host_ip = socket.gethostbyname(host_str)
client_ip = str(urlopen("https://connorsco.de/ip.php").read())
server_address = (host_ip, 25001)

print('Connecting to %s port %s' % server_address)
sock.connect(server_address)
while True:
    time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    message =socket.gethostname()+" ("+client_ip+") "+time+" GMT\n"
    print("Sending pulse to %s at %s GMT" % (host_ip, time))
    sock.sendall(message.encode())
    if not daemon:
        break
    sleep(sleep_int)
