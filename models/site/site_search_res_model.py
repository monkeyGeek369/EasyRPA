from dataclasses import dataclass
from easyrpa.models.base.response_page_base_model import ResponsePageBaseModel
from site_detail_model import SiteDetailModel


@dataclass
class SiteSearchResModel(ResponsePageBaseModel):
    data:list[SiteDetailModel]