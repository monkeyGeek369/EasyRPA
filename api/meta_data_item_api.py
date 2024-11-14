from flask import Blueprint
from easyrpa.tools.request_tool import easyrpa_request_wrapper
from easyrpa.tools.number_tool import num_is_empty
from easyrpa.tools.str_tools import str_is_empty
from easyrpa.tools.json_tools import JsonTool
from easyrpa.models.easy_rpa_exception import EasyRpaException
from easyrpa.enums.easy_rpa_exception_code_enum import EasyRpaExceptionCodeEnum

meta_data_item_api_bp =  Blueprint('meta_data_item_api',__name__)

@meta_data_item_api_bp.route('/meta/data/item/search', methods=['POST'])
@easyrpa_request_wrapper
def search_meta_data_item(dto:any) -> any:
    pass