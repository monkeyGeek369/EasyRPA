from flask import Blueprint
from easyrpa.tools.request_tool import easyrpa_request_wrapper
from easyrpa.tools.number_tool import num_is_empty
from easyrpa.tools.str_tools import str_is_empty
from easyrpa.tools.json_tools import JsonTool
from easyrpa.models.easy_rpa_exception import EasyRpaException
from easyrpa.enums.easy_rpa_exception_code_enum import EasyRpaExceptionCodeEnum
from models.flow_config.flow_config_search_req_model import FlowConfigSearchReqModel
from models.flow_config.flow_config_search_res_model import FlowConfigSearchResModel
from database.models import FlowConfiguration
from core import flow_config_manager_core
from models.flow_config.flow_config_add_req_model import FlowConfigAddReqModel
from models.flow_config.flow_config_update_req_model import FlowConfigUpdateReqModel


flow_config_api_bp =  Blueprint('flow_config_api',__name__)

@flow_config_api_bp.route('/flow/config/search', methods=['POST'])
@easyrpa_request_wrapper
def search_flow_config(dto:FlowConfigSearchReqModel) -> FlowConfigSearchResModel:
    # base check
    if num_is_empty(dto.get("page")):
        raise EasyRpaException("search page is empty",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,dto)
    if num_is_empty(dto.get("page_size")):
        raise EasyRpaException("search page size is empty",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,dto)
    
    # dto to do
    config_obj = FlowConfiguration()
    config_obj.id = dto.get("id")
    config_obj.flow_id = dto.get("flow_id")
    config_obj.config_name = dto.get("config_name")
    config_obj.config_description = dto.get("config_description")
    config_obj.is_active = dto.get("is_active")

    # search from db
    search_result = flow_config_manager_core.search_flow_configs_by_params(do=config_obj,page=dto.get("page"),page_size=dto.get("page_size"),sorts=dto.get("sorts"))
    
    # search count
    total = flow_config_manager_core.search_count_by_params(do=config_obj)

    # return
    result = FlowConfigSearchResModel(
        total=total,
        data=search_result,
        sorts=dto.get("sorts")
    )

    return JsonTool.any_to_dict(result)

@flow_config_api_bp.route('/flow/config/add', methods=['POST'])
@easyrpa_request_wrapper
def add_config(dto:FlowConfigAddReqModel) -> bool:
    ret = flow_config_manager_core.add_config(flow_id=dto.get("flow_id"),
                                              config_name=dto.get("config_name"),
                                              config_description=dto.get("config_description"),
                                              config_json=dto.get("config_json"))

    if ret is None or ret < 0:
        raise EasyRpaException("add flow config failed",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,dto)
    return True

@flow_config_api_bp.route('/flow/config/update', methods=['POST'])
@easyrpa_request_wrapper
def update_config(dto:FlowConfigUpdateReqModel) -> bool:
    return flow_config_manager_core.modify_config(id=dto.get("id"),
                                                  flow_id=dto.get("flow_id"),
                                                  config_name=dto.get("config_name"),
                                                  config_description=dto.get("config_description"),
                                                  config_json=dto.get("config_json"),
                                                  is_active=dto.get("is_active"))

@flow_config_api_bp.route('/flow/config/delete', methods=['POST'])
@easyrpa_request_wrapper
def delete_config(id:int) -> bool:
    return flow_config_manager_core.delete_config(id=id)

