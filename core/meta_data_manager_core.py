from database.models import MetaData
from easyrpa.models.base.sort_base_model import SortBaseModel
from models.meta_data.meta_data_detail_model import MetaDataDetailModel
from database.meta_data_db_manager import MetaDataDbManager
from easyrpa.tools import number_tool,str_tools
from easyrpa.models.easy_rpa_exception import EasyRpaException
from easyrpa.enums.easy_rpa_exception_code_enum import EasyRpaExceptionCodeEnum
from easyrpa.tools.common_tools import CommonTools
from database.meta_data_db_manager import MetaDataDbManager
from database.meta_data_item_db_manager import MetaDataItemDbManager
from transfer import meta_data_transfer

def search_meta_data_by_params(do:MetaData,page: int,page_size: int,sorts: list[SortBaseModel]) -> list[MetaDataDetailModel]:
    # search db
    db_result = MetaDataDbManager.select_page_list(do=do,
                                               page=CommonTools.initPage(page=page),
                                               page_size=CommonTools.initPageSize(pageSize=page_size),
                                               sorts=CommonTools.initSorts(sorts=sorts)) 
    result = meta_data_transfer.metaData2MetaDataDetailModels(db_result)
    
    return result


def search_count_by_params(do:MetaData) -> int:
    return MetaDataDbManager.select_count(do=do)

def add_meta_data(name:str,code:str,description:str) -> int:
    do = MetaData()
    do.name = name
    do.code = code
    do.description = description
    do.is_active = True
    ret = MetaDataDbManager.create_meta_data(meta=do)
    return ret.id

def modify_meta_data(id:int,name:str,code:str,description:str,is_active:bool) -> bool:
    # base check 
    if number_tool.num_is_empty(id):
        raise EasyRpaException("id is empty",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,id)
    if str_tools.str_is_empty(name):
        raise EasyRpaException("name is empty",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,name)
    if str_tools.str_is_empty(code):
        raise EasyRpaException("code is empty",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,code)
    if str_tools.str_is_empty(description):
        raise EasyRpaException("description is empty",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,description)
    
    do = MetaData()
    do.id = id
    do.name = name
    do.code = code
    do.description = description
    do.is_active = is_active

    MetaDataDbManager.update_meta_data(meta=do)
    return True

def delete_meta_data(id:int) -> bool:
    if number_tool.num_is_empty(id):
        raise EasyRpaException("id is empty",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,id)
    
    # check meta data is using
    ls = MetaDataItemDbManager.get_all_meta_data_items_by_meta_id(meta_id=id)
    if ls is not None and len(ls) > 0:
        raise EasyRpaException("meta data is using",EasyRpaExceptionCodeEnum.EXECUTE_ERROR.value[1],None,id)
    
    MetaDataDbManager.delete_meta_data(id=id)
    return True

def search_meta_datas_by_codes(codes:list[str]) -> list[MetaDataDetailModel]:
    if codes is None or len(codes) == 0:
        return []
    db_result = MetaDataDbManager.get_meta_datas_by_codes(codes=codes)
    result = meta_data_transfer.metaData2MetaDataDetailModels(db_result)
    return result