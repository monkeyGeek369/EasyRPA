from dataclasses import dataclass

@dataclass
class FlowConfigAddReqModel():
    flow_id:int
    config_name:str
    config_description:str
    config_json:str