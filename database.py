import sqlite3
from sqlite3 import Error

from models import Reading


class Connection:
    def __init__(self, db_file):
        self.db_file = db_file
        self._create_connection(db_file)

    def _create_connection(self, db_file):
        """ create a database connection """
        try:
            self.connection = sqlite3.connect(db_file)
            print(f'connected. dbversion: {sqlite3.version}')
        except Error as e:
            print(e)

    def _map_to_reading(self, cursor, row):
        return Reading(*row)

    def write_reading(self, reading):
        """ save temperature reading to database """
        sql = ''' INSERT INTO temp_reading(channel, timestamp, value)
                    VALUES(?,?,?) ''' 
        cur = self.connection.cursor()
        cur.execute(sql, [reading.channel, reading.timestamp, reading.value])
        self.connection.commit()
        print(f'write_reading -- {reading}')

    def get_readings(self, start_datetime, end_datetime):
        """ get all readings between start and end datetime """
        sql = ''' SELECT channel, timestamp, value FROM temp_reading
            WHERE timestamp BETWEEN ? AND ? '''
        cur = self.connection.cursor()
        cur.execute(sql, (start_datetime.timestamp(), end_datetime.timestamp()))
        cur.row_factory = self._map_to_reading
        return cur.fetchall()
