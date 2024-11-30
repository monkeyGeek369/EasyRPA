from easyrpa.models.agent_models.flow_task_exe_res_dto import FlowTaskExeResDTO
from models.task.task_detail_model import TaskDetailModel
from models.task_log.task_log_detail_model import TaskLogDetailModel
from database.models import FlowTask,Flow,FlowTaskLog
from easyrpa.enums.flow_task_status_enum import FlowTaskStatusEnum
from easyrpa.enums.log_type_enum import LogTypeEnum
from core import site_manager_core,flow_manager_core,flow_config_manager_core,meta_data_item_manager_core
from configuration.app_config_manager import AppConfigManager
from models.site.site_detail_model import SiteDetailModel
from models.flow_config.flow_config_detail_model import FlowConfigDetailModel
from models.meta_data_item.meta_data_item_detail_model import MetaDataItemDetailModel 

def request_json_to_FlowTaskExeResDTO(json_data:dict) -> FlowTaskExeResDTO:
    return FlowTaskExeResDTO(**json_data)

def task2TaskDetailModel(data:FlowTask,sites_map:dict[int,SiteDetailModel],flows_map:dict[int,Flow],configs_map:dict[int,FlowConfigDetailModel],
                         source_map:dict[int,MetaDataItemDetailModel],task_status_map:dict) -> TaskDetailModel:
    # base data
    site = sites_map.get(data.site_id) if sites_map is not None and data.site_id is not None else None
    flow = flows_map.get(data.flow_id) if flows_map is not None and data.flow_id is not None else None
    config = configs_map.get(data.flow_config_id) if configs_map is not None and data.flow_config_id is not None else None
    source = source_map.get(data.sub_source) if source_map is not None and data.sub_source is not None else None
    
    # transfer
    detail = TaskDetailModel(
        id=data.id,
        site_id=data.site_id,
        site_name=site.site_name if site is not None else None,
        flow_id=data.flow_id,
        flow_code=flow.flow_code if flow is not None else None,
        flow_name=flow.flow_name if flow is not None else None,
        flow_config_id=data.flow_config_id,
        flow_config_name=config.config_name if config is not None else None,
        biz_no=data.biz_no,
        sub_source=data.sub_source,
        sub_source_name=source.name_en if source is not None else None,
        status=data.status,
        status_name=task_status_map.get(data.status) if task_status_map.get(data.status) is not None else None,
        result_code=data.result_code,
        result_message=data.result_message,
        result_data=data.result_data,
        retry_number=data.retry_number,
        screenshot_base64=data.screenshot_base64,
        request_standard_message=data.request_standard_message,
        flow_standard_message=data.flow_standard_message,
        task_result_message=data.task_result_message,
        flow_result_handle_message=data.flow_result_handle_message,
        created_id=data.created_id,
        created_time=data.created_time,
        modify_id=data.modify_id,
        modify_time=data.modify_time,
        trace_id=data.trace_id,
        is_active=data.is_active
    )

    return detail

def tasks2TaskDetailModels(datas:list[FlowTask]) -> list[TaskDetailModel]:
    # search site
    site_ids = [item.site_id for item in datas]
    sites = site_manager_core.search_sites_by_ids(site_ids=site_ids)
    sites_map = {item.id:item for item in sites}

    # search flow
    flow_ids = [item.flow_id for item in datas]
    flows_map = flow_manager_core.search_flow_by_ids(ids=flow_ids)

    # search config
    config_ids = [item.flow_config_id for item in datas]
    configs = flow_config_manager_core.search_config_by_ids(ids=config_ids)
    configs_map = {item.id:item for item in configs}

    # search sub source
    app = AppConfigManager()
    sub_source_items = meta_data_item_manager_core.get_meta_data_item_by_meta_code(code=app.get_flow_task_sub_source_meta_code())
    source_map = {int(item.business_code):item for item in sub_source_items}

    # task status
    task_status_map = {}
    task_status_map[FlowTaskStatusEnum.SUCCESS.value[1]] = FlowTaskStatusEnum.SUCCESS.value[2]
    task_status_map[FlowTaskStatusEnum.FAIL.value[1]] = FlowTaskStatusEnum.FAIL.value[2]
    task_status_map[FlowTaskStatusEnum.WAIT_EXE.value[1]] = FlowTaskStatusEnum.WAIT_EXE.value[2]
    task_status_map[FlowTaskStatusEnum.EXECUTION.value[1]] = FlowTaskStatusEnum.EXECUTION.value[2]

    return [task2TaskDetailModel(data=data,sites_map=sites_map,flows_map=flows_map,configs_map=configs_map,source_map=source_map,task_status_map=task_status_map) for data in datas]

def taskLog2TaskLogDetailModel(data:FlowTaskLog,log_type_map:dict[int,str]) -> TaskLogDetailModel:
    # base data
    log_type_name = log_type_map.get(data.log_type) if log_type_map is not None and data.log_type is not None else None
    
    # transfer
    detail = TaskLogDetailModel(
        id=data.id,
        task_id=data.task_id,
        log_type=data.log_type,
        log_type_name=log_type_name,
        message=data.message,
        screenshot=data.screenshot,
        robot_ip=data.robot_ip,
        created_id=data.created_id,
        created_time=data.created_time,
        modify_id=data.modify_id,
        modify_time=data.modify_time,
        trace_id=data.trace_id,
        is_active=data.is_active
    )

    return detail

def taskLogs2TaskLogDetailModels(datas:list[FlowTaskLog]) -> list[TaskLogDetailModel]:
    # log type
    log_type_map = {}
    log_type_map[LogTypeEnum.TXT.value[1]] = LogTypeEnum.TXT.value[2]
    log_type_map[LogTypeEnum.SCREENSHOTS.value[1]] = LogTypeEnum.SCREENSHOTS.value[2]
    log_type_map[LogTypeEnum.TASK_RESULT.value[1]] = LogTypeEnum.TASK_RESULT.value[2]
    log_type_map[LogTypeEnum.TASK_RESULT_NOTIFY.value[1]] = LogTypeEnum.TASK_RESULT_NOTIFY.value[2]

    return [taskLog2TaskLogDetailModel(data=data,log_type_map=log_type_map) for data in datas]
