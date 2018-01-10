import socket
import sys
from urllib.request import urlopen
import atexit
from signal import signal, SIGINT, SIGTERM
from time import sleep, localtime, strftime, gmtime
import argparse
import requests
import json
#v4.0 for python 3.6
#JAN 9 2018
_default_sleep_ = 3600
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
parser.add_argument("-d", help='Specifies wheter to run Oximeter client in daemon mode.', action="store_true")
parser.add_argument("-t", help="Optional time in seconds between sending a pulse in daemon mode. Default is 3600 (one hour).", type=int)
parser.add_argument("-g", "--use-geo", help="Use geo-location services. Accuracy may vary. Currently sends country code, city, and region.", action="store_true")
parser.add_argument("-gv", "--geographically-verbose", help="Include latitude and longitude.", action="store_true")
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
    sleep_int = _default_sleep_
    
host_ip = socket.gethostbyname(host_str)
server_address = (host_ip, 25001)

send_url = 'http://freegeoip.net/json'

client_ip = str(urlopen("https://api.ipify.org").read())
client_ip = client_ip.replace("b", "")
client_ip = client_ip.replace("'", "")


sock.connect(server_address)
while True:
    time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    message = time+" GMT "+socket.gethostname()+" ("+client_ip+") \n"
    if (args.use_geo or args.geographically_verbose):
        message = message.replace("\n", " ")
        r = requests.get(send_url)
        j = json.loads(r.text)
        lat = j['latitude']
        lon = j['longitude']
        
        message += j['city']+", "
        message += j['region_code']+", "
        message += j['country_code']+" "

        if args.geographically_verbose:
            message += "Lat, Long: "
            message += str(lat)+", "
            message += str(lon)

        message+="\n"
        
    print("Sending pulse to %s at %s GMT" % (host_ip, time))
    #print(message)
    sock.sendall(message.encode())
    if not daemon:
        break
    sleep(sleep_int)
