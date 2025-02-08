
from models.model import EndpointHandler as base
import domolibrary.client.DomoAuth as dmda

class EndpointHandler(base):
    auth : dmda.DomoAuth
    
    def __init__(self):
        auth = super()._get_auth('domo-community')
        super().__init__(auth = auth)

