import re

from src.services.address_util.address_exception import AddressException


def build_full_address(state, city, street_address=None):
    if street_address is None:
        if _is_valid_city(city) and _is_valid_state(state):
            return "{}, {}, USA".format(city, state)
    else:
        if _is_valid_city(city) and _is_valid_state(state) and _is_valid_street_address(street_address):
            return "{}, {}, {}, USA".format(street_address, city, state)
    raise AddressException(_address_exception_message.format(str(street_address), str(city), str(state)))


def is_valid_address(state, city, street_address=None):
    if street_address is None:
        return _is_valid_city(city) and _is_valid_state(state)
    else:
        return _is_valid_city(city) and _is_valid_state(state) and _is_valid_street_address(street_address)


def _is_valid_city(city):
    return city != "N/A" \
           and city is not None \
           and city != "" \
           and re.search('[a-zA-Z]+', str(city)) is not None


def _is_valid_state(state):
    return str(state).lower() in _all_states


def _is_valid_street_address(street_address):
    return street_address != "N/A" \
           and street_address is not None \
           and street_address != "" \
           and re.search('[a-zA-Z]+', str(street_address)) is not None


_all_states = ['alabama', 'alaska', 'arizona', 'arkansas', 'california', 'colorado', 'connecticut', 'delaware',
              'florida', 'georgia', 'hawaii', 'idaho', 'illinois', 'indiana', 'iowa', 'kansas', 'kentucky', 'louisiana',
              'maine', 'maryland', 'massachusetts', 'michigan', 'minnesota', 'mississippi', 'missouri', 'montana',
              'nebraska', 'nevada', 'new hampshire', 'new jersey', 'new mexico', 'new york', 'north carolina',
              'north dakota', 'ohio', 'oklahoma', 'oregon', 'pennsylvania', 'rhode island', 'south carolina',
              'south dakota', 'tennessee', 'texas', 'utah', 'vermont', 'virginia', 'washington', 'west virginia',
              'wisconsin', 'wyoming',
              "al", "ak", "az", "ar", "ca", "co", "ct", "dc", "de", "fl", "ga", "hi", "id", "il", "in", "ia", "ks",
              "ky", "la", "me", "md", "ma", "mi", "mn", "ms", "mo", "mt", "ne", "nv", "nh", "nj", "nm", "ny", "nc",
              "nd", "oh", "ok", "or", "pa", "ri", "sc", "sd", "tn", "tx", "ut", "vt", "va", "wa", "wv", "wi", "wy"]

_address_exception_message = "Attempt to build an invalid address: {}, {}, {}"
