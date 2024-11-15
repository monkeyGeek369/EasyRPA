from dataclasses import dataclass
from easyrpa.models.base.request_page_base_model import RequestPageBaseModel

@dataclass
class MetaDataSearchReqModel(RequestPageBaseModel):
    id:int
    name:str
    code:str
    description:str
    is_active:bool