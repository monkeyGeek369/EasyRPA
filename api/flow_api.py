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
from core import flow_manager_core,meta_data_item_manager_core
from models.flow.flow_add_req_model import FlowAddReqModel
from models.flow.flow_update_req_model import FlowUpdateReqModel
from models.meta_data_item.meta_data_item_search_res_model import MetaDataItemSearchResModel
from configuration.app_config_manager import AppConfigManager
from easyrpa.models.flow.flow_script_search_dto import FlowScriptSearchDTO
from easyrpa.models.flow.flow_script_info_dto import FlowScriptInfoDTO

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
def get_flow_rpa_type(params) -> MetaDataItemSearchResModel:
    app = AppConfigManager()
    meta_code = app.get_flow_rpa_type_meta_code()
    data = meta_data_item_manager_core.get_meta_data_item_by_meta_code(code=meta_code)
    result = MetaDataItemSearchResModel(
        data=data
    )

    return JsonTool.any_to_dict(result)

@flow_api_bp.route('/flow/biz/type', methods=['POST'])
@easyrpa_request_wrapper
def get_flow_biz_type(params) -> MetaDataItemSearchResModel:
    app = AppConfigManager()
    meta_code = app.get_flow_biz_type_meta_code()
    data = meta_data_item_manager_core.get_meta_data_item_by_meta_code(code=meta_code)
    result = MetaDataItemSearchResModel(
        data=data
    )

    return JsonTool.any_to_dict(result)

@flow_api_bp.route('/flow/retry/code', methods=['POST'])
@easyrpa_request_wrapper
def get_flow_retry_code(params) -> MetaDataItemSearchResModel:
    app = AppConfigManager()
    meta_code = app.get_flow_retry_code_meta_code()
    data = meta_data_item_manager_core.get_meta_data_item_by_meta_code(code=meta_code)
    result = MetaDataItemSearchResModel(
        data=data
    )

    return JsonTool.any_to_dict(result)

@flow_api_bp.route('/flow/update/script', methods=['POST'])
@easyrpa_request_wrapper
def update_flow_script(dto:FlowUpdateReqModel) -> bool:
    flow = Flow(
        id=dto.get("id"),
        request_check_script=dto.get("request_check_script"),
        request_adapt_script=dto.get("request_adapt_script"),
        flow_exe_script=dto.get("flow_exe_script"),
        flow_result_handle_script=dto.get("flow_result_handle_script")
    )
    return flow_manager_core.updata_flow_script(flow=flow)

@flow_api_bp.route('/flow/search/dim', methods=['POST'])
@easyrpa_request_wrapper
def search_dim_flow(query:str) -> FlowSearchResModel:
    flows = flow_manager_core.search_flow_by_name_or_code(query_str=query)
    result = FlowSearchResModel(
        data=flows,
        total=None,
        sorts=None
    )
    return result

@flow_api_bp.route('/flow/search/script', methods=['POST'])
@easyrpa_request_wrapper
def flow_script_search(dto:FlowScriptSearchDTO) -> FlowScriptInfoDTO:
    if str_is_empty(dto.get("flow_code")):
        raise EasyRpaException("flow code is empty",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,dto)
    if str_is_empty(dto.get("script_type")):
        raise EasyRpaException("script type is empty",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,dto)

    flows = flow_manager_core.search_flow_by_codes(codes=[dto.get("flow_code")])
    if len(flows) == 0:
        raise EasyRpaException("flow not found",EasyRpaExceptionCodeEnum.DATA_NOT_FOUND.value[1],None,dto)
    if len(flows) > 1:
        raise EasyRpaException("flow found more than one",EasyRpaExceptionCodeEnum.DATA_NOT_FOUND.value[1],None,dto)
    flow = flows[0]

    # get script
    script = None
    if dto.get("script_type") == "check":
        script = flow.request_check_script
    elif dto.get("script_type") == "adapter":
        script = flow.request_adapt_script
    elif dto.get("script_type") == "execution":
        script = flow.flow_exe_script
    elif dto.get("script_type") == "response":
        script = flow.flow_result_handle_script

    result = FlowScriptInfoDTO(
        flow_code=flow.flow_code,
        script_type= dto.get("script_type"),
        script=script
    )

    return result
