import unittest
from unittest.mock import MagicMock, patch
from src.services.maps_service.maps_client import MapsClient, MapsException
import googlemaps
import src.services.maps_service.maps_constants as constants


class TestMapsClient(unittest.TestCase):

    # def __init__(self):
    #     super(TestMapsClient, self).__init__()
    #
    #     self.mock_maps_fails_every_time = googlemaps.Client(key=constants.KEY)
    #
    # def setUp(self):
    #     self.mock_maps_fails_every_time.geocode = MagicMock(return_value=None)  # TODO: Find actual return value for this case

    @patch('src.services.maps_service.maps_client.MapsClient')
    def test_tries_a_different_ways_to_get_long_and_lat_when_first_call_fails(self, mock_maps_client):
        mock_maps_client


    # def test_throws_exception_when_second_call_to_get_long_and_lat_fails:
    #     # make both calls fail
    #
    # def test_throws_exception_when_at_daily_limit_for_requests:
    #     # either first or second call might be limit
    #
    # def test_success_cases:
    #     # either first or second call is valid
    #
    # def test_raised_exception_when_calling_google:
    #     # Do we want it ot continue or fail?

    # TODO: test_response_for_daily_limit_from_google

    # TODO: test_responses_in_quick_succession_from_google