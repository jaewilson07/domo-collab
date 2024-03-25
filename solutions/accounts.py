import requests
from solutions.client import DomoAPIRequest_Error, ResponseClass

import json
import datetime as dt

from pprint import pprint


class Account_Error(DomoAPIRequest_Error):
    def __init__(self, function_name, message):
        super().__init__(function_name, message)


def get_accounts(
    domo_instance,
    headers: dict = None,
    session_token: str = None,
    access_token : str = None,
    debug_api: bool = False,
    return_raw: bool = False,
) -> ResponseClass:

    url = f"https://{domo_instance}.domo.com/api/data/v2/datasources/providers"
    
    headers = headers or {}

    if session_token:
        headers.update({"x-domo-authentication": session_token})
        
    if access_token:
        headers.update({"x-domo-developer-token": access_token})

    if debug_api:
        print({"url": url, "headers": headers})

    res = requests.request(method="GET", url=url, headers=headers)

    # create standardardized response class
    res = ResponseClass.from_request_response(res=res)

    if return_raw:
        return res

    # test for API errrors
    if not res.is_success:
        raise Account_Error(get_accounts.__name__, res.response)

    # test for 'logic errors'
    if len(res.response) == 0:
        raise Account_Error(
            get_accounts.__name__,
            "no accounts returned, does this user have access to accounts Domo > Data > Accounts",
        )

    return res

def get_account_by_id(
    domo_instance,
    account_id,
    headers : dict=None,
    session_token : str =None,
    access_token: str = None,
    return_raw: bool = False,
    debug_api: bool = False,
):
    url = f"https://{domo_instance}.domo.com/api/data/v1/accounts/{account_id}?unmask=true"

    headers = headers or {}

    if session_token:
        headers.update({"x-domo-authentication": session_token})
        
    if access_token:
        headers.update({"x-domo-developer-token": access_token})

    if debug_api:
        print({"url": url, "headers": headers})

    res = requests.request(method="GET", url=url, headers=headers)

    res = ResponseClass.from_request_response(res)

    if return_raw:
        return res

    return res


def generate_account__abstract_credential_store_body(
    account_name, credentials, is_timestamp: bool = True
):

    # the API expects credentials to be type string, so conditionally convert dict to string
    if isinstance(credentials, dict):
        credentials = json.dumps(credentials)

    if is_timestamp:
        account_name = f"{account_name} - updated {dt.date.today()}"
    return {
        "name": "Abstract Credential Store Account",
        "displayName": account_name,
        "dataProviderType": "abstract-credential-store",
        "configurations": {"credentials": credentials},
    }


def generate_account__access_token_body(
    account_name, access_token=None, username=None, password=None
):
    return {
        "name": "Domo Access Token Account",
        "displayName": account_name,
        "dataProviderType": "domo-access-token",
        "configurations": {
            "domoAccessToken": {access_token},
            "username": {username},
            "password": {password},
        },
    }


def create_account(body, 
                   domo_instance, 
                   headers = None,
                   session_token = None,
                   access_token = None,
                   debug_api: bool = False):
    url = f"https://{domo_instance}.domo.com/api/data/v1/accounts"

    headers = headers or {}

    if session_token:
        headers.update({"x-domo-authentication": session_token})
        
    if access_token:
        headers.update({"x-domo-developer-token": access_token})

    if debug_api:
        print({"url": url, "headers": headers, "body": body})

    res = requests.request(method="POST", url=url, json=body, headers=headers)

    res = ResponseClass.from_request_response(res)

    if not res.is_success:
        raise DomoAPIRequest_Error(create_account.__name__, res)

    return res


def update_account_name(
    domo_instance: str,
    account_id: int,
    account_name: str,
    session_token=None,
    access_token = None,
    headers: dict = None,
    debug_api: bool = False,
    return_raw: bool = False,
):
    url = f"https://{domo_instance}.domo.com/api/data/v1/accounts/{account_id}/name"

    headers = headers or {}

    if session_token:
        headers.update({"x-domo-authentication": session_token})
        
    if access_token:
        headers.update({"x-domo-developer-token": access_token})

    if debug_api:
        pprint({"url": url, "headers": headers, "body": account_name})

    res = requests.request(method="PUT", data=account_name, url=url, headers=headers)

    res = ResponseClass.from_request_response(res)

    if return_raw:
        return res

    return res


def update_account_config(
    domo_instance,
    dataprovider_type,
    account_id,
    body: dict,  # only receives configuration portion of the account definition
    headers: dict = None,
    session_token: str = None,
    access_token : str = None,
    debug_api: bool = False,
    return_raw: bool = False,
):
    url = f"https://{domo_instance}.domo.com/api/data/v1/providers/{dataprovider_type}/account/{account_id}"

    headers = headers or {}

    if session_token:
        headers.update({"x-domo-authentication": session_token})
        
    if access_token:
        headers.update({"x-domo-developer-token": access_token})

    if debug_api:
        pprint({"url": url, "headers": headers, "body": body})

    res = requests.request(method="PUT", json=body, url=url, headers=headers)

    res = ResponseClass.from_request_response(res)

    if return_raw:
        return res

    return res
