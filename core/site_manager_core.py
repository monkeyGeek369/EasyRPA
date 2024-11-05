from database.models import Site
from easyrpa.models.base.sort_base_model import SortBaseModel
from models.site.site_detail_model import SiteDetailModel

def search_sites_by_params(do:Site,page: int,page_size: int,sorts: list[SortBaseModel]) -> list[SiteDetailModel]:
    # todo
    pass