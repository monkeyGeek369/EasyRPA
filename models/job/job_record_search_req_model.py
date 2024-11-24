from dataclasses import dataclass
from easyrpa.models.base.request_page_base_model import RequestPageBaseModel

@dataclass
class JobRecordSearchReqModel(RequestPageBaseModel):
    id:int
    job_id:int
    flow_task_id:int
    status:int