from dataclasses import dataclass
from easyrpa.models.base.response_page_base_model import ResponsePageBaseModel
from models.flow.flow_detail_model import FlowDetailModel


@dataclass
class FlowSearchResModel(ResponsePageBaseModel):
    data:list[FlowDetailModel]