from flask import Blueprint
from easyrpa.tools.request_tool import easyrpa_request_wrapper
from easyrpa.tools.number_tool import num_is_empty
from easyrpa.tools.str_tools import str_is_empty
from easyrpa.tools.json_tools import JsonTool
from easyrpa.models.easy_rpa_exception import EasyRpaException
from easyrpa.enums.easy_rpa_exception_code_enum import EasyRpaExceptionCodeEnum
from models.meta_data.meta_data_search_req_model import MetaDataSearchReqModel
from models.meta_data.meta_data_search_res_model import MetaDataSearchResModel
from database.models import MetaData
from core import meta_data_manager_core
from models.meta_data.meta_data_add_req_model import MetaDataAddReqModel
from models.meta_data.meta_data_update_req_model import MetaDataUpdateReqModel

meta_data_api_bp =  Blueprint('meta_data_api',__name__)

@meta_data_api_bp.route('/meta/data/search', methods=['POST'])
@easyrpa_request_wrapper
def search_meta_data(dto:MetaDataSearchReqModel) -> MetaDataSearchResModel:
    # base check
    if num_is_empty(dto.get("page")):
        raise EasyRpaException("search page is empty",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,dto)
    if num_is_empty(dto.get("page_size")):
        raise EasyRpaException("search page size is empty",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,dto)
    
    # dto to do
    meta_data = MetaData()
    meta_data.id = dto.get("id")
    meta_data.name = dto.get("name")
    meta_data.code = dto.get("code")
    meta_data.description = dto.get("description")
    meta_data.is_active = dto.get("is_active")

    # search from db
    search_result = meta_data_manager_core.search_meta_data_by_params(do=meta_data,page=dto.get("page"),page_size=dto.get("page_size"),sorts=dto.get("sorts"))
    
    # search count
    total = meta_data_manager_core.search_count_by_params(do=meta_data)

    # return
    result = MetaDataSearchResModel(
        total=total,
        data=search_result,
        sorts=dto.get("sorts")
    )

    return JsonTool.any_to_dict(result)

@meta_data_api_bp.route('/meta/data/add', methods=['POST'])
@easyrpa_request_wrapper
def add_meta_data(dto:MetaDataAddReqModel) -> bool:
    # base check
    if str_is_empty(dto.get("name")):
        raise EasyRpaException("name is empty",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,dto)
    if str_is_empty(dto.get("code")):
        raise EasyRpaException("code is empty",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,dto)
    if str_is_empty(dto.get("description")):
        raise EasyRpaException("description is empty",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,dto)
    
    ret = meta_data_manager_core.add_meta_data(name=dto.get("name"),code=dto.get("code"),description=dto.get("description"))

    if ret is None:
        raise EasyRpaException("add meta data failed",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,dto)
    return True

@meta_data_api_bp.route('/meta/data/update', methods=['POST'])
@easyrpa_request_wrapper
def update_meta_data(dto:MetaDataUpdateReqModel) -> bool:
    return meta_data_manager_core.modify_meta_data(id=dto.get("id"),name=dto.get("name"),code=dto.get("code"),description=dto.get("description"),is_active=dto.get("is_active"))

@meta_data_api_bp.route('/meta/data/delete', methods=['POST'])
@easyrpa_request_wrapper
def delete_meta_data(id:int) -> bool:
    return meta_data_manager_core.delete_meta_data(id=id)
