import domolibrary.client.ResponseGetData as rgd
import domolibrary.client.DomoAuth as dmda
import requests

from pprint import pprint

def get_data_sync(auth: dmda.DomoTokenAuth,
                  url,
                  method: str,
                  body = None, debug_api: bool = False, headers : dict = None):
    
    headers = headers or {}
    headers.update({ 'x-domo-developer-token' : auth.domo_access_token})
    
    if debug_api: 

        pprint({'headers' : headers, 'method' : method, 'url' : url, 'body' : body})
        
    res = requests.request(
        headers = headers,
        url=url,
        method=method,
        json = body,
    )
    return rgd.ResponseGetData._from_requests_response(res)
    