import codeengine
import json
import requests


def domo_api_request(
    url, request_type, instance=None, auth=None, params=None, headers=None, body=None
):
    if instance == "":
        instance = None
    if auth == "":
        auth = None
    my_auth = None

    if headers == None:
        headers = {"Accept": "application/json", "Content-Type": "application/json"}

    if instance != None:
        if ".domo.com" not in instance:
            instance = instance + ".domo.com"
        url = "https://" + instance + url

    if instance != None and auth != None:
        my_auth = remote_authentication(account_name=auth, remote_instance=instance)

    if my_auth != None:
        # username/password
        if "sessionToken" in my_auth:
            # we have a session token - use it for auth
            headers["x-domo-authentication"] = my_auth["sessionToken"]
            print("*** new headers : " + str(headers))

        # access token
        elif "accessToken" in my_auth:
            # we have an access token - use it for auth
            headers["x-domo-developer-token"] = my_auth["accessToken"]
            print("*** new headers : " + str(headers))

    try:
        if instance != None:
            if request_type.lower() == "post":
                response = json.loads(
                    requests.post(url, json=body, headers=headers).text
                )
            elif request_type.lower() == "get":
                response = json.loads(
                    requests.get(url, json=body, headers=headers, params=params).text
                )

        else:
            response = codeengine.send_request(request_type, url, body, headers, None)

    except requests.exceptions.HTTPError as e:
        print("*** Error occurred")
        print(str(e))
        return str(e)
    return response


def get_creds(account_name):
    return codeengine.get_account(account_name)


def remote_auth_username_password(creds, remote_instance):

    url = "/api/content/v2/authentication"
    headers = {"Accept": "application/json", "Content-Type": "application/json"}
    payload = {
        "method": "password",
        "emailAddress": creds["username"],
        "password": creds["password"],
    }

    response = domo_api_request(
        url, "post", instance=remote_instance, headers=headers, body=payload
    )
    if response.get("success") == True:
        return {"sessionToken": response.get("sessionToken")}
    return False


def remote_authentication(account_name, remote_instance):
    creds = get_creds(account_name)

    if (
        creds["dataProviderType"] == "abstract-credential-store"
        and creds["credentialsType"] == "fields"
    ):
        credentials = json.loads(creds["properties"]["credentials"])
        if "username" in credentials and "password" in credentials:
            token = remote_auth_username_password(credentials, remote_instance)
        elif "accessToken" in credentials:
            token = credentials
    return token


def list_roles():
    return domo_api_request(url="/api/authorization/v1/roles", request_type="get")


def list_roles_2(instance=None, auth=None):
    return domo_api_request(
        url="/api/authorization/v1/roles",
        request_type="get",
        instance=instance,
        auth=auth,
    )


def list_pages(instance=None, auth=None):
    body = {"ascending": True, "orderBy": "pageTitle"}
    response = domo_api_request(
        url="/api/content/v1/pages/adminsummary?limit=10&skip=0",
        request_type="post",
        instance=instance,
        auth=auth,
        body=body,
    )
    return response


def get_page_by_id(page_id, instance=None, auth=None):

    url = (
        "/api/content/v3/stacks/"
        + page_id
        + "/cards?includeV4PageLayouts=true&parts=metadata,datasources,library,drillPathURNs,certification,owners,dateInfo,subscriptions,slicers"
    )
    response = domo_api_request(
        url=url, request_type="get", instance=instance, auth=auth
    )
    return response


def list_subscription_invites(instance=None, auth=None):
    response = domo_api_request(
        url="/api/publish/v2/subscription/invites",
        request_type="get",
        instance=instance,
        auth=auth,
    )
    return response
