from dataclasses import dataclass
from easyrpa.models.base.response_do_base_model import ResponseDoBaseModel


@dataclass
class JobRecordDetailModel(ResponseDoBaseModel):
    id:int
    job_id:int
    job_name:str    
    flow_code:str
    flow_name:str
    flow_task_id:int
    status:int
    status_name:str
    result_message:str

