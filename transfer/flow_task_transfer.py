from easyrpa.models.agent_models.flow_task_exe_res_dto import FlowTaskExeResDTO
from models.task.task_detail_model import TaskDetailModel
from database.models import FlowTask
from easyrpa.enums.flow_task_status_enum import FlowTaskStatusEnum
from core import site_manager_core,flow_manager_core,flow_config_manager_core

def request_json_to_FlowTaskExeResDTO(json_data:dict) -> FlowTaskExeResDTO:
    return FlowTaskExeResDTO(**json_data)

def task2TaskDetailModel(data:FlowTask,jobs_map:dict[int,DispatchJob]) -> TaskDetailModel:
    # base data
    job = jobs_map.get(data.job_id) if jobs_map is not None and data.job_id is not None else None
    
    # transfer
    detail = JobDataDetailModel(
        id=data.id,
        job_id=data.job_id,
        job_name=job.job_name if job is not None else None,
        data_business_no = data.data_business_no,
        data_json=data.data_json,
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
    sites_map = flow_manager_core.search_flow_by_ids(ids=flow_ids)

    # search config
    config_ids = [item.flow_config_id for item in datas]
    configs = flow_config_manager_core.search_config_by_ids(ids=config_ids)
    configs_map = {item.id:item for item in configs}

    # search sub source

    # search result code


    return [data2DataDetailModel(data=data,jobs_map=jobs_map) for data in datas]