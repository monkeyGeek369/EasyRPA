from models.meta_data_item.meta_data_item_detail_model import MetaDataItemDetailModel
from database.meta_data_item_db_manager import MetaDataItemDbManager
from transfer.site_transfer import sits2SiteDetailModels
from easyrpa.tools import number_tool,str_tools
from easyrpa.models.easy_rpa_exception import EasyRpaException
from easyrpa.enums.easy_rpa_exception_code_enum import EasyRpaExceptionCodeEnum
from easyrpa.tools.common_tools import CommonTools
from transfer import meta_data_transfer
from database.models import MetaDataItem

def search_by_params(id:int) -> list[MetaDataItemDetailModel]:
    # search db
    db_result = MetaDataItemDbManager.get_all_meta_data_items_by_meta_id(meta_id=id)

    result = meta_data_transfer.metaDataItems2MetaDataItemDetailModels(db_result)
    return result

def add_meta_data_item(meta_id:int,business_code:str,name_en:str,name_cn:str) -> int:
    item = MetaDataItem(
        meta_id=meta_id,
        business_code=business_code,
        name_en=name_en,
        name_cn=name_cn
    )
    result = MetaDataItemDbManager.create_meta_data_item(item=item)
    return result.id

def modify_meta_data_item(id:int,meta_id:int,business_code:str,name_en:str,name_cn:str,is_active:bool) -> bool:
    # base check 
    if number_tool.num_is_empty(id):
        raise EasyRpaException("id is empty",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,id)
    if number_tool.num_is_empty(meta_id):
        raise EasyRpaException("meta id is empty",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,meta_id)
    if str_tools.str_is_empty(business_code):
        raise EasyRpaException("business code is empty",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,business_code)
    if str_tools.str_is_empty(name_en):
        raise EasyRpaException("name en is empty",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,name_en)
    if str_tools.str_is_empty(name_cn):
        raise EasyRpaException("name cn is empty",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,name_cn)
    
    item = MetaDataItem(
        id=id,
        meta_id=meta_id,
        business_code=business_code,
        name_en=name_en,
        name_cn=name_cn,
        is_active=is_active
    )

    MetaDataItemDbManager.update_meta_data_item(item=item)
    return True

def delete_meta_data_item(item_id:int) -> bool:
    if number_tool.num_is_empty(item_id):
        raise EasyRpaException("meta data item id is empty",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,item_id)
    
    item = MetaDataItem(
        id=item_id
    )

    MetaDataItemDbManager.delete_meta_data_item(item=item)
    return True