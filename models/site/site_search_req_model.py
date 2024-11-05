from dataclasses import dataclass
from easyrpa.models.base.request_page_base_model import RequestPageBaseModel

@dataclass
class SiteSearchReqModel(RequestPageBaseModel):
    id:int
    site_name:str
    site_description:str
    is_active:bool