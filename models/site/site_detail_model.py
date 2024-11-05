from dataclasses import dataclass
from easyrpa.models.base.response_do_base_model import ResponseDoBaseModel


@dataclass
class SiteDetailModel(ResponseDoBaseModel):
    id:int
    site_name:str
    site_description:str