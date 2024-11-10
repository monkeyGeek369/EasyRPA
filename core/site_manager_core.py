from database.models import Site
from easyrpa.models.base.sort_base_model import SortBaseModel
from models.site.site_detail_model import SiteDetailModel
from database.site_db_manager import SiteDbManager
from transfer.site_transfer import sits2SiteDetailModels
from easyrpa.tools import number_tool,str_tools
from easyrpa.models.easy_rpa_exception import EasyRpaException
from easyrpa.enums.easy_rpa_exception_code_enum import EasyRpaExceptionCodeEnum
from database.flow_db_manager import FlowDbManager
from easyrpa.tools.common_tools import CommonTools

def search_sites_by_params(do:Site,page: int,page_size: int,sorts: list[SortBaseModel]) -> list[SiteDetailModel]:
    # search db
    db_result = SiteDbManager.select_page_list(do=do,
                                               page=CommonTools.initPage(page=page),
                                               page_size=CommonTools.initPageSize(pageSize=page_size),
                                               sorts=CommonTools.initSorts(sorts=sorts)) 
    result = sits2SiteDetailModels(db_result)
    
    return result

def search_count_by_params(do:Site) -> int:
    return SiteDbManager.select_count(do=do)

def add_site(site_name:str,site_description:str) -> int:
    return SiteDbManager.add_site(site_name=site_name,site_description=site_description)

def modify_site(site_id:int,site_name:str,site_description:str,is_active:bool) -> bool:
    # base check 
    if number_tool.num_is_empty(site_id):
        raise EasyRpaException("site id is empty",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,site_id)
    if str_tools.str_is_empty(site_name):
        raise EasyRpaException("site name is empty",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,site_name)
    if str_tools.str_is_empty(site_description):
        raise EasyRpaException("site description is empty",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,site_description)
    SiteDbManager.update_site(site_id=site_id,site_name=site_name,site_description=site_description,is_active=is_active)
    return True

def delete_site(site_id:int) -> bool:
    if number_tool.num_is_empty(site_id):
        raise EasyRpaException("site id is empty",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,site_id)
    
    # check site is using
    ls = FlowDbManager.get_flow_by_site_id(site_id=site_id)
    if ls is not None and len(ls) > 0:
        raise EasyRpaException("site is using",EasyRpaExceptionCodeEnum.EXECUTE_ERROR.value[1],None,site_id)
    
    return SiteDbManager.delete_site(site_id=site_id)
