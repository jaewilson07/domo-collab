import codeengine
import json
import requests
import inspect
from typing import List


def get_account(auth_name: str) -> dict:
    return codeengine.get_account(auth_name)


class CodeEngine_RequestError(Exception):
    def __init__(self, message = None, res=None, url=None):
        function_name = inspect.stack()[1][3]
        message = (
            message or f"{function_name} : {res['status']} - {res['response']} - {url}"
        )

        super().__init__(message)


def get_full_auth_session_token(
    username: str, password: str, domo_instance: str
) -> str:

    url = "/api/content/v2/authentication"

    payload = {
        "method": "password",
        "emailAddress": username,
        "password": password.strip(),
    }

    res = get_data(
        url=url,
        method="post",
        domo_instance=domo_instance,
        body=payload,
        debug_api=False,
    )

    data = res["response"]

    if not data.get("success") or not data.get("sessionToken"):

        raise CodeEngine_RequestError(
            "get_full_auth_session_token: no session token returned"
        )

    return data.get("sessionToken")


def generate_auth_header(auth_name: str, domo_instance: str) -> dict:

    account = get_account(auth_name)

    creds = None
    access_token = None
    session_token = None

    if (
        account["dataProviderType"] == "abstract-credential-store"
        and account["credentialsType"] == "fields"
    ):
        creds = json.loads(account["properties"]["credentials"])

    if account["dataProviderType"] == "domo-access-token":
        creds = account["properties"]

    if not creds:
        raise CodeEngine_RequestError(
            f"account {auth_name} is not of type 'abstract-credential-store' or domo-access'token'"
        )

    username = creds.get("username", creds.get("DOMO_USERNAME"))
    password = creds.get("password", creds.get("DOMO_PASSWORD"))
    access_token = creds.get("domoAccessToken", creds.get("DOMO_ACCESS_TOKEN"))
    access_token = access_token and access_token.strip()

    if (not username or not password) and not access_token:
        raise CodeEngine_RequestError(
            f"credentials stored in an invalid combination in {auth_name}.  Creds must either be stored as username or DOMO_USERNAME and password or DOMO_PASSWORD or store accessToken or DOMO_ACCESS_TOKEN"
        )

    if username and password:
        session_token = get_full_auth_session_token(
            username=username,
            password=password,
            domo_instance=domo_instance,
        )

    if session_token:
        return {"x-domo-authentication": session_token}

    if access_token:
        return {"x-domo-developer-token": access_token}

    raise CodeEngine_RequestError("no token returned")


def get_data(
    url: str,
    method: str,
    domo_instance: str = None,
    auth_name: str = None,
    params: dict = None,
    headers: dict = None,
    body: dict = None,
    debug_api: bool = False,
) -> dict:

    domo_instance = (
        None if domo_instance == "" else domo_instance.replace(".domo.com", "")
    )
    auth_name = None if auth_name == "" else auth_name

    headers = headers or {}
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        **headers,
    }

    if domo_instance:
        url = f"https://{domo_instance}.domo.com/{url[1:]}"

    if domo_instance and auth_name:
        auth_header = generate_auth_header(
            auth_name=auth_name, domo_instance=domo_instance
        )
        headers = {**headers, **auth_header}

    if debug_api:
        print({"url": url, "method": method, "headers": headers, "body": body})

    if auth_name or domo_instance:
        try:
            res = requests.request(
                method=method.lower(),
                url=url,
                json=body,
                headers=headers,
                params=params,
                timeout=30,
            )
            try:
              data = res.json()
            except:
              data = res.text
              
            if not res.ok:
                return {
                    "response": data['message'],
                    "is_success": res.ok,
                    "status": res.status_code,
                }

            return {
                "response": data,
                "is_success": res.ok,
                "status": res.status_code,
            }

        except requests.exceptions.HTTPError as e:
            print("*** Error occurred")
            print(str(e))
            return str(e)
          
    if params:
      if "?" not in url: 
        url +='?'
      else:
        url +='&'
      for i, (k, v) in enumerate(params.items()):
        url+=str(k)+'='+str(v)+'&'
      url = url[:-1]
      params = None

    return {
        "is_success": True,
        "response": codeengine.send_request(method, url, body, headers, params),
        "status": 200,
    }


def who_am_i(domo_instance: str = None, auth_name: str = None, debug_api: bool = False):
    res = get_data(
        url="/api/content/v2/users/me",
        method="get",
        domo_instance=domo_instance,
        auth_name=auth_name,
        debug_api=debug_api,
    )

    return res["response"]


