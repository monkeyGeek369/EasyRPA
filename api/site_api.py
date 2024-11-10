from flask import Blueprint
from easyrpa.tools.request_tool import easyrpa_request_wrapper
from models.site.site_search_req_model import SiteSearchReqModel
from models.site.site_search_res_model import SiteSearchResModel
from models.site.site_add_req_model import SiteAddReqModel
from models.site.site_update_req_model import SiteUpdateReqModel
from easyrpa.tools.number_tool import num_is_empty
from easyrpa.tools.str_tools import str_is_empty
from easyrpa.tools.json_tools import JsonTool
from easyrpa.models.easy_rpa_exception import EasyRpaException
from easyrpa.enums.easy_rpa_exception_code_enum import EasyRpaExceptionCodeEnum
from core import site_manager_core
from database.models import Site

site_api_bp =  Blueprint('site_api',__name__)

@site_api_bp.route('/site/search/sites', methods=['POST'])
@easyrpa_request_wrapper
def search_sites(dto:SiteSearchReqModel) -> SiteSearchResModel:
    # base check
    if num_is_empty(dto.get("page")):
        raise EasyRpaException("search page is empty",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,dto)
    if num_is_empty(dto.get("page_size")):
        raise EasyRpaException("search page size is empty",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,dto)
    
    # dto to do
    site_obj = Site()
    site_obj.id = dto.get("id")
    site_obj.site_name = dto.get("site_name")
    site_obj.site_description = dto.get("site_description")
    site_obj.is_active = dto.get("is_active")

    # search from db
    search_result = site_manager_core.search_sites_by_params(do=site_obj,page=dto.get("page"),page_size=dto.get("page_size"),sorts=dto.get("sorts"))
    
    # search count
    total = site_manager_core.search_count_by_params(do=site_obj)

    # return
    result = SiteSearchResModel(
        total=total,
        data=search_result,
        sorts=dto.get("sorts")
    )

    return JsonTool.any_to_dict(result)

@site_api_bp.route('/site/add', methods=['POST'])
@easyrpa_request_wrapper
def add_site(dto:SiteAddReqModel) -> bool:
    # base check
    if str_is_empty(dto.get("site_name")):
        raise EasyRpaException("site name is empty",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,dto)
    if str_is_empty(dto.get("site_description")):
        raise EasyRpaException("site description is empty",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,dto)
    
    ret = site_manager_core.add_site(site_name=dto.get("site_name"),site_description=dto.get("site_description"))

    if ret is None:
        raise EasyRpaException("add site failed",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,dto)
    return True

@site_api_bp.route('/site/update', methods=['POST'])
@easyrpa_request_wrapper
def update_site(dto:SiteUpdateReqModel) -> bool:
    return site_manager_core.modify_site(site_id=dto.get("site_id"),site_name=dto.get("site_name"),site_description=dto.get("site_description"),is_active=dto.get("is_active"))

@site_api_bp.route('/site/delete', methods=['POST'])
@easyrpa_request_wrapper
def delete_site(site_id:int) -> bool:
    return site_manager_core.delete_site(site_id=site_id)