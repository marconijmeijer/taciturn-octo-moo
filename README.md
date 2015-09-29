# taciturn-octo-moo
Python service for checking switch on RaspberryPi GPIO 18,23,24 en 25

# Installeren
Kopieer beide file naar de home folder van je raspberry user


# Installeer python button controller
Kopieer switch-service.py naar /usr/local/bin/switch-service
> cd /usr/local/bin/
> sudo mkdir switch-service
> sudo chown -R pi:pi switch-service/
> cd switch-service/
> cp ~/switch-service.py .
> chmod 755 switch-service.py

Edit regel 13 en 14 en configureer de juiste pade
LOG_FILENAME = "/tmp/switch-service.log"
LOG_LEVEL = logging.INFO  # Could be e.g. "DEBUG" or "WARNING"


# (optioneel) Installeer auto startup service
kopieer switch-service.sh naar /etc/init.d/
> sudo cp switch-service.sh /etc/init.d/

Edit regel 14,15 en 16. Vul hier de juiste paden in.
DIR=/usr/local/bin/switch-service
DAEMON=$DIR/switch-service.py
DAEMON_NAME=switch-service

Creeer startup scripts
> sudo update-rc.d switch-service.sh defaults

Start service
> sudo service switch-service.sh start




