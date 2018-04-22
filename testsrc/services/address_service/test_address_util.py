import unittest

from src.services.address_util import address_util
from src.services.address_util.address_exception import AddressException


class TestAddressValidator(unittest.TestCase):
    def test_address_is_invalid(self):
        for invalid_city_name in ['', ' ', 'N/A', None, 434, '][}{}{', '3']:
            is_valid = address_util.is_valid_address('alabama', invalid_city_name)
            self.assertFalse(is_valid)
        for invalid_state_name in ['', ' ', 'N/A', None, 434, '][][', '3', 'Abu Dhabi', 'oklahooma']:
            is_valid = address_util.is_valid_address(invalid_state_name, 'Seattle')
            self.assertFalse(is_valid)
        for invalid_street_address in ['', ' ', 'N/A', 434, '][][', '3']:
            is_valid = address_util.is_valid_address('washington', 'Seattle', invalid_street_address)
            self.assertFalse(is_valid)

    def test_address_is_valid(self):
        for valid_city_name in ['new', 'new 2', 'new \'', 'new ][][3434']:
            is_valid = address_util.is_valid_address('alabama', valid_city_name)
            self.assertTrue(is_valid)
        for valid_state_name in ['Wyoming', 'KY', 'ky', 'NORTH CAROLINA']:
            is_valid = address_util.is_valid_address(valid_state_name, 'Seattle')
            self.assertTrue(is_valid)
        for valid_street_address in ['big house', '99 Pike Place']:
            is_valid = address_util.is_valid_address('Washington', 'Seattle', valid_street_address)
            self.assertTrue(is_valid)


class TestBuildAddress(unittest.TestCase):
    def test_throw_exception_when_building_invalid_address(self):
        self.assertRaises(AddressException, address_util.build_full_address, None, 'Seattle')
        self.assertRaises(AddressException, address_util.build_full_address, 'Washington', None)
        self.assertRaises(AddressException, address_util.build_full_address, 'Washington', 'Seattle', '90')

    def test_exclude_street_address_when_none(self):
        full_address = address_util.build_full_address('Washington', 'Seattle', None)
        self.assertTrue(not full_address.startswith(','))

    def test_valid_addresses(self):
        full_address = address_util.build_full_address('Washington', 'Seattle', '99 Pike Place')
        self.assertTrue(full_address.startswith('99 Pike Place, Seattle, Washington'))

        full_address = address_util.build_full_address('Washington', 'Seattle')
        self.assertTrue(full_address.startswith('Seattle, Washington'))
