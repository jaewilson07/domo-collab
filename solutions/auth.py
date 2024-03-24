import requests

from solutions.client import DomoAPIRequest_Error, ResponseClass


class AuthError(DomoAPIRequest_Error):
    def __init__(self, function_name, message):
        super().__init__(function_name, message)


def get_session_token(
    domo_instance: str, domo_username: str, domo_password: str, return_raw: bool = False
) -> ResponseClass:
    """use username and password to generate an access token"""

    url = f"https://{domo_instance}.domo.com/api/content/v2/authentication"

    body = {
        "method": "password",
        "emailAddress": domo_username,
        "password": domo_password,
    }

    res = requests.request(method="POST", url=url, json=body)

    # create standardardized response class
    res = ResponseClass.from_request_response(res=res)

    if return_raw:
        return res

    # test for API errrors
    if not res.is_success:
        raise AuthError(get_session_token.__name__, res.response)

    session_token = res.response.get("sessionToken")

    # test for 'logic errors'
    if not session_token:
        raise AuthError(
            get_session_token.__name__, "unable to retrieve a session token"
        )

    return session_token
