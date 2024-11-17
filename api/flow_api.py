from flask import Blueprint
from easyrpa.tools.request_tool import easyrpa_request_wrapper
from easyrpa.tools.number_tool import num_is_empty
from easyrpa.tools.str_tools import str_is_empty
from easyrpa.tools.json_tools import JsonTool
from easyrpa.models.easy_rpa_exception import EasyRpaException
from easyrpa.enums.easy_rpa_exception_code_enum import EasyRpaExceptionCodeEnum
from database.models import Flow
from models.flow.flow_search_req_model import FlowSearchReqModel
from models.flow.flow_search_res_model import FlowSearchResModel
from core import flow_manager_core
from models.flow.flow_add_req_model import FlowAddReqModel
from models.flow.flow_update_req_model import FlowUpdateReqModel
from models.meta_data_item.meta_data_item_search_res_model import MetaDataItemSearchResModel

flow_api_bp =  Blueprint('flow_api',__name__)

@flow_api_bp.route('/flow/search', methods=['POST'])
@easyrpa_request_wrapper
def search_flows(dto:FlowSearchReqModel) -> FlowSearchResModel:
    # base check
    if num_is_empty(dto.get("page")):
        raise EasyRpaException("search page is empty",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,dto)
    if num_is_empty(dto.get("page_size")):
        raise EasyRpaException("search page size is empty",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,dto)
    
    # dto to do
    flow_obj = Flow()
    flow_obj.id = dto.get("id")
    flow_obj.site_id = dto.get("site_id")
    flow_obj.flow_code = dto.get("flow_code")
    flow_obj.flow_name = dto.get("flow_name")
    flow_obj.flow_rpa_type = dto.get("flow_rpa_type")
    flow_obj.flow_exe_env = dto.get("flow_exe_env")
    flow_obj.flow_biz_type = dto.get("flow_biz_type")
    flow_obj.retry_code = dto.get("retry_code")
    flow_obj.is_active = dto.get("is_active")
    
    # search from db
    search_result = flow_manager_core.search_flows_by_params(do=flow_obj,page=dto.get("page"),page_size=dto.get("page_size"),sorts=dto.get("sorts"))

    # search count
    total = flow_manager_core.search_count_by_params(do=flow_obj)

    # return
    result = FlowSearchResModel(
        total=total,
        data=search_result,
        sorts=dto.get("sorts")
    )

    return JsonTool.any_to_dict(result)

@flow_api_bp.route('/flow/add', methods=['POST'])
@easyrpa_request_wrapper
def add_flow(dto:FlowAddReqModel) -> bool:
    # base check
    if num_is_empty(dto.get("site_id")):
        raise EasyRpaException("site id is empty",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,dto)
    if str_is_empty(dto.get("flow_code")):
        raise EasyRpaException("flow_code is empty",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,dto)
    
    flow = Flow(
        site_id=dto.get("site_id"),
        flow_code=dto.get("flow_code"),
        flow_name=dto.get("flow_name"),
        flow_rpa_type=dto.get("flow_rpa_type"),
        flow_exe_env=dto.get("flow_exe_env"),
        flow_biz_type=dto.get("flow_biz_type"),
        max_retry_number=dto.get("max_retry_number"),
        max_exe_time=dto.get("max_exe_time"),
        retry_code=dto.get("retry_code"),
        request_check_script=dto.get("request_check_script"),
        request_adapt_script=dto.get("request_adapt_script"),
        flow_exe_script=dto.get("flow_exe_script"),
        flow_result_handle_script=dto.get("flow_result_handle_script")
    )
    
    ret = flow_manager_core.add_flow(flow=flow)

    if ret is None:
        raise EasyRpaException("add flow failed",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,dto)
    return True

@flow_api_bp.route('/flow/update', methods=['POST'])
@easyrpa_request_wrapper
def update_flow(dto:FlowUpdateReqModel) -> bool:
    flow = Flow(
        id=dto.get("id"),
        site_id=dto.get("site_id"),
        flow_code=dto.get("flow_code"),
        flow_name=dto.get("flow_name"),
        flow_rpa_type=dto.get("flow_rpa_type"),
        flow_exe_env=dto.get("flow_exe_env"),
        flow_biz_type=dto.get("flow_biz_type"),
        max_retry_number=dto.get("max_retry_number"),
        max_exe_time=dto.get("max_exe_time"),
        retry_code=dto.get("retry_code"),
        request_check_script=dto.get("request_check_script"),
        request_adapt_script=dto.get("request_adapt_script"),
        flow_exe_script=dto.get("flow_exe_script"),
        flow_result_handle_script=dto.get("flow_result_handle_script"),
        is_active=dto.get("is_active")
    )
    return flow_manager_core.updata_flow(flow=flow)

@flow_api_bp.route('/flow/delete', methods=['POST'])
@easyrpa_request_wrapper
def delete_flow(id:int) -> bool:
    flow = Flow(
        id=id,
        is_active=False
    )
    flow_manager_core.logic_delete_flow(flow=flow)
    return True

@flow_api_bp.route('/flow/rpa/type', methods=['POST'])
@easyrpa_request_wrapper
def get_flow_rpa_type() -> MetaDataItemSearchResModel:
    pass

@flow_api_bp.route('/flow/exe/env', methods=['POST'])
@easyrpa_request_wrapper
def get_flow_exe_env() -> MetaDataItemSearchResModel:
    pass

@flow_api_bp.route('/flow/biz/type', methods=['POST'])
@easyrpa_request_wrapper
def get_flow_biz_type() -> MetaDataItemSearchResModel:
    pass