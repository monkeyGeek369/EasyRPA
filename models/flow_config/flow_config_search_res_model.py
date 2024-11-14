from dataclasses import dataclass
from easyrpa.models.base.response_page_base_model import ResponsePageBaseModel
from models.flow_config.flow_config_detail_model import FlowConfigDetailModel


@dataclass
class FlowConfigSearchResModel(ResponsePageBaseModel):
    data:list[FlowConfigDetailModel]