from dataclasses import dataclass
import sqlite3
from sqlite3 import Error
import time

try:
    import piplates.THERMOplate as THERMO
except ImportError:
    print('sensor not found. Running in debug mode.')
    from test.mock_sensor import THERMOplate as THERMO


DATABASE = 'Test.db'
READ_INTERVAL_SECONDS = 1

connection = None

@dataclass
class Reading():
    channel: int
    timestamp: int
    value: float

def continuous_read():
    """ main loop to read from sensor each READ_INTERVAL_SECONDS """
    while True:
        try:
            value = THERMO.getTEMP(0, 1)
            reading = Reading(1, int(time.time()), value)
            write_reading(reading)
            time.sleep(READ_INTERVAL_SECONDS)
        except KeyboardInterrupt:
            break

def write_reading(reading):
    """ save temperature reading to database """
    sql = ''' INSERT INTO temp_reading(channel, timestamp, value)
                VALUES(?,?,?) '''
    cur = connection.cursor()
    cur.execute(sql, [reading.channel, reading.timestamp, reading.value])
    connection.commit()
    print(f'wrote reading - {reading}')

def create_connection(db_file):
    """ create a database connection """
    try:
        return sqlite3.connect(db_file)
        print(f'connected. dbversion: {sqlite3.version}')
    except Error as e:
        print(e)


if __name__ == '__main__':
    connection = create_connection(DATABASE)
    continuous_read()
