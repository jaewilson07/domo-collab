import domolibrary.client.ResponseGetData as rgd

import models.messages as msg

def llm_dataflow_process_definition(res: rgd.ResponseGetData) -> dict:
    return {"dataflow_id" : res.response['id'],
            "dataflow_name" :  res.response['name'],
            "datafow_actions" :  res.response['actions']
           }

def generate_llm_messages() -> msg.Messages:
    return msg.Messages.from_system_prompt('./prompts/dataflows.txt')