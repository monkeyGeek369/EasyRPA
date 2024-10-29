from flask import Blueprint,request
from easyrpa.tools import str_tools,logs_tool,number_tool
from easyrpa.tools.request_tool import easyrpa_request_wrapper
from easyrpa.models.easy_rpa_exception import EasyRpaException
from easyrpa.enums.easy_rpa_exception_code_enum import EasyRpaExceptionCodeEnum
from database.dispatch_job_db_manager import DispatchJobDBManager
from job import dispatch_job_manager


job_api_bp =  Blueprint('job_api',__name__)

@job_api_bp.route('/job/exe', methods=['POST'])
@easyrpa_request_wrapper
def flow_task_result_handler(job_id:int) -> bool:
    if number_tool.num_is_empty(job_id):
        raise EasyRpaException("job id is empty",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,None)
    
    # search job
    job = DispatchJobDBManager.get_dispatch_job_by_id(id=job_id)
    if job is None:
        raise EasyRpaException("job not found",EasyRpaExceptionCodeEnum.DATA_NOT_FOUND.value[1],None,job_id)

    # exe
    job_type_abc = dispatch_job_manager.get_job_type_impl(job_type=job.job_type)
    job_type_abc.execute_job(job_id=job_id)

    return True