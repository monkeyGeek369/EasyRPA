from database.models import Site
from easyrpa.models.base.sort_base_model import SortBaseModel
from models.site.site_detail_model import SiteDetailModel
from database.site_db_manager import SiteDbManager
from transfer.site_transfer import sits2SiteDetailModels

def search_sites_by_params(do:Site,page: int,page_size: int,sorts: list[SortBaseModel]) -> list[SiteDetailModel]:
    # page and page_size transform
    if page < 1:
        page = 1
    if page_size < 1:
        page_size = 10
    
    # sort transform
    sort_dict = {}
    if sorts is None or len(sorts) == 0:
        sort_dict['id'] = 'desc'
    else:
        for sort in sorts:
            if sort.order == 'asc':
                sort_dict[sort.prop] = 'asc'
            else:
                sort_dict[sort.prop] = 'desc'

    # search db
    db_result = SiteDbManager.select_page_list(do=do,page=page,page_size=page_size,sorts=sort_dict) 
    result = sits2SiteDetailModels(db_result)
    
    return result