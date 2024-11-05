from flask import Blueprint
from easyrpa.tools.request_tool import easyrpa_request_wrapper
from models.site.site_search_req_model import SiteSearchReqModel
from models.site.site_search_res_model import SiteSearchResModel
from easyrpa.tools.number_tool import number_tool
from easyrpa.tools.str_tools import str_tools
from easyrpa.models.easy_rpa_exception import EasyRpaException
from easyrpa.enums.easy_rpa_exception_code_enum import EasyRpaExceptionCodeEnum
from core.site_manager_core import search_sites_by_params
from database.models import Site

site_api_bp =  Blueprint('site_api',__name__)

@site_api_bp.route('/site/search/sites', methods=['POST'])
@easyrpa_request_wrapper
def search_sites(dto:SiteSearchReqModel) -> SiteSearchResModel:
    # base check
    if number_tool.num_is_empty(dto.page):
        raise EasyRpaException("search page is empty",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,dto)
    if number_tool.num_is_empty(dto.size):
        raise EasyRpaException("search page size is empty",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,dto)
    
    # dto to do
    site_obj = Site()
    site_obj.id = dto.id
    site_obj.site_name = dto.site_name
    site_obj.site_description = dto.site_description
    site_obj.is_active = dto.is_active

    # search from db
    search_result = search_sites_by_params(do=site_obj,page=dto.page,page_size=dto.page_size,sorts=dto.sorts)
    total = 0
    if search_result is not None:
        total = len(search_result)

    # return
    result = SiteSearchResModel()
    result.total=total
    result.data=search_result
    result.sorts=dto.sorts

    return result