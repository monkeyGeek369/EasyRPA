from database.models import DispatchData
from easyrpa.tools.common_tools import CommonTools
from easyrpa.models.base.sort_base_model import SortBaseModel
from models.job.job_data_detail_model import JobDataDetailModel
from database.dispatch_data_db_manager import DispatchDataDBManager
from transfer.job_data_transfer import datas2DataDetailModels


def search_datas_by_params(do:DispatchData,page: int,page_size: int,sorts: list[SortBaseModel]) -> list[JobDataDetailModel]:
    # search db
    db_result = DispatchDataDBManager.select_page_list(do=do,
                                               page=CommonTools.initPage(page=page),
                                               page_size=CommonTools.initPageSize(pageSize=page_size),
                                               sorts=CommonTools.initSorts(sorts=sorts)) 
    result = datas2DataDetailModels(db_result)
    
    return result

def search_count_by_params(do:DispatchData) -> int:
    return DispatchDataDBManager.select_count(do=do)

def search_count_by_job_id(job_id: int) -> int:
    if job_id is None or job_id == 0:
        return 0
    return DispatchDataDBManager.get_count(job_id=job_id)
