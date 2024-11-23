from models.flow_config.flow_config_detail_model import FlowConfigDetailModel
from database.models import FlowConfiguration,Flow
from core import flow_manager_core


def config2ConfigDetailModel(config:FlowConfiguration,flow_dict:dict[int,Flow]) -> FlowConfigDetailModel:
    flow = flow_dict.get(config.flow_id)
    
    config_detail = FlowConfigDetailModel(
        id=config.id,
        flow_id=flow.id if flow is not None else None,
        flow_code=flow.flow_code if flow is not None else None,
        flow_name=flow.flow_name if flow is not None else None,
        config_name=config.config_name,
        config_description=config.config_description,
        config_json=config.config_json,
        created_id=config.created_id,
        created_time=config.created_time,
        modify_id=config.modify_id,
        modify_time=config.modify_time,
        trace_id=config.trace_id,
        is_active=config.is_active
    )

    return config_detail

def configs2ConfigDetailModels(configs:list[FlowConfiguration]) -> list[FlowConfigDetailModel]:
    # get all flow ids and not null and distinct
    flow_ids = [config.flow_id for config in configs if config.flow_id is not None]
    flow_ids = list(set(flow_ids))

    # get flow
    flow_details = flow_manager_core.search_flow_by_ids(ids=flow_ids)

    return [config2ConfigDetailModel(config,flow_dict=flow_details) for config in configs]