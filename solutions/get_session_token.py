import requests


def get_session_token(
    domo_instance: str, domo_username: str, domo_password: str, return_raw: bool = False
) -> str:

    url = f"https://{domo_instance}.domo.com/api/content/v2/authentication"

    body = {
        "method": "password",
        "emailAddress": domo_username,
        "password": domo_password,
    }

    res = requests.request(method="POST", url=url, json=body, verify=False)

    data = res.json()

    if return_raw:
        return res

    if not res.ok:
        raise Exception(data["message"])

    token = data.get("sessionToken")

    if not token:
        raise Exception("No token returned from API")

    return token
