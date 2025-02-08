import domojupyter as dj
import domolibrary_execution.utils.domojupyter as dxdj

import domolibrary.client.DomoAuth as dmda
import domolibrary.client.ResponseGetData as rgd

from models.messages import Message , Messages 
import models.dataflow_model as dfm

import routes.chat as chat_routes
import routes.dataflow as dataflow_routes

import json


class EndpointHandler:
    auth: dmda.DomoFullAuth

    def __init__(self, auth: dmda.DomoAuth):
        self.auth = auth
    
    @staticmethod
    def _get_auth(domo_instance):
        account_name = f"sdk_{domo_instance}"

        account_properties = dj.get_account_property_keys(
            account_name
        )

        creds = {
            prop: dj.get_account_property_value(
                account_name, prop
            )
            for prop in account_properties
        }

        return dmda.DomoTokenAuth(
            # domo_username = creds['username'],
            # domo_password=  creds['password'],
            domo_access_token=creds["domoAccessToken"],
            domo_instance= dxdj.which_environment(),
        )
    
    @classmethod
    def _from_creds_account(cls, domo_instance):
        auth = cls._get_auth(domo_instance)
        
        return cls(auth = auth)
    
    def invoke(
        self,
        data: str = None,
        return_raw: bool = False,
        debug_api: bool = False,
        messages: Messages = None,
        **kwargs,
    ) -> dict:
        
        messages = messages or Messages([])

        data = messages.generate_context(text_input= data)

        res = chat_routes.chat_route_sync(
            auth=self.auth, return_raw=return_raw, debug_api=debug_api, prompt=data
        )
        
        messages.messages.append(Message("SYSTEM", res.response["output"]))

        return json.dumps(res.response)


    def invoke_message(
        self,
        data: str = None,
        return_raw: bool = False,
        debug_api: bool = False,
        messages: Messages = None,
        **kwargs,
    ) -> Messages:
        messages = messages or Messages([])

        data = messages.generate_context(text_input= data)

        res = chat_routes.chat_route_sync(
            auth=self.auth, return_raw=return_raw, debug_api=debug_api, prompt=data
        )

        if return_raw: 
            return res

        messages.messages.append(Message("SYSTEM", res.response["output"]))

        return messages
    

    
    def llm_describe_dataflow(self,
                              dataflow_id,
                              messages : Messages = None, 
                              debug_api : bool = False, 
                              return_raw : bool = False):
        
        res = dataflow_routes.get_dataflow_by_id_sync(
            auth = self.auth,
            dataflow_id = dataflow_id,
            debug_api = debug_api
        )
        
        data = dfm.llm_dataflow_process_definition(res)
        
        messages = dfm.generate_llm_messages()
        
        messages.add_message(f"""
        describe the following JSON transformation steps in plain english: {data}.
        Limit your response to 300 words""")
        
        res=  self.invoke_message(
            messages = messages,
            debug_api = debug_api,
            return_raw = return_raw
        )
        
        if return_raw:
            return res
        
        return messages        
        