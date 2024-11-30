from dataclasses import dataclass
from easyrpa.models.base.response_do_base_model import ResponseDoBaseModel

@dataclass
class TaskLogDetailModel(ResponseDoBaseModel):
    id:int
    task_id:int
    log_type:int
    log_type_name:str
    message:str
    screenshot:str
    robot_ip:str