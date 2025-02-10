import domolibrary.client.DomoAuth  as dmda
import domolibrary.client.DomoError as dmde
import routes.client as client




def generate_chat_body(text_input : str, 
                       model = "domo.domo_ai.domogpt-chat-medium-v1.1:anthropic"
):

    return {"input":text_input,
            "promptTemplate":{"template":"${input}"},
            "model":model}

def chat_route_sync(text_input,
                    auth: dmda.DomoAuth, 
                    chat_body : dict = None,
                    debug_api : bool = False, 
                    parent_class : str = None,
                    debug_num_stacks_to_drop = 1, 
                    return_raw: bool  =False, 
                    ):
    
    url = f'https://{auth.domo_instance}.domo.com/api/ai/v1/text/generation'
    
    body = chat_body or generate_chat_body(text_input = text_input)
        
    res = client.get_data_sync(
        auth = auth, 
        url = url, 
        method = 'POST',
        body = body,
        debug_api = debug_api,  
    )
    
    if return_raw:
        return res
    
    if not res.is_success:
        raise dmde.DomoError(message = res.response )
    
    res.response['output'] = res.response['choices'][0]['output']

    return res