def get_accounts(
    auth_name: str, domo_instance: str, debug_api: bool = False
) -> List[dict]:
    """retrieve a list of all the accounts the user has read access to.  Note users with "Manage all accounts" will retrieve all account objects"""

    url = "/api/data/v1/accounts"

    res = get_data(
        auth_name=auth_name,
        domo_instance=domo_instance,
        url=url,
        method="GET",
        debug_api=debug_api,
    )

    return res["response"]


def get_account_from_id(
    auth_name: str,
    domo_instance: str,
    account_id: int,
    debug_api: bool = False,
):
    """retrieves metadata about an account"""

    url = f"/api/data/v1/accounts/{account_id}?unmask=true"

    res = get_data(
        auth_name=auth_name,
        domo_instance=domo_instance,
        url=url,
        method="GET",
        debug_api=debug_api,
    )

    if not res["is_success"]:
        raise CodeEngine_RequestError(res = res, url = url)

    return res["response"]

def call_function(
    auth_name: str, domo_instance: str, function_name:str, package_id: str, version: str, input_variables, get_logs: bool = True, debug_api: bool = False
) -> List[dict]:
    """Call function on another instance using SUDO
"""
  
    url = f"/api/codeengine/v2/packages/{package_id}/versions/{version}/functions/{function_name}"
    
    input_params =  {"inputVariables":input_variables,"settings":{"getLogs":get_logs}}
    res = get_data(
        auth_name=auth_name,
        domo_instance=domo_instance,
        body = input_params,
        url=url,
        method="post",
        debug_api=debug_api,
    )

    return res["response"]
  
def get_groups_membership (auth_name: str, domo_instance: str, debug_api: bool = False
) -> List[dict]:
    """retrieves groups which owned by auth_name"""
    user = who_am_i (auth_name = auth_name,
                    domo_instance=domo_instance,
                    debug_api=debug_api)

    owner_id = str (user["id"])
    url = f"/api/content/v2/groups/grouplist?ascending=true&includeDeleted=false&includeSupport=false&limit=100&members={owner_id}&offset=0&sort=name"

    res = get_data(
        auth_name=auth_name,
        domo_instance=domo_instance,
        url=url,
        method="GET",
        debug_api=debug_api,
    )

    if not res["is_success"]:
        raise CodeEngine_RequestError(res = res, url = url)

    return res["response"]

def get_groups_membership_v2 (auth_name: str, domo_instance: str, debug_api: bool = False,
                              debug_loop : bool = False, return_raw: bool = False
) -> List[dict]:
    """retrieves groups which owned by auth_name"""
    user = who_am_i (auth_name = auth_name,
                    domo_instance=domo_instance,
                    debug_api=debug_api)

    owner_id = str (user["id"])
  
    def arr_fn(res) :
      
      try:
        return res["response"]
      except:
        print ('ERROR')
        return []

    offset_params = { "offset": "offset", "limit": "limit",}
    url = f"/api/content/v2/groups/grouplist?ascending=true&includeDeleted=false&includeSupport=false&members={owner_id}&sort=name"
    res = looper(
        auth_name = auth_name,
        domo_instance = domo_instance,
        method="get",
        url = url,
        debug_api = debug_api,
        arr_fn=arr_fn,
        offset_params_is_header=True,
        offset_params=offset_params,
        debug_loop=debug_loop,
        return_raw = return_raw
    )

    return res

def get_group_where_owner (auth_name: str, domo_instance: str, debug_api: bool = False
) -> List[dict]:
    """retrieves groups which owned by auth_name"""
    user = who_am_i (auth_name = auth_name,
                    domo_instance=domo_instance,
                    debug_api=debug_api)

    owner_id = str (user["id"])
    url = f"/api/content/v2/groups/grouplist?ascending=true&includeFullMembership=false&limit=100&offset=0&owner={owner_id}&ownerType=USER&sort=name"
    
    print (url)
    res = get_data(
        auth_name=auth_name,
        domo_instance=domo_instance,
        url=url,
        method="GET",
        debug_api=debug_api,
    )

    if not res["is_success"]:
        raise CodeEngine_RequestError(res = res, url = url)

    return res["response"]

