from dataclasses import dataclass

@dataclass
class FlowConfigUpdateReqModel():
    id:int
    flow_id:int
    config_name:str
    config_description:str
    config_json:str
    is_active:bool