from dataclasses import dataclass
from easyrpa.models.base.response_page_base_model import ResponsePageBaseModel
from models.job.job_record_detail_model import JobRecordDetailModel


@dataclass
class JobRecordSearchResModel(ResponsePageBaseModel):
    data:list[JobRecordDetailModel]