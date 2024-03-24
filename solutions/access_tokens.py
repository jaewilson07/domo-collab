import requests
from solutions.client import ResponseClass
from solutions.utils import (
    convert_domo_utc_to_datetime,
    generate_domo_expiration_unixtimestamp,
)

from pprint import pprint


def get_all_access_tokens(
    domo_instance,
    session_token=None,
    headers=None,
    return_raw: bool = False,
    debug_api: bool = False,
):

    url = f"https://{domo_instance}.domo.com/api/data/v1/accesstokens"

    headers = headers or {}

    if session_token:
        headers.update({"x-domo-authentication": session_token})

    if debug_api:
        print({"url": url, "headers": headers})

    res = requests.request(
        url=url,
        method="GET",
        headers=headers,
    )

    res = ResponseClass.from_request_response(res)

    if return_raw:
        return res

    [
        token.update({"expires": convert_domo_utc_to_datetime(token["expires"])})
        for token in res.response
    ]

    return res


def generate_access_token(
    domo_instance,
    token_name: str,
    user_id,
    duration_in_days: 15,
    session_token=None,
    headers=None,
    return_raw: bool = False,
    debug_api: bool = False,
):
    url = f"https://{domo_instance}.domo.com/api/data/v1/accesstokens"

    expiration_timestamp = generate_domo_expiration_unixtimestamp(
        duration_in_days=duration_in_days
    )

    body = {"name": token_name, "ownerId": user_id, "expires": expiration_timestamp}

    headers = headers or {}

    if session_token:
        headers.update({"x-domo-authentication": session_token})

    if debug_api:
        pprint({"url": url, "headers": headers, "body": body})

    res = requests.request(method="post", url=url, json=body, headers=headers)

    res = ResponseClass.from_request_response(res)
    if return_raw:
        return res

    return res


def revoke_access_token(
    domo_instance,
    access_token_id,
    session_token=None,
    headers=None,
    return_raw: bool = False,
    debug_api: bool = False,
):

    url = f"https://{domo_instance}.domo.com/api/data/v1/accesstokens/{access_token_id}"

    headers = headers or {}

    if session_token:
        headers.update({"x-domo-authentication": session_token})

    if debug_api:
        pprint({"url": url, "headers": headers})

    res = requests.request(method="DELETE", url=url, headers=headers)

    res = ResponseClass.from_request_response(res)
    if return_raw:
        return res

    res.response = f"access token {access_token_id} deleted"
    return res
