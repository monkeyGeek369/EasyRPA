from models.job.job_record_detail_model import JobRecordDetailModel
from database.models import DispatchRecord,DispatchJob,Flow
from core import flow_manager_core,task_manager_core,job_manager_core
from easyrpa.enums.job_status_enum import JobStatusEnum

def record2RecordDetailModel(data:DispatchRecord,jobs_map:dict[int,DispatchJob],task_flow_map:dict[int,Flow]) -> JobRecordDetailModel:
    # base data
    flow = task_flow_map.get(data.flow_task_id) if task_flow_map is not None and data.id is not None else None
    job = jobs_map.get(data.job_id) if jobs_map is not None and data.job_id is not None else None
    st_name = ""
    if data.status==JobStatusEnum.DISPATCHING.value[1]:
        st_name = JobStatusEnum.DISPATCHING.value[2]
    elif data.status==JobStatusEnum.DISPATCH_SUCCESS.value[1]:
        st_name = JobStatusEnum.DISPATCH_SUCCESS.value[2]
    elif data.status==JobStatusEnum.DISPATCH_FAIL.value[1]:
        st_name = JobStatusEnum.DISPATCH_FAIL.value[2]

    
    # transfer
    detail = JobRecordDetailModel(
        id=data.id,
        job_id=data.job_id,
        job_name=job.job_name if job is not None else None,
        flow_code=flow.flow_code if flow is not None else None,
        flow_name=flow.flow_name if flow is not None else None,
        flow_task_id=data.flow_task_id,
        status=data.status,
        status_name=st_name,
        result_message=data.result_message,
        created_id=data.created_id,
        created_time=data.created_time,
        modify_id=data.modify_id,
        modify_time=data.modify_time,
        trace_id=data.trace_id,
        is_active=data.is_active
    )

    return detail

def records2RecordDetailModels(datas:list[DispatchRecord]) -> list[JobRecordDetailModel]:
    # search parent job
    job_ids = [item.job_id for item in datas]
    jobs = job_manager_core.search_job_by_ids(ids=job_ids)
    jobs_map = {item.id:item for item in jobs}

    # search all flow by task id
    task_ids = [item.flow_task_id for item in datas]
    tasks = task_manager_core.get_flow_task_db_by_ids(ids=task_ids)
    flow_ids = [item.flow_id for item in tasks]
    flow_map = flow_manager_core.search_flow_by_ids(ids=flow_ids)
    
    # get task flow map
    task_flow_map = {}
    for task in tasks:
        if task.flow_id is not None:
            flow_item = flow_map.get(task.flow_id)
            if flow_item is not None:
                task_flow_map[task.id] = flow_item

    return [record2RecordDetailModel(data=data,jobs_map=jobs_map,task_flow_map=task_flow_map) for data in datas]