def get_group_where_owner_v2 (auth_name: str, domo_instance: str, debug_api: bool = False,
                              debug_loop : bool = False, return_raw: bool = False
) -> List[dict]:
    """retrieves groups which owned by auth_name"""
    user = who_am_i (auth_name = auth_name,
                    domo_instance=domo_instance,
                    debug_api=debug_api)

    owner_id = str (user["id"])
  
    def arr_fn(res) :
        try:
          return res["response"]
        except:
          print ('ERROR')
          return []

    offset_params = { "offset": "offset", "limit": "limit",}
    url = f"/api/content/v2/groups/grouplist?ascending=true&includeFullMembership=false&owner={owner_id}&ownerType=USER&sort=name"
    res = looper(
        auth_name = auth_name,
        domo_instance = domo_instance,
        method="get",
        url = url,
        debug_api = debug_api,
        arr_fn=arr_fn,
        offset_params_is_header=True,
        offset_params=offset_params,
        debug_loop=debug_loop,
        return_raw = return_raw
    )

    return res


    
  

def list_pages(
    domo_instance: str = None, auth_name: str = None, debug_api: bool = False
):
    body = {"ascending": True, "orderBy": "pageTitle"}

    url = "/api/content/v1/pages/adminsummary?limit=100&skip=0"

    res = get_data(
        method="post",
        url=url,
        body=body,
        domo_instance=domo_instance,
        auth_name=auth_name,
        debug_api=debug_api,
    )

    if not res["is_success"]:
        raise CodeEngine_RequestError(res=res, url=url)

    return res["response"]

def list_pages_v2(
    domo_instance: str = None, auth_name: str = None, debug_api: bool = False,
  debug_loop : bool = False, return_raw: bool = False
):
    body = {"ascending": True, "orderBy": "pageTitle"}
    
    def arr_fn(res) :
        try:
          return res["response"]["pageAdminSummaries"]
        except:
          print ('ERROR')
          return []

    offset_params = { "offset": "skip", "limit": "limit",}
    url = "/api/content/v1/pages/adminsummary"
    res = looper(
        auth_name = auth_name,
        domo_instance = domo_instance,
        method="post",
        url = url,
        body = body,
        debug_api = debug_api,
        arr_fn=arr_fn,
        offset_params_is_header=True,
        offset_params=offset_params,
        debug_loop=debug_loop,
        return_raw = return_raw
    )

    return res

def search_beastmodes(auth_name :str, 
                      domo_instance: str,
                      filters = None,  debug_api: bool = False,
                      debug_loop : bool = False,  
                      return_raw: bool = False
                      ):
    
    offset_params = { "offset": "offset", "limit": "limit",}
                        
    url = f"/api/query/v1/functions/search"

    body = {}   # generate_beastmode_body(filters)

    def arr_fn(res) :
        return res['response']

    # res= {'is_success' : True}

    res = looper(
        auth_name = auth_name,
        domo_instance = domo_instance,
        method="POST",
        url = url,
        body = body,
        debug_api = debug_api,
        
        arr_fn=arr_fn,
        offset_params_is_header=False,
        offset_params=offset_params,
        debug_loop=debug_loop,
        return_raw = return_raw,
        # loop_until_end=True, not implemented
    )
                        
                        
    # if not res['is_success'] :
    #   raise Exception('fail')
      
    return res

def list_groups(
    domo_instance: str = None, auth_name: str = None, debug_api: bool = False
):

    url = "/api/content/v2/groups"

    res = get_data(
        method="GET",
        url=url,
        domo_instance=domo_instance,
        auth_name=auth_name,
        debug_api=debug_api,
    )

    if not res["is_success"]:
        raise CodeEngine_RequestError(res=res, url=url)

    return res["response"]

def get_pages_where_owner (auth_name: str, domo_instance: str, debug_api: bool = False
):
    user = who_am_i (auth_name = auth_name,
                    domo_instance=domo_instance,
                    debug_api=debug_api)
    
    pages_ls = list_pages (auth_name = auth_name,
                    domo_instance=domo_instance,
                    debug_api=debug_api)

    groups_ls = get_groups_membership(auth_name = auth_name,
                    domo_instance=domo_instance,
                    debug_api=debug_api)
    
    page_res = []
    for page in pages_ls["pageAdminSummaries"]:
      for owner in page["owners"]:
        if owner["type"]== 'USER' and str(owner["id"]) == str (user["id"]):
          page_res.append(page)
          break;
        if owner["type"]== 'GROUP' and next((True for g in groups_ls if g["groupId"]==owner["id"]), False):
          page_res.append(page)
          break;
    return page_res


