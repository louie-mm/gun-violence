from src.services.csv_service import csv_constants


class CsvClient:

    def __init__(self):
        self.filename = '../../raw_data/data_2018_02.csv'


def get_state_city_and_street_address(csv_row):
        return csv_row[csv_constants.STATE], csv_row[csv_constants.CITY], csv_row[csv_constants.ADDRESS]