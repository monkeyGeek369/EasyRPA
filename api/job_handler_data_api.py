from flask import Blueprint
from easyrpa.tools.request_tool import easyrpa_request_wrapper
from easyrpa.models.easy_rpa_exception import EasyRpaException
from easyrpa.enums.easy_rpa_exception_code_enum import EasyRpaExceptionCodeEnum
from easyrpa.tools import str_tools,logs_tool,number_tool
from easyrpa.tools.json_tools import JsonTool
from models.job.job_handler_data_search_req_model import JobHandlerDataSearchReqModel
from models.job.job_handler_data_search_res_model import JobHandlerDataSearchResModel
from database.models import DispatchHandlerData
from core import job_handler_data_manager_core
from models.base.meta_data_base_model import MetaDataBaseModel
from models.job.job_handler_data_update_req_model import JobHandlerDataUpdateReqModel

job_handler_data_api_bp =  Blueprint('job_handler_data_api',__name__)

@job_handler_data_api_bp.route('/job/handler/data/search', methods=['POST'])
@easyrpa_request_wrapper
def search_job_handler_datas(dto:JobHandlerDataSearchReqModel) -> JobHandlerDataSearchResModel:
    # base check
    if number_tool.num_is_empty(dto.get("page")):
        raise EasyRpaException("search page is empty",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,dto)
    if number_tool.num_is_empty(dto.get("page_size")):
        raise EasyRpaException("search page size is empty",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,dto)
    
    # dto to do
    handler_data = DispatchHandlerData()
    handler_data.id = dto.get("id")
    handler_data.job_id=dto.get("job_id")
    handler_data.data_job_id=dto.get("data_job_id")
    handler_data.data_id=dto.get("data_id")
    handler_data.status=dto.get("status")
    handler_data.is_active = dto.get("is_active")

    # search from db
    search_result = job_handler_data_manager_core.search_handler_datas_by_params(do=handler_data,page=dto.get("page"),page_size=dto.get("page_size"),sorts=dto.get("sorts"))
    
    # search count
    total = job_handler_data_manager_core.search_count_by_params(do=handler_data)

    # return
    result = JobHandlerDataSearchResModel(
        total=total,
        data=search_result,
        sorts=dto.get("sorts")
    )

    return JsonTool.any_to_dict(result)

@job_handler_data_api_bp.route('/job/handler/data/status', methods=['POST'])
@easyrpa_request_wrapper
def get_handler_data_status(data) -> list[MetaDataBaseModel]:
    result = job_handler_data_manager_core.get_handler_data_status()
    return JsonTool.any_to_dict(result)

@job_handler_data_api_bp.route('/job/handler/data/delete', methods=['POST'])
@easyrpa_request_wrapper
def delete_handler_data(id:int) -> bool:
    result = job_handler_data_manager_core.delete_handler_data(id=id)
    return JsonTool.any_to_dict(result)

@job_handler_data_api_bp.route('/job/handler/data/update/status', methods=['POST'])
@easyrpa_request_wrapper
def update_handler_data_status(dto:JobHandlerDataUpdateReqModel) -> bool:
    job_handler_data_manager_core.update_handler_data_status(id=dto.get("id"),status=dto.get("status"))
    return JsonTool.any_to_dict(True)
