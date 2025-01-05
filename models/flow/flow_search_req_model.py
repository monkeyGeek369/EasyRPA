from dataclasses import dataclass
from easyrpa.models.base.request_page_base_model import RequestPageBaseModel

@dataclass
class FlowSearchReqModel(RequestPageBaseModel):
    id:int
    site_id:int
    site_name:str
    flow_code:str
    flow_name:str
    flow_rpa_type:int
    flow_biz_type:int
    retry_code:str
    is_active:bool