from dataclasses import dataclass
from easyrpa.models.base.response_page_base_model import ResponsePageBaseModel
from models.job.job_handler_data_detail_model import JobHandlerDataDetailModel


@dataclass
class JobHandlerDataSearchResModel(ResponsePageBaseModel):
    data:list[JobHandlerDataDetailModel]