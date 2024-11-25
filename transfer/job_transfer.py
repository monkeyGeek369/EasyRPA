from models.job.job_detail_model import JobDetailModel
from models.flow.flow_detail_model import FlowDetailModel
from models.flow_config.flow_config_detail_model import FlowConfigDetailModel
from database.models import DispatchJob
from core import flow_manager_core,flow_config_manager_core,job_manager_core,job_data_manager_core
from easyrpa.enums.job_type_enum import JobTypeEnum

def job2JobDetailModel(data:DispatchJob,flow_map:dict[int,FlowDetailModel],config_map:dict[int,FlowConfigDetailModel],parent_map:dict[int,DispatchJob]) -> JobDetailModel:
    # base data
    flow = flow_map.get(data.flow_code) if flow_map is not None and data.flow_code is not None else None
    config = config_map.get(data.flow_config_id) if config_map is not None and data.flow_config_id is not None else None
    parent = parent_map.get(data.parent_job) if parent_map is not None and data.parent_job is not None else None
    job_typs = JobTypeEnum.DATA_PULL if data.job_type == 1 else JobTypeEnum.DATA_PUSH

    # data count
    data_count = job_data_manager_core.search_count_by_job_id(job_id=data.id)
    
    # transfer
    detail = JobDetailModel(
        id=data.id,
        job_name=data.job_name,
        data_count=data_count,
        cron=data.cron,
        flow_code=data.flow_code,
        flow_name=flow.flow_name if flow is not None else None,
        flow_config_id=data.flow_config_id,
        flow_config_name= config.config_name if config is not None else None,
        job_type=data.job_type,
        job_type_name=job_typs.value[2],
        parent_job=data.parent_job,
        parent_job_name=parent.job_name if parent is not None else None,
        current_data_id=data.current_data_id,
        last_record_id=data.last_record_id,
        created_id=data.created_id,
        created_time=data.created_time,
        modify_id=data.modify_id,
        modify_time=data.modify_time,
        trace_id=data.trace_id,
        is_active=data.is_active
    )

    return detail

def jobs2JobDetailModels(datas:list[DispatchJob]) -> list[JobDetailModel]:
    # search all flow
    flow_codes = [item.flow_code for item in datas]
    flows = flow_manager_core.search_flow_by_codes(codes=flow_codes)
    flow_map = {item.flow_code:item for item in flows}

    # search all flow config
    config_ids = [item.flow_config_id for item in datas]
    configs = flow_config_manager_core.search_config_by_ids(ids=config_ids)
    config_map = {item.id:item for item in configs}

    # search parent job
    parent_ids = [item.parent_job for item in datas]
    parent_jobs = job_manager_core.search_job_by_ids(ids=parent_ids)
    parent_map = {item.id:item for item in parent_jobs}

    return [job2JobDetailModel(data=data,flow_map=flow_map,config_map=config_map,parent_map=parent_map) for data in datas]