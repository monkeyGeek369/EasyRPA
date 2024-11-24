from database.models import DispatchRecord
from easyrpa.models.base.sort_base_model import SortBaseModel
from models.job.job_record_detail_model import JobRecordDetailModel
from database.dispatch_record_db_manager import DispatchRecordDBManager
from easyrpa.tools.common_tools import CommonTools
from transfer.job_record_transfer import records2RecordDetailModels
from models.job.job_record_status_model import JobRecordStatusModel
from easyrpa.enums.job_status_enum import JobStatusEnum


def search_records_by_params(do:DispatchRecord,page: int,page_size: int,sorts: list[SortBaseModel]) -> list[JobRecordDetailModel]:
    # search db
    db_result = DispatchRecordDBManager.select_page_list(do=do,
                                               page=CommonTools.initPage(page=page),
                                               page_size=CommonTools.initPageSize(pageSize=page_size),
                                               sorts=CommonTools.initSorts(sorts=sorts)) 
    result = records2RecordDetailModels(db_result)
    
    return result

def search_count_by_params(do:DispatchRecord) -> int:
    return DispatchRecordDBManager.select_count(do=do)

def get_record_status() -> list[JobRecordStatusModel]:
    result = []
    result.append(JobRecordStatusModel(id=JobStatusEnum.DISPATCHING.value[1],des=JobStatusEnum.DISPATCHING.value[2]))
    result.append(JobRecordStatusModel(id=JobStatusEnum.DISPATCH_SUCCESS.value[1],des=JobStatusEnum.DISPATCH_SUCCESS.value[2]))
    result.append(JobRecordStatusModel(id=JobStatusEnum.DISPATCH_FAIL.value[1],des=JobStatusEnum.DISPATCH_FAIL.value[2]))

    return result
