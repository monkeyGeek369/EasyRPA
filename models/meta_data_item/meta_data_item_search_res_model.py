from dataclasses import dataclass
from models.meta_data_item.meta_data_item_detail_model import MetaDataItemDetailModel

@dataclass
class MetaDataItemSearchResModel:
    data:list[MetaDataItemDetailModel]