import csv

from src.converters import csv_to_db_converter
from src.etl import feature_flags
from src.services.address_util import address_exception, address_util
from src.services.csv_service import csv_service
from src.services.db_service import db_service, db_constants
from src.services.maps_service import maps_service, maps_exception


class CsvToDb:
    def __init__(self):
        self.db = db_service.DbService()
        self.maps = maps_service.MapsService()
        self.csv = csv_service.CsvService()

    def run(self):
        with open(self.csv.filename, 'r') as file:
            reader = csv.DictReader(file)
            try:
                self._read_rows_to_db(file)
            except csv.Error as e:
                print('Failed to open file %s, line %d: %s' % (self.csv.filename, reader.line_num, e))
        print('Total Repeated Incidents: ' + str(self.db.attempts_to_add_existing_data))

    def _read_rows_to_db(self, file):
        for csv_row in csv.DictReader(file):
            try:
                incident_model = csv_to_db_converter.convert(csv_row)
                # TODO: Need to find a way to cleanly decouple
                # TODO: Probably time to introduce
                if address_util.is_address_usable(
                        incident_model[db_constants.STATE], incident_model[db_constants.CITY], incident_model[db_constants.ADDRESS]):
                    print('Address is unusable: ' + incident_model)
                    continue
                if self.db.contains(incident_model):
                    print('DB Already contains ' + str(csv_row))
                    continue
                self._read_row_to_db(csv_row)
            except address_exception.AddressException or maps_exception.MapsException as e:
                print(e)

    def _read_row_to_db(self, csv_row):
        state, city, street_address = csv_service.get_state_city_and_street_address(csv_row)
        longitude, latitude = self._get_lat_and_long_from_address(state, city, street_address)
        db_entry = csv_to_db_converter.convert(csv_row, longitude, latitude)
        self.db.add(db_entry)

    def _get_lat_and_long_from_address(self, state, city, street_address):
        if not feature_flags.MAPS or self.maps.is_limit_reached():
            return None, None
        return self.maps.get_long_and_lat_from_address(state, city, street_address)

