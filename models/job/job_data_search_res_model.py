from dataclasses import dataclass
from easyrpa.models.base.response_page_base_model import ResponsePageBaseModel
from models.job.job_data_detail_model import JobDataDetailModel


@dataclass
class JobDataSearchResModel(ResponsePageBaseModel):
    data:list[JobDataDetailModel]