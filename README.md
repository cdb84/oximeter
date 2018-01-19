# oximeter
All programs use TCP/IP port 25001.
## Client
usage: `oximeter-c.py [-h] [-d] [-t T] host`

Oximeter: a program that contacts another host simply to let it know that your computer is alive.

positional arguments:


* `host`
  * The remote computer to connect to.

optional arguments:


* `-h, --help`
  * show this help message and exit
* `-d`
  * Specifies wheter to run Oximeter client in daemon mode.
* `-t T`
  * Optional time in T seconds between sending a pulse in daemon mode. Default is 3600 (one hour).
* `-g, --use-geo`
  * Use geo-location services. Accuracy may vary. Currently sends country code, city, and region.
* `-gv, --geographically-verbose`     
  * Include latitude and longitude.
## Server

The `oximeter-server` file is a shell script. It creates a netcat process and records the pid to a temp file. Output logs can be found in /var/log/oximeter/.

usage: `bash oximeter-server {start|stop|restart}` (for startin in a TTY)

In order to add the server to your machine's startup:

1. First move the sctip to `/etc/init.d/` with `sudo cp -v ./oximeter-server /etc/init.d/`
1. Run the commant `sudo update-rc.d oximeter-server default` to configure SystemV and LSB info
1. Either wait for next reboot to start the server, or run `sudo service oximeter-server start`


### Todo

- [ ] Add C/C++ sources so that we don't have to rely on Python and Python Alone
- [x] Write a better server daemon
- [ ] Use only libraries that Python3.4 for Windows is comfortable with :/

### Pipe Dreams

- [x] Add geo-location
- [ ] Create a whitelist so that unknown randos can't send their pulses to your server (even though it wouldn't make sense(???))
