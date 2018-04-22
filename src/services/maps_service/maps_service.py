import time

import src.services.address_util.address_util as address_util
import src.services.maps_service.maps_constants as constants
from src.services.maps_service.maps_client_wrapper import MapsClientWrapper
from src.services.maps_service.maps_exception import MapsException


class MapsService:

    def __init__(self):
        self.maps = MapsClientWrapper
        self.daily_limit = constants.DAILY_LIMIT
        self.number_of_requests = 0

    def get_long_and_lat_from_address(self, state, city, street_address):
        geocode_result = self._request_geocode(state, city, street_address)
        if not geocode_result:
            geocode_result = self._request_geocode(state, city)
        if not geocode_result:
            raise MapsException('No geocode result for {0}, {1}, {2} or {1}, {2}'.format(street_address, city, state))
        return _get_long_and_lat_from_geocode(geocode_result)

    def is_limit_reached(self):
        return self.number_of_requests > self.daily_limit

    def _request_geocode(self, state, city, street_address=None):
        if self.is_limit_reached():
            raise MapsException('Attempt to request geocode after daily limit was reached')
        time.sleep(constants.SLEEP_SECONDS)
        self.number_of_requests += 1
        full_address = address_util.build_full_address(state, city, street_address)
        return self.maps.geocode(full_address)


def _get_long_and_lat_from_geocode(geocode_result):
    location = geocode_result[0]['geometry']['location']
    return location['lng'], location['lat']
