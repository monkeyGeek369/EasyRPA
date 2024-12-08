from dataclasses import dataclass
from easyrpa.models.base.response_page_base_model import ResponsePageBaseModel
from models.robot.robot_log_detail_model import RobotLogDetailModel


@dataclass
class RobotLogSearchResModel(ResponsePageBaseModel):
    data:list[RobotLogDetailModel]