import time

from src.services.db_service import db_constants, db_service
from src.ws.services import json_fields


class ShootingsFacade:
    def __init__(self):
        self.db = db_service.DbClient()

    def build_array(self):
        all_data = self.db.find_all()
        array = []
        for entry in all_data:
            if entry[db_constants.KILLED] != 0:
                array.append(_build_api_entry(entry, json_fields.KILLED))
            if entry[db_constants.INJURED] != 0:
                array.append(_build_api_entry(entry, json_fields.INJURED))
        return array

    def build_optimized_array(self):
        # TODO: Is this more efficient as a DB query? Even when sorting to maintain order?
        # TODO: There may come a point where this is too much for memory. Look into doing this in separate queries
        all_data = self.db.find_all()
        optimized_dictionary = {}
        for entry in all_data:
            current_date = str(time.mktime(entry[db_constants.DATE].timetuple()))
            if current_date not in optimized_dictionary:
                optimized_dictionary[current_date] = []
            incidents_at_date = optimized_dictionary[current_date]
            if entry[db_constants.KILLED] != 0:
                incidents_at_date.append(_build_optimized_api_entry(entry, json_fields.KILLED))
            if entry[db_constants.INJURED] != 0:
                incidents_at_date.append(_build_optimized_api_entry(entry, json_fields.INJURED))
            optimized_dictionary[current_date] = incidents_at_date
        return optimized_dictionary


def _build_api_entry(entry, entry_type):
    return {
        json_fields.NUMBER: _get_number(entry, entry_type),
        json_fields.LATITUDE: entry[db_constants.LATITUDE],
        json_fields.LONGITUDE: entry[db_constants.LONGITUDE],
        json_fields.TYPE: entry_type,
        json_fields.DATE: entry[db_constants.DATE]
    }


def _build_optimized_api_entry(entry, entry_type):
    return {
        json_fields.NUMBER: _get_number(entry, entry_type),
        json_fields.LATITUDE: entry[db_constants.LATITUDE],
        json_fields.LONGITUDE: entry[db_constants.LONGITUDE],
        json_fields.TYPE: entry_type
    }


def _get_number(entry, entry_type):
    if entry_type == json_fields.KILLED:
        return entry[db_constants.KILLED]
    else:
        return entry[db_constants.INJURED]
