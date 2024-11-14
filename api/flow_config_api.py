from flask import Blueprint
from easyrpa.tools.request_tool import easyrpa_request_wrapper
from easyrpa.tools.number_tool import num_is_empty
from easyrpa.tools.str_tools import str_is_empty
from easyrpa.tools.json_tools import JsonTool
from easyrpa.models.easy_rpa_exception import EasyRpaException
from easyrpa.enums.easy_rpa_exception_code_enum import EasyRpaExceptionCodeEnum
from models.flow_config.flow_config_search_req_model import FlowConfigSearchReqModel
from models.flow_config.flow_config_search_res_model import FlowConfigSearchResModel


flow_config_api_bp =  Blueprint('flow_config_api',__name__)

@flow_config_api_bp.route('/flow/config/search', methods=['POST'])
@easyrpa_request_wrapper
def search_flow_config(dto:FlowConfigSearchReqModel) -> FlowConfigSearchResModel:
    pass


