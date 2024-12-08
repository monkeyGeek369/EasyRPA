from dataclasses import dataclass
from easyrpa.models.base.response_do_base_model import ResponseDoBaseModel


@dataclass
class RobotDetailModel(ResponseDoBaseModel):
    id:int
    robot_code:str
    robot_ip:str
    status:int
    status_name:str
    port:int
    current_task_id:int