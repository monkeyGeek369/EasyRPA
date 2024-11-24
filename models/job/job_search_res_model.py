from dataclasses import dataclass
from easyrpa.models.base.response_page_base_model import ResponsePageBaseModel
from models.job.job_detail_model import JobDetailModel


@dataclass
class JobSearchResModel(ResponsePageBaseModel):
    data:list[JobDetailModel]