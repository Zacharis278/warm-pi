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
READ_INTERVAL_SECONDS = 5

db = None

def continuous_read():
    """ main loop to read from sensor each READ_INTERVAL_SECONDS """
    previous_value = 0
    while True:
        try:
            value = _to_farhenheit(THERMO.getTEMP(0, 1))
            adjusted_value = round(value)
            print(f'actual {value} -- previous {previous_value}')
            # stay sticky to previous reading if within 1 degree (c)
            # this prevents noisy data based on rounding the float
            if abs(previous_value - value) < 1:
                adjusted_value = previous_value
            previous_value = adjusted_value
            reading = Reading(1, int(time.time()), adjusted_value)
            db.write_reading(reading)
            time.sleep(READ_INTERVAL_SECONDS)
        except KeyboardInterrupt:
            break

def _to_farhenheit(celsius):
    return celsius * 1.8 + 32


if __name__ == '__main__':
    db = Connection(DATABASE)
    continuous_read()
