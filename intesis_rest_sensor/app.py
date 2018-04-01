import json
import os
import logging
import configparser
from flask import Flask
from pyintesishome import IntesisHome

app = Flask(__name__)
logging.getLogger().setLevel(logging.DEBUG)

config = configparser.ConfigParser()
config.read('config.ini')

_username = config.get('Intesis', 'Username')
_password = config.get('Intesis', 'Password')
logging.info('Trying to connect to IntesisHome with username %s and password %s', _username, _password)
server = IntesisHome(_username, _password)

logging.info('Polling for device statuses...')
server.poll_status(False)

@app.route('/<device_id>')
def get_temperature(device_id):
    logging.info('Requesting temperature for device_id: %s', device_id)
    temperature = server.get_temperature(device_id)
    logging.info('Temperature is: %s', temperature)
    return json.dumps(temperature)

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
