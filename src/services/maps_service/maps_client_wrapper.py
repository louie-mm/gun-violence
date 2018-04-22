import googlemaps

import src.services.maps_service.maps_constants as constants


class MapsClientWrapper:

    def __init__(self):
        self.maps_client = googlemaps.Client(key=constants.KEY)

    def geocode(self, full_address):
        self.maps_client.geocode(full_address)
