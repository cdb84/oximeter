import socket
import sys
from urllib.request import urlopen
import atexit
from signal import signal, SIGINT, SIGTERM
from time import sleep, localtime, strftime, gmtime
import argparse
import requests
import json
#v4.0 DEV for python 3.6
#JAN 9 2018
send_url = "http://freegeoip.net/json"
ip_get_url = "https://api.ipify.org"
_default_sleep_ = 3600
_port_ = 25001
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#Define a signal handler that sends a distress call
def signal_handler(signal, frame):
    print("Sending signal...")
    sock.sendall((str(signal)+" signal on "+socket.gethostname()+" at "+strftime("%Y-%m-%d %H:%M:%S", gmtime())+" GMT\n").encode())
    exit()
#define an exit handler that sends a distress call
def exit_handler():
    print("Sending shutdown signal...")
    sock.sendall(("Daemon exit on "+socket.gethostname()+" at "+strftime("%Y-%m-%d %H:%M:%S", gmtime())+" GMT\n").encode())


parser = argparse.ArgumentParser(description="Oximeter: a program that contacts another host to remotely monitor system status.")
parser.add_argument("host", help="The remote computer to connect to.", type=str)
parser.add_argument("-d", help='Specifies wheter to run Oximeter client in daemon mode.', action="store_true")
parser.add_argument("-t", help="Optional time in seconds between sending a pulse in daemon mode. Default is 3600 (one hour).", type=int)
parser.add_argument("-g", "--use-geo", help="Use geo-location services. Accuracy may vary. Currently sends country code, city, and region.", action="store_true")
parser.add_argument("-gv", "--geographically-verbose", help="Include latitude and longitude.", action="store_true")
args = parser.parse_args()
daemon = bool(args.d)
#handlers only needed for daemon mode
if daemon: 
    atexit.register(exit_handler)
    signal(SIGINT, signal_handler)
    signal(SIGTERM, signal_handler)
if (args.host):
    host_str = args.host
#assume user values for sleep interval
if (args.t): 
    sleep_int = args.t
#assume default values for sleep interval
else: 
    sleep_int = _default_sleep_
    
#resolve the host
host_ip = socket.gethostbyname(host_str)
#create a tuple/ordered pair for our host and port
server_address = (host_ip, _port_)
#gather information about our client (just the ip)
#TODO: use requests.get(ip_get_url) instead of urllib
client_ip = str(urlopen(ip_get_url).read())
#trim some unicode leftovers
client_ip = client_ip.replace("b", "")
client_ip = client_ip.replace("'", "")

#make our connection
sock.connect(server_address)
while True:
    #get the current time in GMT/UTC
    time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    #start developing a message to send across TCP
    message = time+" GMT "+socket.gethostname()+" ("+client_ip+") \n"
    #considering geoip options:
    if (args.use_geo or args.geographically_verbose):
        message = message.replace("\n", " ")
        r = requests.get(send_url)
        j = json.loads(r.text)
        lat = j['latitude']
        lon = j['longitude']
        #add what the user requested to the send message
        message += j['city']+", "
        message += j['region_code']+", "
        message += j['zip_code']+" "
        message += j['country_code']+" "
        #add more if the -gv option was specified
        if args.geographically_verbose:
            message += "Lat, Long: "
            message += str(lat)+", "
            message += str(lon)

        message+="\n"
    #tell the user what's going on
    print("Sending pulse to %s at %s GMT" % (host_ip, time))
    #ship the message
    sock.sendall(message.encode())
    if not daemon:
        break #we only need to do this once if not daemonized
    #otherwise, sleep and repeat
    sleep(sleep_int)
