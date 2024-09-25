from easyrpa.models.easy_rpa_exception import EasyRpaException
from easyrpa.enums.easy_rpa_exception_code_enum import EasyRpaExceptionCodeEnum
from database.models import DispatchJob
from easyrpa.tools import str_tools,number_tool

def check_dispatch_job(job:DispatchJob):
    if str_tools.str_is_empty(job.job_name):
        raise EasyRpaException('job_name cannot be empty',EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None)
    
    if str_tools.str_is_empty(job.cron):
        raise EasyRpaException('cron cannot be empty',EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None)
    
    if str_tools.str_is_empty(job.flow_code):
        raise EasyRpaException('flow_code cannot be empty',EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None)
    
    if number_tool.num_is_empty(job.job_type):
        raise EasyRpaException('job_type cannot be empty',EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None)