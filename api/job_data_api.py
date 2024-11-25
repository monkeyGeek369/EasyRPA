from flask import Blueprint
from easyrpa.tools.request_tool import easyrpa_request_wrapper
from models.job.job_data_search_req_model import JobDataSearchReqModel
from models.job.job_data_search_res_model import JobDataSearchResModel
from easyrpa.models.easy_rpa_exception import EasyRpaException
from easyrpa.enums.easy_rpa_exception_code_enum import EasyRpaExceptionCodeEnum
from easyrpa.tools import number_tool
from database.models import DispatchData
from core import job_data_manager_core
from easyrpa.tools.json_tools import JsonTool

job_data_api_bp =  Blueprint('job_data_api',__name__)

@job_data_api_bp.route('/job/data/search', methods=['POST'])
@easyrpa_request_wrapper
def search_data_records(dto:JobDataSearchReqModel) -> JobDataSearchResModel:
    # base check
    if number_tool.num_is_empty(dto.get("page")):
        raise EasyRpaException("search page is empty",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,dto)
    if number_tool.num_is_empty(dto.get("page_size")):
        raise EasyRpaException("search page size is empty",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,dto)
    
    # dto to do
    data_obj = DispatchData()
    data_obj.id = dto.get("id")
    data_obj.job_id = dto.get("job_id")
    data_obj.data_business_no = dto.get("data_business_no")
    data_obj.data_json = dto.get("data_json")
    data_obj.is_active = dto.get("is_active")

    # search from db
    search_result = job_data_manager_core.search_datas_by_params(do=data_obj,page=dto.get("page"),page_size=dto.get("page_size"),sorts=dto.get("sorts"))
    
    # search count
    total = job_data_manager_core.search_count_by_params(do=data_obj)

    # return
    result = JobDataSearchResModel(
        total=total,
        data=search_result,
        sorts=dto.get("sorts")
    )

    return JsonTool.any_to_dict(result)
