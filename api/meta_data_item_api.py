from flask import Blueprint
from easyrpa.tools.request_tool import easyrpa_request_wrapper
from easyrpa.tools.number_tool import num_is_empty
from easyrpa.tools.str_tools import str_is_empty
from easyrpa.tools.json_tools import JsonTool
from easyrpa.models.easy_rpa_exception import EasyRpaException
from easyrpa.enums.easy_rpa_exception_code_enum import EasyRpaExceptionCodeEnum
from models.meta_data_item.meta_data_item_search_res_model import MetaDataItemSearchResModel
from core import meta_data_item_manager_core
from models.meta_data_item.meta_data_item_add_req_model import MetaDataItemAddReqModel
from models.meta_data_item.meta_data_item_update_req_model import MetaDataItemUpdateReqModel

meta_data_item_api_bp =  Blueprint('meta_data_item_api',__name__)

@meta_data_item_api_bp.route('/meta/data/item/search', methods=['POST'])
@easyrpa_request_wrapper
def search_meta_data_item(id:int) -> MetaDataItemSearchResModel:
    if num_is_empty(id):
        raise EasyRpaException("meta data id is empty",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,id)
    
    data = meta_data_item_manager_core.search_by_params(id=id)

    result = MetaDataItemSearchResModel(
        data=data
    )
    
    return JsonTool.any_to_dict(result)

@meta_data_item_api_bp.route('/meta/data/item/add', methods=['POST'])
@easyrpa_request_wrapper
def add_meta_data_item(dto:MetaDataItemAddReqModel) -> bool:
    # base check
    if num_is_empty(dto.get("meta_id")):
        raise EasyRpaException("meta data id is empty",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,dto)
    if str_is_empty(dto.get("business_code")):
        raise EasyRpaException("business code is empty",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,dto)
    if str_is_empty(dto.get("name_en")):
        raise EasyRpaException("name en is empty",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,dto)
    
    ret = meta_data_item_manager_core.add_meta_data_item(meta_id=dto.get("meta_id"),business_code=dto.get("business_code"),name_en=dto.get("name_en"),name_cn=dto.get("name_cn"))

    if ret is None:
        raise EasyRpaException("add meta data item failed",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,dto)
    return True

@meta_data_item_api_bp.route('/meta/data/item/update', methods=['POST'])
@easyrpa_request_wrapper
def update_meta_data_item(dto:MetaDataItemUpdateReqModel) -> bool:
    return meta_data_item_manager_core.modify_meta_data_item(id=dto.get("id"),meta_id=dto.get("meta_id"),business_code=dto.get("business_code"),name_en=dto.get("name_en"),name_cn=dto.get("name_cn"),is_active=dto.get("is_active"))

@meta_data_item_api_bp.route('/meta/data/item/delete', methods=['POST'])
@easyrpa_request_wrapper
def delete_meta_data_item(site_id:int) -> bool:
    return meta_data_item_manager_core.delete_meta_data_item(item_id=site_id)