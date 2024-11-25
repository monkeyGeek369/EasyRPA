from dataclasses import dataclass
from easyrpa.models.base.response_do_base_model import ResponseDoBaseModel

@dataclass
class JobDataDetailModel(ResponseDoBaseModel):
    id:int
    job_id:int
    job_name:str
    data_business_no:str
    data_json:str

