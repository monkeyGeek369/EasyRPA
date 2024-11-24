from dataclasses import dataclass
from easyrpa.models.base.response_do_base_model import ResponseDoBaseModel


@dataclass
class JobDetailModel(ResponseDoBaseModel):
    id:int
    job_name:str
    cron:str
    flow_code:str
    flow_name:str
    flow_config_id:int
    flow_config_name:str
    job_type:int
    job_type_name:str
    parent_job:int
    parent_job_name:str
    current_data_id:int
    last_record_id:int