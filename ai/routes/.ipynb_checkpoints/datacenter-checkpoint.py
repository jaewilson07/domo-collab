import domolibrary.client.DomoError as dmde
import routes.client as client
import domolibrary.client.ResponseGetData as rgd
import domolibrary.client.DomoAuth as dmda

# Function to POST a query to the search API
def search_datacenter_sync(
    auth: dmda.DomoAuth,
    query_body: dict,
    debug_api: bool = False,
) -> rgd.ResponseGetData:
    
    # Construct the URL for the search query API
    url = f"https://{auth.domo_instance}.domo.com/api/search/v1/query"
    
    # Send POST request to the API
    res = client.get_data_sync(
        auth=auth,
        url=url,
        method="POST",
        body=query_body,
        debug_api=debug_api
    )
    
    # Check if the request was successful
    if not res.is_success:
        raise dmde.DomoError(res.response)
    
    return res