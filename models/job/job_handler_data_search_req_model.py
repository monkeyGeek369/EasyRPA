from dataclasses import dataclass
from easyrpa.models.base.request_page_base_model import RequestPageBaseModel

@dataclass
class JobHandlerDataSearchReqModel(RequestPageBaseModel):
    id:int
    job_id:int
    data_job_id:int
    data_id:int
    status:int
