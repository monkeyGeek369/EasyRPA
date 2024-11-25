from models.job.job_data_detail_model import JobDataDetailModel
from database.models import DispatchData,DispatchJob
from core import job_manager_core

def data2DataDetailModel(data:DispatchData,jobs_map:dict[int,DispatchJob]) -> JobDataDetailModel:
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

def datas2DataDetailModels(datas:list[DispatchData]) -> list[JobDataDetailModel]:
    # search job
    job_ids = [item.job_id for item in datas]
    jobs = job_manager_core.search_job_by_ids(ids=job_ids)
    jobs_map = {item.id:item for item in jobs}

    return [data2DataDetailModel(data=data,jobs_map=jobs_map) for data in datas]