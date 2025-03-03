from models.job.job_handler_data_detail_model import JobHandlerDataDetailModel
from database.models import DispatchJob,DispatchHandlerData
from core import job_manager_core
from easyrpa.enums.job_status_enum import JobStatusEnum

def handlerDatas2DetailModel(data:DispatchHandlerData,jobs_map:dict[int,DispatchJob]) -> JobHandlerDataDetailModel:
    # base data
    job = jobs_map.get(data.job_id) if jobs_map is not None and data.job_id is not None else None
    data_job = jobs_map.get(data.data_job_id) if jobs_map is not None and data.data_job_id is not None else None
    st_name = ""
    if data.status==JobStatusEnum.DISPATCHING.value[1]:
        st_name = JobStatusEnum.DISPATCHING.value[2]
    elif data.status==JobStatusEnum.DISPATCH_SUCCESS.value[1]:
        st_name = JobStatusEnum.DISPATCH_SUCCESS.value[2]
    elif data.status==JobStatusEnum.DISPATCH_FAIL.value[1]:
        st_name = JobStatusEnum.DISPATCH_FAIL.value[2]

    
    # transfer
    detail = JobHandlerDataDetailModel(
        id=data.id,
        job_id=data.job_id,
        job_name=job.job_name if job is not None else None, 
        data_job_id=data.data_job_id,
        data_job_name=data_job.job_name if data_job is not None else None,
        data_id=data.data_id,
        status=data.status,
        status_name=st_name,
        created_id=data.created_id,
        created_time=data.created_time,
        modify_id=data.modify_id,
        modify_time=data.modify_time,
        trace_id=data.trace_id,
        is_active=data.is_active
    )

    return detail

def handlerDatas2DetailModels(datas:list[DispatchHandlerData]) -> list[JobHandlerDataDetailModel]:
    # search parent job
    job_ids = [item.job_id for item in datas]
    data_job_ids = [item.data_job_id for item in datas]
    if data_job_ids is not None and len(data_job_ids) > 0:
        job_ids.extend(data_job_ids)
    jobs = job_manager_core.search_job_by_ids(ids=job_ids)
    jobs_map = {item.id:item for item in jobs}
   
    return [handlerDatas2DetailModel(data=data,jobs_map=jobs_map) for data in datas]