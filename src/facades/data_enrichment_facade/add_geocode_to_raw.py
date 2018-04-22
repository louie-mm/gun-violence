from datetime import datetime

from src.services.db_service import db_constants, db_service
from src.services.maps_service import maps_service, maps_exception
from src.services.address_util import address_exception


class AddGeoCodesToDb:
    def __init__(self):
        self.db = db_service.DbClient()
        self.maps = maps_service.MapsService()
        self.year_rage = list(range(2014, datetime.now().year + 1))

    def run(self):
        for year in self.year_rage:
            # TODO: Year is too large. Should change this to month
            records = self._find_records_for_year(year)
            self._enrich_records(records)

    def _find_records_for_year(self, year):
        # TODO: Use Calendar to change this to month
        start = datetime(year, 1, 1)
        end = datetime(year + 1, 1, 1)
        return self.db.find_between_dates(start, end)

    def _enrich_records(self, records):
        for record in records:
            try:
                if db_constants.LATITUDE in record and db_constants.LONGITUDE in record:
                    print('Record already has Long and Lat. Skipping record: ' + str(record))
                    continue
                self._update_db_with_geocode(record)
            except maps_exception.MapsException or address_exception.AddressException as e:
                print(e)

    def _update_db_with_geocode(self, record):
        longitude, latitude = self.maps.get_long_and_lat_from_address(
            record[db_constants.STATE], record[db_constants.CITY], record[db_constants.ADDRESS]
        )
        db_update = {
            db_constants.LATITUDE: latitude,
            db_constants.LONGITUDE: longitude
        }
        self.db.update(record, db_update)
