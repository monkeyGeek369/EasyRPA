from dataclasses import dataclass
from easyrpa.models.base.response_page_base_model import ResponsePageBaseModel
from models.meta_data.meta_data_detail_model import MetaDataDetailModel


@dataclass
class MetaDataSearchResModel(ResponsePageBaseModel):
    data:list[MetaDataDetailModel]