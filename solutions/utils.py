from typing import List, Any

import domojupyter as dj
import json
import re
import datetime as dt
import time

def read_domo_jupyter_account(account_name, is_abstract: bool = False):

    account_properties = dj.get_account_property_keys(account_name)

    creds = {
        prop: dj.get_account_property_value(account_name, prop)
        for prop in account_properties
    }

    if not is_abstract:
        return creds

    return json.loads(
        creds["credentials"]
    )  # converts credentials string into a dictionary


def flatten_list_of_lists(list_of_lists) -> List[Any]:
    return [row for ls in list_of_lists for row in ls]


def format_str_camel_case(text):
    return "_".join(
        re.sub(
            "([A-Z][a-z]+)", r" \1", re.sub("([A-Z]+)", r" \1", text.replace("-", " "))
        ).split()
    ).lower()


def convert_domo_utc_to_datetime(timestamp):
    """Domo returns token expiration date in unix time"""
    return dt.datetime.fromtimestamp(timestamp / 1000, dt.timezone.utc)


def generate_domo_expiration_unixtimestamp(
    duration_in_days: int = 15, debug_prn: bool = False
):
    """the expiration date of the access token is calculated based off of x days into the future which must then be converted into a unix timestamp"""

    today = dt.datetime.today()
    expiration_date = today + dt.timedelta(days=duration_in_days)

    if debug_prn:
        print(f"expiration_date is {duration_in_days} from today {expiration_date}")

    return int(time.mktime(expiration_date.timetuple()) * 1000)
