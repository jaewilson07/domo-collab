import domolibrary.client.DomoError as dmde
import routes.client as client
import domolibrary.client.ResponseGetData as rgd
import domolibrary.client.DomoAuth as dmda

from typing import List


def get_dataflow_by_id_sync(
    auth: dmda.DomoAuth,
    dataflow_id: int,
    debug_api: bool = False,
) -> rgd.ResponseGetData:
    url = f"https://{auth.domo_instance}.domo.com/api/dataprocessing/v1/dataflows/{dataflow_id}"     
    
    res= client.get_data_sync(
        auth=auth,
        url=url,
        method="GET",
        debug_api=debug_api
    )     
    
    if not res.is_success:        
        raise dmde.DomoError(res.response)     
    
    return res


# Function to retrieve tags for a dataflow
def get_dataflow_tags_by_id_sync(
    auth: dmda.DomoAuth,
    dataflow_id: int,
    debug_api: bool = False,
) -> rgd.ResponseGetData:
    # Construct the URL for the GET request
    url = f"https://{auth.domo_instance}.domo.com/api/dataprocessing/v1/dataflows/{dataflow_id}/tags"
    
    # Make the GET request
    res = client.get_data_sync(
        auth=auth,
        url=url,
        method="GET",
        debug_api=debug_api
    )
    
    # Check if the request was successful
    if not res.is_success:
        raise dmde.DomoError(res.response)
    
    return res

# Function to generate the request body
def generate_tag_body(dataflow_id, tag_ls) -> dict:
    return {"flowId": dataflow_id, "tags": tag_ls}

# Function to update dataflow tags
def put_dataflow_tags_by_id_sync(
    auth: dmda.DomoAuth,
    dataflow_id: int,
    tag_ls: List[str],
    debug_api: bool = False,
) -> rgd.ResponseGetData:
    
    # Construct the URL
    url = f"https://{auth.domo_instance}.domo.com/api/dataprocessing/v1/dataflows/{dataflow_id}/tags"
    
    # Generate the request body
    body = generate_tag_body(dataflow_id=dataflow_id, tag_ls=tag_ls)
    
    # Make the API call
    res = client.get_data_sync(
        auth=auth,
        url=url,
        method="PUT",
        body=body,
        debug_api=debug_api
    )
    
    # Check for successful response
    if not res.is_success:
        raise dmde.DomoError(res.response)
    
    return res