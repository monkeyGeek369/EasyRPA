from models.site.site_detail_model import SiteDetailModel
from database.models import Site
from copy import deepcopy

def site2SiteDetailModel(site:Site) -> SiteDetailModel:
    # copy
    site_detail = SiteDetailModel(
        id=site.id,
        site_name=site.site_name,
        site_description=site.site_description,
        created_id=site.created_id,
        created_time=site.created_time,
        modify_id=site.modify_id,
        modify_time=site.modify_time,
        trace_id=site.trace_id,
        is_active=site.is_active
    )

    return site_detail

def sits2SiteDetailModels(sites:list[Site]) -> list[SiteDetailModel]:
    return [site2SiteDetailModel(site) for site in sites]