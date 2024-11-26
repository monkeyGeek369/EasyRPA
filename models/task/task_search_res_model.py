from dataclasses import dataclass
from easyrpa.models.base.response_page_base_model import ResponsePageBaseModel
from models.task.task_detail_model import TaskDetailModel


@dataclass
class TaskSearchResModel(ResponsePageBaseModel):
    data:list[TaskDetailModel]