from flask import Blueprint
from easyrpa.tools.request_tool import easyrpa_request_wrapper
from models.job.job_record_search_req_model import JobRecordSearchReqModel
from models.job.job_record_search_res_model import JobRecordSearchResModel
from models.job.job_record_detail_model import JobRecordDetailModel
from easyrpa.models.easy_rpa_exception import EasyRpaException
from easyrpa.enums.easy_rpa_exception_code_enum import EasyRpaExceptionCodeEnum
from easyrpa.tools import str_tools,logs_tool,number_tool
from database.models import DispatchRecord
from core import job_record_manager_core
from easyrpa.tools.json_tools import JsonTool
from models.job.job_record_status_model import JobRecordStatusModel

job_record_api_bp =  Blueprint('job_record_api',__name__)

@job_record_api_bp.route('/job/record/search', methods=['POST'])
@easyrpa_request_wrapper
def search_job_records(dto:JobRecordSearchReqModel) -> JobRecordSearchResModel:
    # base check
    if number_tool.num_is_empty(dto.get("page")):
        raise EasyRpaException("search page is empty",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,dto)
    if number_tool.num_is_empty(dto.get("page_size")):
        raise EasyRpaException("search page size is empty",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,dto)
    
    # dto to do
    record_obj = DispatchRecord()
    record_obj.id = dto.get("id")
    record_obj.job_id=dto.get("job_id")
    record_obj.flow_task_id=dto.get("flow_task_id")
    record_obj.status=dto.get("status")
    record_obj.is_active = dto.get("is_active")

    # search from db
    search_result = job_record_manager_core.search_records_by_params(do=record_obj,page=dto.get("page"),page_size=dto.get("page_size"),sorts=dto.get("sorts"))
    
    # search count
    total = job_record_manager_core.search_count_by_params(do=record_obj)

    # return
    result = JobRecordSearchResModel(
        total=total,
        data=search_result,
        sorts=dto.get("sorts")
    )

    return JsonTool.any_to_dict(result)

@job_record_api_bp.route('/job/record/status', methods=['POST'])
@easyrpa_request_wrapper
def get_record_status(data) -> list[JobRecordStatusModel]:
    result = job_record_manager_core.get_record_status()
    return JsonTool.any_to_dict(result)
