from dataclasses import dataclass
from easyrpa.models.base.response_do_base_model import ResponseDoBaseModel


@dataclass
class MetaDataDetailModel(ResponseDoBaseModel):
    id:int
    name:str
    code:str
    description:str