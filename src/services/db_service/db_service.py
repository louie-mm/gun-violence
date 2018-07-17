from pymongo import MongoClient, TEXT, DESCENDING

from src.services.db_service import db_constants


class DbService(object):

    def __init__(self):
        self.db = _initialize()
        self.attempts_to_add_existing_data = 0

    def add(self, db_entry):
        if self.contains(db_entry):
            self._data_already_exists(db_entry)
        else:
            self._insert(db_entry)

    def update(self, db_filter, db_entry):
        return self.db.shootings.update_one(db_filter, {'$set': db_entry})

    def find(self, query):
        return list(self.db.shootings.find(query))

    def find_between_dates(self, start, end):
        query = {
            db_constants.DATE: {'$gte': start, '$lt': end}
        }
        return list(self.db.shootings.find(query))

    def find_all(self):
        lat_and_long_exist = {
            db_constants.LONGITUDE: {'$ne': None},
            db_constants.LATITUDE: {'$ne': None}
        }
        return list(self.db.shootings.find(lat_and_long_exist).sort(db_constants.DATE, DESCENDING))

    def contains(self, db_entry):
        return self.db.shootings.find_one(db_entry) is not None

    def _insert(self, db_entry):
        return self.db.shootings.insert_one(db_entry)

    def _data_already_exists(self, db_entry):
        self.attempts_to_add_existing_data += 1
        print('Repeated Entry: ' + str(db_entry))


def _initialize():
    client = MongoClient(db_constants.CLIENT_NAME)
    db = client.shootings

    db.shootings.create_index([
       (db_constants.ADDRESS, TEXT),
       (db_constants.CITY, TEXT),
       (db_constants.STATE, TEXT),
       (db_constants.KILLED, TEXT),
       (db_constants.INJURED, TEXT),
       (db_constants.DATE, TEXT)
    ])
    return db

