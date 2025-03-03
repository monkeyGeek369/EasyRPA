from database.models import DispatchHandlerData
from easyrpa.models.base.sort_base_model import SortBaseModel
from database.dispatch_handler_data_db_manager import DispatchHandlerDataDBManager
from models.job.job_handler_data_detail_model import JobHandlerDataDetailModel
from models.base.meta_data_base_model import MetaDataBaseModel
from easyrpa.tools.common_tools import CommonTools
from easyrpa.enums.job_status_enum import JobStatusEnum
from transfer.job_handler_data_transfer import handlerDatas2DetailModels


def search_handler_datas_by_params(do:DispatchHandlerData,page: int,page_size: int,sorts: list[SortBaseModel]) -> list[JobHandlerDataDetailModel]:
    # search db
    db_result = DispatchHandlerDataDBManager.select_page_list(do=do,
                                               page=CommonTools.initPage(page=page),
                                               page_size=CommonTools.initPageSize(pageSize=page_size),
                                               sorts=CommonTools.initSorts(sorts=sorts)) 
    result = handlerDatas2DetailModels(db_result)
    
    return result

def search_count_by_params(do:DispatchHandlerData) -> int:
    return DispatchHandlerDataDBManager.select_count(do=do)

def get_handler_data_status() -> list[MetaDataBaseModel]:
    result = []
    result.append(MetaDataBaseModel(id=JobStatusEnum.DISPATCHING.value[1],des=JobStatusEnum.DISPATCHING.value[2]))
    result.append(MetaDataBaseModel(id=JobStatusEnum.DISPATCH_SUCCESS.value[1],des=JobStatusEnum.DISPATCH_SUCCESS.value[2]))
    result.append(MetaDataBaseModel(id=JobStatusEnum.DISPATCH_FAIL.value[1],des=JobStatusEnum.DISPATCH_FAIL.value[2]))

    return result

def delete_handler_data(id:int) -> bool:
    DispatchHandlerDataDBManager.delete_dispatch_handler_data(id=id)
    return True

def update_handler_data_status(id:int,status:int) -> bool:
    data = DispatchHandlerData(
        id=id,
        status=status
    )
    DispatchHandlerDataDBManager.update_dispatch_handler_data(data=data)
    return True
