from src.services.csv_service import csv_constants


class CsvService(object):

    def __init__(self):
        self.filename = '../../raw_data/data_2018_02.csv'


def get_state_city_and_street_address(csv_row):
        state = csv_row[csv_constants.STATE]
        city = csv_row[csv_constants.CITY]
        street_address = csv_row[csv_constants.ADDRESS]
        return state, city, street_address
