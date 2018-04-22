import csv

from src.facades.converters import csv_to_db_converter
from src.facades.download_facade import feature_flags
from src.services.address_util import address_util, address_exception
from src.services.csv_service import csv_service
from src.services.db_service import db_service
from src.services.maps_service import maps_service, maps_exception


class CsvToDb:
    def __init__(self):
        self.db = db_service.DbClient()
        self.maps = maps_service.MapsService()
        self.csv = csv_service.CsvService()

    def run(self):
        with open(self.csv.filename, 'r') as file:
            reader = csv.DictReader(file)
            try:
                self._read_rows_to_db(file)
            except csv.Error as e:
                print('file %s, line %d: %s' % (self.csv.filename, reader.line_num, e))
        print('Total Repeated Incidents: ' + str(self.db.attempts_to_add_existing_data))

    def _read_rows_to_db(self, file):
        for csv_row in csv.DictReader(file):
            try:
                db_entry = csv_to_db_converter.convert(csv_row)
                if self.db.contains(db_entry):
                    print('DB Already contains ' + str(csv_row))
                    continue
                self._read_row_to_db(csv_row)
            except address_exception.AddressException or maps_exception.MapsException as e:
                print(e)

    def _read_row_to_db(self, csv_row):
        state, city, street_address = csv_service.get_state_city_and_street_address(csv_row)
        _verify_if_address_is_usable(state, city, street_address)
        longitude, latitude = self._get_lat_and_long_from_address(state, city, street_address)
        db_entry = csv_to_db_converter.convert(csv_row, longitude, latitude)
        self.db.add(db_entry)

    def _get_lat_and_long_from_address(self, street_address, city, state):
        if not feature_flags.MAPS or self.maps.is_limit_reached():
            return None, None
        return self.maps.get_long_and_lat_from_address(state, city, street_address)


def _verify_if_address_is_usable(state, city, street_address):
    if not address_util.is_valid_address(state, city, street_address):
        print('Unusual address found. Still saving to database: {}, {}, {}'.format(street_address, city, state))
    if not address_util.is_valid_address(state, city):
        raise address_exception.AddressException('Address {}, {}, {} is unusable'.format(street_address, city, state))
