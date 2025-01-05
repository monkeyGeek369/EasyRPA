from dataclasses import dataclass
from easyrpa.models.base.response_do_base_model import ResponseDoBaseModel


@dataclass
class FlowDetailModel(ResponseDoBaseModel):
    id:int
    site_id:int
    site_name:str
    flow_code:str
    flow_name:str
    flow_rpa_type:int
    flow_rpa_type_name:str
    flow_biz_type:int
    flow_biz_type_name:str
    max_retry_number:int
    max_exe_time:int
    retry_code:str
    request_check_script:str
    request_adapt_script:str
    flow_exe_script:str
    flow_result_handle_script:str