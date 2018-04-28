import unittest
from unittest.mock import MagicMock, call

from src.services.maps_service import maps_service
from src.services.maps_service.maps_exception import MapsException
from src.services.address_util.address_exception import AddressException


class TestMapsClient(unittest.TestCase):

    def setUp(self):
        self.maps_service = maps_service.MapsService()
        self.maps_service.wait_time = 0

    def test_success_case_on_first_call(self):
        mock_geocode = MagicMock(side_effect=geocode_always_succeeds)
        self.maps_service.maps_client.geocode = mock_geocode

        actual_long, actual_lat = self.maps_service.get_long_and_lat_from_address(state, city, street_address)

        mock_geocode.assert_called_once_with(full_address)
        self.assertEquals(actual_long, expected_long)
        self.assertEquals(actual_lat, expected_lat)

    def test_tries_a_different_way_to_get_long_and_lat_when_first_call_fails(self):
        mock_geocode = MagicMock(side_effect=geocode_success_on_second_call)
        self.maps_service.maps_client.geocode = mock_geocode

        actual_long, actual_lat = self.maps_service.get_long_and_lat_from_address(state, city, street_address)

        mock_geocode.assert_has_calls([call(full_address), call(part_address)], any_order=False)
        self.assertEquals(actual_long, expected_long)
        self.assertEquals(actual_lat, expected_lat)

    def test_throws_exception_when_second_call_to_get_long_and_lat_fails(self):
        mock_geocode = MagicMock(side_effect=geocode_always_fails)
        self.maps_service.maps_client.geocode = mock_geocode

        self.assertRaises(MapsException, self.maps_service.get_long_and_lat_from_address, state, city, street_address)

    def test_throws_exception_when_at_daily_limit_for_requests(self):
        mock_geocode = MagicMock(side_effect=geocode_success_on_second_call)
        self.maps_service.maps_client.geocode = mock_geocode

        # Fail on first request
        self.maps_service.number_of_requests = self.maps_service.daily_limit
        self.assertRaises(MapsException, self.maps_service.get_long_and_lat_from_address, state, city, street_address)

        # Fail on second request
        self.maps_service.number_of_requests = self.maps_service.daily_limit - 1
        self.assertRaises(MapsException, self.maps_service.get_long_and_lat_from_address, state, city, street_address)

    def test_throws_exception_for_bad_addresses(self):
        mock_geocode = MagicMock(side_effect=geocode_always_fails)
        self.maps_service.maps_client.geocode = mock_geocode

        self.assertRaises(AddressException, self.maps_service.get_long_and_lat_from_address, 'very', 'strange', 'address')

    # TODO: test_response_for_daily_limit_from_google (replicate then code for soln)
    # TODO: test_responses_in_quick_succession_from_google (replicate then code soln)
    # TODO: test when request can't reach google (try calling without internet and see what happens)


def geocode_success_on_second_call(value):
    if value == full_address:
        return cant_find
    if value == part_address:
        return success
    raise ValueError("Unexpected value in unit test. Expect: \"" + part_address + "\" or \"" + full_address + "\"")


def geocode_always_fails(value):
    if value == full_address or value == part_address:
        return cant_find
    raise ValueError("Unexpected value in unit test. Expect: \"" + part_address + "\" or \"" + full_address + "\"")


def geocode_always_succeeds(value):
    if value == full_address or value == part_address:
        return success
    raise ValueError("Unexpected value in unit test. Expect: \"" + part_address + "\" or \"" + full_address + "\"")

state = "Washington"
city = "Seattle"
street_address = "99 Pike Ave"

part_address = city + ", " + state + ", USA"
full_address = street_address + ", " + part_address

expected_long = -101.8428718
expected_lat = 35.2284232

success = [{
        'geometry': {
            'location': {
                'lat': expected_lat,
                'lng': expected_long
            }
        }
    }]

cant_find = []
