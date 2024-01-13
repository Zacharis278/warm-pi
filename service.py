import time

from database import Connection
from models import Reading

try:
    import piplates.THERMOplate as THERMO
except ImportError:
    print('sensor not found. Running in debug mode.')
    from test.mock_sensor import THERMOplate as THERMO


#DATABASE = ':memory:'
DATABASE = 'Test.db'
READ_INTERVAL_SECONDS = 1

db = None

def continuous_read():
    """ main loop to read from sensor each READ_INTERVAL_SECONDS """
    while True:
        try:
            value = THERMO.getTEMP(0, 1)
            value = int(value * 1.8 + 32)  # convert to fahrenheit
            reading = Reading(1, int(time.time()), value)
            db.write_reading(reading)
            time.sleep(READ_INTERVAL_SECONDS)
        except KeyboardInterrupt:
            break


if __name__ == '__main__':
    db = Connection(DATABASE)
    continuous_read()
