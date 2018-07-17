from datetime import datetime, timedelta

from src.services.db_service import db_constants, db_service
from src.ws.services import json_fields


class ShootingsFacade:
    def __init__(self):
        self.db = db_service.DbService()

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
        optimized_dictionary = {}
        start_date = _format_datetime(datetime.max)
        end_date = 0
        next_date = None
        total_deaths_for_date = 0
        total_injuries_for_date = 0
        total_deaths = 0
        total_injuries = 0
        for entry in self.db.find_all():
            current_date = _format_datetime(entry[db_constants.DATE])
            if current_date > end_date:
                end_date = current_date
            if current_date < start_date:
                start_date = current_date

            # TODO: Everything below here can be moved to a separate function
            if current_date not in optimized_dictionary:
                total_deaths_for_date = 0
                total_deaths_for_date = 0
                optimized_dictionary[current_date] = {
                    'incidents': [],
                    'next': next_date
                }
            incidents_at_date = optimized_dictionary[current_date]['incidents']

            if entry[db_constants.KILLED] != 0:
                total_deaths_for_date = total_deaths_for_date + entry[db_constants.KILLED]
                total_deaths = total_deaths + entry[db_constants.KILLED]
                incidents_at_date.append(_build_optimized_api_entry(entry, json_fields.KILLED))
            if entry[db_constants.INJURED] != 0:
                total_injuries_for_date = total_injuries_for_date + entry[db_constants.INJURED]
                total_injuries = total_injuries + entry[db_constants.INJURED]
                incidents_at_date.append(_build_optimized_api_entry(entry, json_fields.INJURED))
            optimized_dictionary[current_date]['incidents'] = incidents_at_date
            optimized_dictionary[current_date]['totalDeathsForDate'] = total_deaths_for_date
            optimized_dictionary[current_date]['totalInjuriesForDate'] = total_injuries_for_date
            next_date = current_date
        # TODO: Throw exception if start date is greater than end date
        temp_date = start_date
        start_date = _format_datetime(datetime.strptime(str(start_date), "%y%m%d") - timedelta(days=1))
        optimized_dictionary[start_date] = {
            'incidents': [],
            'next': temp_date,
            'totalDeathsForDate': 0,
            'totalInjuriesForDate': 0
        }
        response_body = {
            'startDate': start_date,
            'endDate': end_date,
            'data': optimized_dictionary,
            'totalDeaths': total_deaths,
            'totalInjuries': total_injuries
        }
        return response_body


def _build_api_entry(entry, entry_type):
    return {
        json_fields.NUMBER: _get_number(entry, entry_type),
        json_fields.LATITUDE: entry[db_constants.LATITUDE],
        json_fields.LONGITUDE: entry[db_constants.LONGITUDE],
        json_fields.TYPE: entry_type,
        json_fields.DATE: entry[db_constants.DATE]
    }


def _format_datetime(datetime_input):
    return int(datetime_input.strftime("%y%m%d"))


def _build_optimized_api_entry(entry, entry_type):
    return {
        json_fields.NUMBER: _get_number(entry, entry_type),
        json_fields.LATITUDE: entry[db_constants.LATITUDE],
        json_fields.LONGITUDE: entry[db_constants.LONGITUDE],
        json_fields.TYPE: entry_type,
        json_fields.ID: _get_id(entry, entry_type)
    }


# TODO: Find out if this is how we plan on using data in the long term
# TODO: If it is then we should be storing our data this way in the first place
def _get_number(entry, entry_type):
    if entry_type == json_fields.KILLED:
        return entry[db_constants.KILLED]
    else:
        return entry[db_constants.INJURED]


def _get_id(entry, entry_type):
    if entry_type == json_fields.KILLED:
        return str(entry[db_constants.ID]) + '0'
    else:
        return str(entry[db_constants.ID]) + '1'
