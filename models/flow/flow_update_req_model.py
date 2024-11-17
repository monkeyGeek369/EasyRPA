from dataclasses import dataclass

@dataclass
class FlowUpdateReqModel():
    id:int
    site_id:int
    flow_code:str
    flow_name:str
    flow_rpa_type:int
    flow_exe_env:int
    flow_biz_type:int
    max_retry_number:int
    max_exe_time:int
    retry_code:str
    request_check_script:str
    request_adapt_script:str
    flow_exe_script:str
    flow_result_handle_script:str
    is_active:bool