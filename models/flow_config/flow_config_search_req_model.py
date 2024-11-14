from dataclasses import dataclass
from easyrpa.models.base.request_page_base_model import RequestPageBaseModel

@dataclass
class FlowConfigSearchReqModel(RequestPageBaseModel):
    id:int
    flow_id:str
    config_name:str
    config_description:str
    is_active:bool