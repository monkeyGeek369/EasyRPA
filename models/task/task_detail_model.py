from dataclasses import dataclass
from easyrpa.models.base.response_do_base_model import ResponseDoBaseModel

@dataclass
class TaskDetailModel(ResponseDoBaseModel):
    id:int
    site_id:int
    site_name:str
    flow_id:int
    flow_code:str
    flow_name:str
    flow_config_id:int
    flow_config_name:str
    biz_no:str
    sub_source:int
    sub_source_name:str
    status:int
    status_name:str
    result_code:int
    result_message:str
    result_data:str
    retry_number:int
    screenshot_base64:str
    request_standard_message:str
    flow_standard_message:str
    task_result_message:str
    flow_result_handle_message:str