import domolibrary.client.ResponseGetData as rgd

import models.messages as msg

def generate_llm_messages() -> msg.Messages:
    return msg.Messages.from_system_prompt('./prompts/dataflows.txt')


def llm_dataflow_process_definition(res: rgd.ResponseGetData) -> dict:
    s =  {"dataflow_id" : res.response['id'],        
            "dataflow_name" :  res.response['name'],
            "dataflow_actions" :  res.response.get('actions')
    }

    description =  res.response.get('description')
    
    if description:
        s.update({"description" : description})
        
    return s

