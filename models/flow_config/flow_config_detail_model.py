from dataclasses import dataclass
from easyrpa.models.base.response_do_base_model import ResponseDoBaseModel


@dataclass
class FlowConfigDetailModel(ResponseDoBaseModel):
    id:int
    flow_id:int
    flow_code:str
    flow_name:str
    config_name:str
    config_description:str
    config_json:str