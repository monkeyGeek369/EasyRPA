from database.models import DispatchJob
from easyrpa.models.base.sort_base_model import SortBaseModel
from models.job.job_detail_model import JobDetailModel
from database.dispatch_job_db_manager import DispatchJobDBManager
from easyrpa.tools.common_tools import CommonTools
from transfer.job_transfer import job2JobDetailModel,jobs2JobDetailModels
from easyrpa.tools import str_tools,number_tool
from easyrpa.models.easy_rpa_exception import EasyRpaException
from easyrpa.enums.easy_rpa_exception_code_enum import EasyRpaExceptionCodeEnum
from models.job.job_type_model import JobTypeModel
from easyrpa.enums.job_type_enum import JobTypeEnum


def search_jobs_by_params(do:DispatchJob,page: int,page_size: int,sorts: list[SortBaseModel]) -> list[JobDetailModel]:
    # search db
    db_result = DispatchJobDBManager.select_page_list(do=do,
                                               page=CommonTools.initPage(page=page),
                                               page_size=CommonTools.initPageSize(pageSize=page_size),
                                               sorts=CommonTools.initSorts(sorts=sorts)) 
    result = jobs2JobDetailModels(db_result)
    
    return result

def search_count_by_params(do:DispatchJob) -> int:
    return DispatchJobDBManager.select_count(do=do)

def search_job_by_ids(ids: list[int]) -> list[DispatchJob]:
    if ids is None or len(ids) == 0:
        return []
    return DispatchJobDBManager.search_job_by_ids(ids=ids)

def base_check(job:DispatchJob):
    if str_tools.str_is_empty(job.job_name):
        raise EasyRpaException('job_name cannot be empty',EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None)
    
    if str_tools.str_is_empty(job.cron):
        raise EasyRpaException('cron cannot be empty',EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None)
    
    if str_tools.str_is_empty(job.flow_code):
        raise EasyRpaException('flow_code cannot be empty',EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None)
    
    if number_tool.num_is_empty(job.flow_config_id):
        raise EasyRpaException('flow_config_id cannot be empty',EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None)
    
    if number_tool.num_is_empty(job.job_type):
        raise EasyRpaException('job_type cannot be empty',EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None)

def add_job(job_name:str,cron:str,flow_code:str,flow_config_id:int,job_type:int,parent_job:int,current_data_id:int,last_record_id:int) -> int:
    db = DispatchJob(
        job_name=job_name,
        cron=cron,
        flow_code=flow_code,
        flow_config_id=flow_config_id,
        job_type=job_type,
        parent_job=parent_job,
        current_data_id=current_data_id,
        last_record_id=last_record_id
    )

    # base check
    base_check(job=db)
    
    result = DispatchJobDBManager.create_dispatch_job(dispatch_job=db)
    if result is None:
        raise EasyRpaException("add job failed",EasyRpaExceptionCodeEnum.CREATE_FAILED.value[1],None,None)
    return result.id

def modify_job(id:int,job_name:str,cron:str,flow_code:str,flow_config_id:int,job_type:int,parent_job:int,current_data_id:int,last_record_id:int,is_active:bool) -> bool:
    # build db
    db = DispatchJob(
        id=id,
        job_name=job_name,
        cron=cron,
        flow_code=flow_code,
        flow_config_id=flow_config_id,
        job_type=job_type,
        parent_job=parent_job,
        current_data_id=current_data_id,
        last_record_id=last_record_id,
        is_active=is_active
    )

    # base check
    if number_tool.num_is_empty(id):
        raise EasyRpaException("id cannot be empty",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,id)
    base_check(job=db)

    DispatchJobDBManager.update_dispatch_job(data=db)
    return True

def delete_job(id:int) -> bool:
    if number_tool.num_is_empty(id):
        raise EasyRpaException("job id is empty",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,id)
    
    return DispatchJobDBManager.delete_dispatch_job(id=id)

def get_job_type() -> list[JobTypeModel]:
    return [JobTypeModel(id=job_type.value[1],des=job_type.value[2]) for job_type in JobTypeEnum]

def search_job_by_name(name:str) -> list[JobDetailModel]:
    if str_tools.str_is_empty(name):
        return []
    result = DispatchJobDBManager.search_job_by_name(name=name)
    return jobs2JobDetailModels(result)
