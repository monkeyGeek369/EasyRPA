from dataclasses import dataclass
from easyrpa.models.base.response_page_base_model import ResponsePageBaseModel
from models.task_log.task_log_detail_model import TaskLogDetailModel


@dataclass
class TaskLogSearchResModel(ResponsePageBaseModel):
    data:list[TaskLogDetailModel]