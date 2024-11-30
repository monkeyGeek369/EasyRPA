from dataclasses import dataclass
from easyrpa.models.base.request_page_base_model import RequestPageBaseModel

@dataclass
class TaskLogSearchReqModel(RequestPageBaseModel):
    id:int
    task_id:int