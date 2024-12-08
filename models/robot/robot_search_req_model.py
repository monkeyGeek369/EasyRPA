from dataclasses import dataclass
from easyrpa.models.base.request_page_base_model import RequestPageBaseModel

@dataclass
class RobotSearchReqModel(RequestPageBaseModel):
    robot_code:str
    robot_ip:str
    status:int
    current_task_id:int