from dataclasses import dataclass
from easyrpa.models.base.response_do_base_model import ResponseDoBaseModel


@dataclass
class MetaDataItemDetailModel(ResponseDoBaseModel):
    id:int
    meta_id:int
    business_code:str
    name_en:str
    name_cn:str