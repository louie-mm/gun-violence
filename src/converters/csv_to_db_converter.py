from datetime import datetime

from src.services.csv_service import csv_constants
from src.services.db_service import db_constants


def convert(csv_row, longitude=None, latitude=None):
    db_entry = {
        db_constants.ADDRESS: csv_row[csv_constants.ADDRESS],
        db_constants.CITY: csv_row[csv_constants.CITY],
        db_constants.STATE: csv_row[csv_constants.STATE],
        db_constants.KILLED: int(csv_row[csv_constants.KILLED]),
        db_constants.INJURED: int(csv_row[csv_constants.INJURED]),
        db_constants.OPERATIONS: csv_row[csv_constants.OPERATIONS],
        db_constants.DATE: _convert_date(csv_row[csv_constants.DATE]),
    }
    if longitude is not None and latitude is not None:
        db_entry[db_constants.LONGITUDE] = longitude
        db_entry[db_constants.LATITUDE] = latitude
    return db_entry


def _convert_date(date):
    return datetime.strptime(date, csv_constants.DATE_FORMAT)
