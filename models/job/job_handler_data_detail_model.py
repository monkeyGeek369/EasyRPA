from dataclasses import dataclass
from easyrpa.models.base.response_do_base_model import ResponseDoBaseModel


@dataclass
class JobHandlerDataDetailModel(ResponseDoBaseModel):
    id:int
    job_id:int
    job_name:str    
    data_job_id:int
    data_job_name:str
    data_id:int
    status:int
    status_name:str