def get_pages_where_owner_v2 (auth_name: str, domo_instance: str, debug_api: bool = False
):
    user = who_am_i (auth_name = auth_name,
                    domo_instance=domo_instance,
                    debug_api=debug_api)
    
    pages_ls = list_pages_v2 (auth_name = auth_name,
                    domo_instance=domo_instance,
                    debug_api=debug_api)

    groups_ls = get_groups_membership_v2 (auth_name = auth_name,
                    domo_instance=domo_instance,
                    debug_api=debug_api)
    
    page_res = []
    for page in pages_ls["response"]:
      for owner in page["owners"]:
        if owner["type"]== 'USER' and str(owner["id"]) == str (user["id"]):
          page_res.append(page)
          break;
        if owner["type"]== 'GROUP' and next((True for g in groups_ls["response"] if g["groupId"]==owner["id"]), False):
          page_res.append(page)
          break;
    return page_res

def list_appstudio(
    domo_instance: str = None, auth_name: str = None, debug_api: bool = False
):

    url = "/api/content/v1/dataapps"

    res = get_data(
        method="GET",
        url=url,
        domo_instance=domo_instance,
        auth_name=auth_name,
        debug_api=debug_api,
    )

    if not res["is_success"]:
        raise CodeEngine_RequestError(res=res, url=url)

    return res["response"]

def get_appstudio_where_owner (auth_name: str, domo_instance: str, debug_api: bool = False
):
    user = who_am_i (auth_name = auth_name,
                    domo_instance=domo_instance,
                    debug_api=debug_api)
    
    appstudio_ls = list_appstudio (auth_name = auth_name,
                    domo_instance=domo_instance,
                    debug_api=debug_api)

    groups_ls = get_groups_membership(auth_name = auth_name,
                    domo_instance=domo_instance,
                    debug_api=debug_api)
    
    appstudio_res = []
    for page in appstudio_ls:
      for owner in page["owners"]:
        if owner["type"]== 'USER' and str(owner["id"]) == str (user["id"]):
          appstudio_res.append(page)
          break;
        if owner["type"]== 'GROUP' and next((True for g in groups_ls if g["groupId"]==owner["id"]), False):
          appstudio_res.append(page)
          break;
    return appstudio_res

def share_appstudio (auth_name: str, domo_instance: str, appstudio_id_ls: [], group_id_ls: [], debug_api: bool = False
):
    url = "/api/content/v1/dataapps/share?sendEmail=false"
    recipients = []
    for id in group_id_ls:
      recipients.append({
            "type": "group",
            "id": id
        })
    body = {
    "dataAppIds": appstudio_id_ls,
    "recipients": recipients,
    "message": ""
    }
    res = get_data(
        method="post",
        url=url,
        body=body,
        domo_instance=domo_instance,
        auth_name=auth_name,
        debug_api=debug_api
    )
    return res

def looper(
    url : str,
    auth_name: str,
    domo_instance: str,
    arr_fn : callable,
    offset_params: dict,
    method="GET",
    offset : int=0,
    limit : int =50,
    params: dict = None,
    body: dict = None,
    offset_params_is_header: bool = False,
    debug_loop: bool = False,
    debug_api: bool = False,
    return_raw: bool = False,  # will break the looper after the first request and ignore the array processing step.
):
    final_array = []
    keep_looping = True
    counter = 1
    while keep_looping:
        counter +=1
        new_params = params.copy() if params else {}
        new_body = body.copy() if body else None
        new_offset = {
            offset_params["offset"]: offset,
            offset_params["limit"]: limit,
        }
        if offset_params_is_header:
            new_params = {**new_params, **new_offset}
        else:
            new_body = {**new_body, **new_offset}
        if debug_loop:
          print(new_offset, new_body)
        res = get_data(
            auth_name=auth_name,
            domo_instance=domo_instance,
            url=url,
            method=method,
            params=new_params,
            debug_api=debug_api,
            body=new_body,
        )
        if not res['is_success'] or return_raw:
            return res
        new_array = arr_fn(res)
        if debug_loop:
            print(new_params, new_body, new_array)
        if not new_array or len(new_array) <= 0 or counter >3:
            keep_looping = False
        final_array += new_array
        offset += limit
    res.update({'response': final_array})
    return res