# oximeter

usage: `oximeter-c.py [-h] [-d] [-t T] host`

Oximeter: a program that contacts another host simply to let it know that it's
alive.

positional arguments:


* host        The remote computer to connect to.

optional arguments:


* `-h, --help  show this help message and exit`
* `-d          Specifies wheter to run Oximeter client in daemon mode.`
* `-t T        Optional time in seconds between sending a pulse in daemon mode. Default is 3600 (one hour).`
