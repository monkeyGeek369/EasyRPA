from dataclasses import dataclass
from easyrpa.models.base.request_page_base_model import RequestPageBaseModel

@dataclass
class RobotLogSearchReqModel(RequestPageBaseModel):
    robot_id:int
    task_id:int
    log_type:int