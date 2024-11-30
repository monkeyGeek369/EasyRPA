from flask import Blueprint,request
from easyrpa.tools import str_tools,logs_tool,number_tool
from easyrpa.tools.request_tool import easyrpa_request_wrapper
from easyrpa.models.easy_rpa_exception import EasyRpaException
from easyrpa.enums.easy_rpa_exception_code_enum import EasyRpaExceptionCodeEnum
from database.dispatch_job_db_manager import DispatchJobDBManager
from job import dispatch_job_manager
from models.job.job_search_req_model import JobSearchReqModel
from models.job.job_search_res_model import JobSearchResModel
from database.models import DispatchJob
from core import job_manager_core
from easyrpa.tools.json_tools import JsonTool
from models.job.job_add_req_model import JobAddReqModel
from models.job.job_update_req_model import JobUpdateReqModel
from models.job.job_type_model import JobTypeModel


job_api_bp =  Blueprint('job_api',__name__)

@job_api_bp.route('/job/exe', methods=['POST'])
@easyrpa_request_wrapper
def dispatch_job_exe(job_id:int) -> bool:
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

@job_api_bp.route('/job/search/jobs', methods=['POST'])
@easyrpa_request_wrapper
def search_jobs(dto:JobSearchReqModel) -> JobSearchResModel:
    # base check
    if number_tool.num_is_empty(dto.get("page")):
        raise EasyRpaException("search page is empty",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,dto)
    if number_tool.num_is_empty(dto.get("page_size")):
        raise EasyRpaException("search page size is empty",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,dto)
    
    # dto to do
    job_obj = DispatchJob()
    job_obj.id = dto.get("id")
    job_obj.job_name = dto.get("job_name")
    job_obj.flow_code = dto.get("flow_code")
    job_obj.flow_config_id = dto.get("flow_config_id")
    job_obj.job_type = dto.get("job_type")
    job_obj.parent_job = dto.get("parent_job")
    job_obj.is_active = dto.get("is_active")

    # search from db
    search_result = job_manager_core.search_jobs_by_params(do=job_obj,page=dto.get("page"),page_size=dto.get("page_size"),sorts=dto.get("sorts"))
    
    # search count
    total = job_manager_core.search_count_by_params(do=job_obj)

    # return
    result = JobSearchResModel(
        total=total,
        data=search_result,
        sorts=dto.get("sorts")
    )

    return JsonTool.any_to_dict(result)

@job_api_bp.route('/job/add', methods=['POST'])
@easyrpa_request_wrapper
def add_job(dto:JobAddReqModel) -> bool:
    job_manager_core.add_job(job_name=dto.get("job_name"),
                                   cron=dto.get("cron"),
                                   flow_code=dto.get("flow_code"),
                                   flow_config_id=dto.get("flow_config_id"),
                                   job_type=dto.get("job_type"),
                                   parent_job=int(dto.get("parent_job")) if dto.get("parent_job") is not None else None,
                                   current_data_id=int(dto.get("current_data_id")) if dto.get("current_data_id") is not None else None,
                                   last_record_id=int(dto.get("last_record_id")) if dto.get("last_record_id") is not None else None)
    return True

@job_api_bp.route('/job/update', methods=['POST'])
@easyrpa_request_wrapper
def update_job(dto:JobUpdateReqModel) -> bool:
    return job_manager_core.modify_job(id=dto.get("id"),
                                       job_name=dto.get("job_name"),
                                        cron=dto.get("cron"),
                                        flow_code=dto.get("flow_code"),
                                        flow_config_id=dto.get("flow_config_id"),
                                        job_type=dto.get("job_type"),
                                        parent_job=int(dto.get("parent_job")) if dto.get("parent_job") is not None else None,
                                        current_data_id=int(dto.get("current_data_id")) if dto.get("current_data_id") is not None else None,
                                        last_record_id=int(dto.get("last_record_id")) if dto.get("last_record_id") is not None else None,
                                       is_active=dto.get("is_active"))

@job_api_bp.route('/job/delete', methods=['POST'])
@easyrpa_request_wrapper
def delete_job(id:int) -> bool:
    return job_manager_core.delete_job(id=id)

@job_api_bp.route('/job/type', methods=['POST'])
@easyrpa_request_wrapper
def get_job_type(data) -> list[JobTypeModel]:
    return job_manager_core.get_job_type()

@job_api_bp.route('/job/search/dim', methods=['POST'])
@easyrpa_request_wrapper
def search_jobs_dim(name:str)->JobSearchResModel:
    datas = job_manager_core.search_job_by_name(name=name)

    result  = JobSearchResModel(
        data=datas,
        total=None,
        sorts=None
    )
    return JsonTool.any_to_dict(result)
