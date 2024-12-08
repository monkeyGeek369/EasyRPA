from dataclasses import dataclass
from easyrpa.models.base.response_page_base_model import ResponsePageBaseModel
from models.robot.robot_detail_model import RobotDetailModel


@dataclass
class RobotSearchResModel(ResponsePageBaseModel):
    data:list[RobotDetailModel]