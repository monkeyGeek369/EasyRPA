from dataclasses import dataclass
from easyrpa.models.base.request_page_base_model import RequestPageBaseModel

@dataclass
class JobSearchReqModel(RequestPageBaseModel):
    id:int
    job_name:str
    flow_code:str
    flow_config_id:int
    job_type:int
    parent_job:int
    is_active:bool