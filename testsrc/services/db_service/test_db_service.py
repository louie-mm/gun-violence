import unittest
from unittest.mock import MagicMock, call
from src.services.db_service import db_service, db_constants


class TestAddingToDb(unittest.TestCase):

    def setUp(self):
        self.db_service = db_service.DbService()
        self.db_service.db.shootings = MagicMock()

    def test_doesnt_try_to_add_repeat_data(self):
        mock_find_one = MagicMock(side_effect=does_contain)
        self.db_service.db.shootings.find_one = mock_find_one
        mock_insert_one = MagicMock()
        self.db_service.db.shootings.insert_one = mock_insert_one

        self.db_service.add(dummy_db_entry)

        mock_find_one.assert_called_once_with(dummy_db_entry)
        mock_insert_one.assert_not_called()
        self.assertEquals(self.db_service.attempts_to_add_existing_data, 1)

    def test_does_add_non_repeat_data(self):
        mock_find_one = MagicMock(side_effect=does_not_contain)
        self.db_service.db.shootings.find_one = mock_find_one
        mock_insert_one = MagicMock()
        self.db_service.db.shootings.insert_one = mock_insert_one

        self.db_service.add(dummy_db_entry)

        mock_find_one.assert_called_once_with(dummy_db_entry)
        mock_insert_one.assert_called_once_with(dummy_db_entry)
        self.assertEquals(self.db_service.attempts_to_add_existing_data, 0)

# TODO: Test for initialization


def does_not_contain(value):
    return None


def does_contain(value):
    return value

dummy_db_entry = {
    db_constants.ADDRESS: '99 Pike Place',
    db_constants.CITY: 'Seattle',
    db_constants.STATE: 'Washington',
    db_constants.KILLED: 1,
    db_constants.INJURED: 2,
    db_constants.OPERATIONS: 'N/A',
    db_constants.DATE: 1110828398283,
    db_constants.LONGITUDE: -101.8428718,
    db_constants.LATITUDE: 35.2284232
}