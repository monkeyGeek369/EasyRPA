from dataclasses import dataclass
from easyrpa.models.base.request_page_base_model import RequestPageBaseModel

@dataclass
class TaskSearchReqModel(RequestPageBaseModel):
    id:int
    site_id:int
    flow_id:int
    biz_no:str
    sub_source:int
    status:int
    result_code:int
    result_message:str
    result_data:str