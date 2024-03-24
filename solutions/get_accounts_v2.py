import requests
from typing import List


def get_accounts(
    domo_instance,
    headers: dict = None,
    session_token: str = None,
    debug_api: bool = False,  # to conditionally print request parameters for debugging
    return_raw: bool = False,  # conditionally return the Response class instead of just the sessionToken
) -> List[dict]:

    headers = headers or {}

    if session_token:
        headers.update({"x-domo-authentication": session_token})

    url = f"https://{domo_instance}.domo.com/api/data/v2/datasources/providers"

    if debug_api:
        print({"headers": headers, "url": url})

    res = requests.request(method="GET", url=url, headers=headers)

    if return_raw:
        return res

    account_ls = res.json()

    return account_ls
