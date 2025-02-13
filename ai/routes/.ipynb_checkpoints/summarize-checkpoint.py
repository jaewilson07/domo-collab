
import domolibrary.client.DomoAuth  as dmda
import domolibrary.client.DomoError as dmde
import routes.client as client


def generate_summarize_body(text_input : str, 
                            summary_length: int = 100, 
                            output_style :str = "BULLETED",
                            system_prompt : str = "You are a helpful assistant that writes concise summaries",
                            model = "domo.domo_ai.domogpt-summarize-v1:anthropic"
) :
    text_input = text_input if isinstance(text_input, str) else json.dumps(text_input)
    
    return {"input":text_input,
            "system":system_prompt,
            "promptTemplate":{
            "template": system_prompt or f"Write a {summary_length} summary of the following text {output_style}. ```{text_input}``` CONCISE SUMMARY:",
                #"template":f"rewrite the following text ```{text_input}```s as a {output_style} {summary_length} ",
            },
            "model":model,
            "outputStyle": output_style,
            "outputWordLength":{"max": summary_length }
           }

from enum import Enum

class OutputStyleEnum(Enum):
    BULLETED = "BULLETED"
    NUMBERED ="Numbered"
    PARAGRAPH = "PARAGRAPH"

    
def summarize_route_sync(
    text_input : str,
    auth: dmda.DomoAuth, 
    system_prompt: str = None,
    summary_length : int = 100,
    output_style: OutputStyleEnum = OutputStyleEnum.BULLETED,
    summary_body : dict = None,
    debug_api : bool = False, 
    return_raw: bool  =False, 
):
    output_style = output_style.value if isinstance(output_style, OutputStyleEnum) else output_style
    
    url = f'https://{auth.domo_instance}.domo.com/api/ai/v1/text/summarize'
    
    body = summary_body or generate_summarize_body(text_input = text_input,
                                                   system_prompt=system_prompt,
                                                   output_style = output_style, 
                                                   summary_length = summary_length)
        
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
    
    res.response['ouptput'] = res.response['choices'][0]['output']

    return res

