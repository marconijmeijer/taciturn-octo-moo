#!/usr/bin/env python

import RPi.GPIO as GPIO
import logging
import logging.handlers
import argparse
import sys
import time
import requests
import signal

# Deafults
LOG_FILENAME = "/tmp/switch-service.log"
LOG_LEVEL = logging.INFO  # Could be e.g. "DEBUG" or "WARNING"

# Define and parse command line arguments
parser = argparse.ArgumentParser(description="Python service for checking switch on GPIO 18,23,24 en 25")
parser.add_argument("-l", "--log", help="file to write log to (default '" + LOG_FILENAME + "')")

# If the log file is specified on the command line then override the default
args = parser.parse_args()
if args.log:
        LOG_FILENAME = args.log

# Configure logging to log to a file, making a new file at midnight and keeping the last 3 day's data
# Give the logger a unique name (good practice)
logger = logging.getLogger(__name__)
# Set the log level to LOG_LEVEL
logger.setLevel(LOG_LEVEL)
# Make a handler that writes to a file, making a new file at midnight and keeping 3 backups
handler = logging.handlers.TimedRotatingFileHandler(LOG_FILENAME, when="midnight", backupCount=3)
# Format each log message like this
formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
# Attach the formatter to the handler
handler.setFormatter(formatter)
# Attach the handler to the logger
logger.addHandler(handler)

# Make a class we can use to capture stdout and sterr in the log
class MyLogger(object):
        def __init__(self, logger, level):
                """Needs a logger and a logger level."""
                self.logger = logger
                self.level = level

        def write(self, message):
                # Only log if there is a message (not just a new line)
                if message.rstrip() != "":
                        self.logger.log(self.level, message.rstrip())

# Replace stdout with logging to file at INFO level
sys.stdout = MyLogger(logger, logging.INFO)
# Replace stderr with logging to file at ERROR level
sys.stderr = MyLogger(logger, logging.ERROR)

logger.info("Starting switch service")


class GracefulKiller:
        kill_now = False
        def __init__(self):
                signal.signal(signal.SIGINT, self.exit_gracefully)
                signal.signal(signal.SIGTERM, self.exit_gracefully)

        def exit_gracefully(self,signum, frame):
                self.kill_now = True




GPIO.setmode(GPIO.BCM)

# GPIO 18 set up as input, pulled up
# 18 will go to GND when button pressed.
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(25, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# now we'll define the threaded callback function
# this will run in another thread when our event is detected
def my_callback(channel):
        logger.info("Button pressed on port "+channel)


def my_callback1(channel):
        logger.info("Button pressed on port 18")
        logger.info("Calling Jenkins : ")
        logger.info(requests.get(url='http://jenkinsServer:8080/job/BuildJob/build?token=h55U4NO6IW&cause=redButton'))

def my_callback2(channel):
        logger.info("Button pressed on port 23")
        logger.info("NOT IMPLEMENTED YET")

def my_callback3(channel):
        logger.info("Button pressed on port 24")
        logger.info("NOT IMPLEMENTED YET")

def my_callback4(channel):
        logger.info("Button pressed on port 25")
        logger.info("NOT IMPLEMENTED YET")



logger.info("listen on port 18")
GPIO.add_event_detect(18, GPIO.RISING, callback=my_callback1, bouncetime=500)

logger.info("listen on port 23")
GPIO.add_event_detect(23, GPIO.RISING, callback=my_callback2, bouncetime=500)

logger.info("listen on port 24")
GPIO.add_event_detect(24, GPIO.RISING, callback=my_callback3, bouncetime=500)

logger.info("listen on port 25")
GPIO.add_event_detect(25, GPIO.RISING, callback=my_callback4, bouncetime=500)



# Loop forever, doing something useful hopefully:
if __name__ == '__main__':
        killer = GracefulKiller()
        while True:
                time.sleep(1)
                if killer.kill_now:
                        break

        logger.info("Switch-Service stopped.")
        logger.info("Clean up GPIO")
        GPIO.cleanup()
