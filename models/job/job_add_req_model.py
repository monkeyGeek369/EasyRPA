from dataclasses import dataclass

@dataclass
class JobAddReqModel():
    job_name:str
    cron:str
    flow_code:str
    flow_config_id:int
    job_type:int
    parent_job:int
    current_data_id:int
    last_record_id:int