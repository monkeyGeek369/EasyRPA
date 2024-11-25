from dataclasses import dataclass
from easyrpa.models.base.request_page_base_model import RequestPageBaseModel

@dataclass
class JobDataSearchReqModel(RequestPageBaseModel):
    id:int
    job_id:int
    data_business_no:str
    data_json:str