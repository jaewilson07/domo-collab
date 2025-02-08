import domolibrary.client.DomoError as dmde
import routes.client as client
import domolibrary.client.DomoAuth as dmda

def get_dataflow_by_id_sync(
    auth: dmda.DomoAuth,
    dataflow_id: int,
    debug_api: bool = False,
):
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
