import requests
from solutions.client import ResponseClass


def get_user_by_id(
    domo_instance,
    user_id: int,
    session_token: str=None,
    access_token:str = None, 
    headers: dict=None,
    return_raw: bool = False,
    debug_api: bool = False,
):
    url = f"https://{domo_instance}.domo.com/api/content/v2/users/{user_id}"

    headers = headers or {}

    if session_token:
        headers.update({"x-domo-authentication": session_token})
        
    if access_token:
        headers.update({"x-domo-developer-token": access_token})

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

    return res
