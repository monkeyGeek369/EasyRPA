from database.flow_task_db_manager import FlowTaskDBManager
from database.models import FlowTask
from easyrpa.models.base.sort_base_model import SortBaseModel
from models.task.task_detail_model import TaskDetailModel
from easyrpa.tools.common_tools import CommonTools
from transfer.flow_task_transfer import tasks2TaskDetailModels
from models.base.meta_data_base_model import MetaDataBaseModel
from configuration.app_config_manager import AppConfigManager
from core import meta_data_item_manager_core
from easyrpa.enums.flow_task_status_enum import FlowTaskStatusEnum

def get_flow_task_db_by_ids(ids:list[int])->list[FlowTask]:
    if not ids:
        return []
    return FlowTaskDBManager.get_flow_task_by_ids(ids=ids)

def search_tasks_by_params(do:FlowTask,page: int,page_size: int,sorts: list[SortBaseModel]) -> list[TaskDetailModel]:
    # search db
    db_result = FlowTaskDBManager.select_page_list(do=do,
                                               page=CommonTools.initPage(page=page),
                                               page_size=CommonTools.initPageSize(pageSize=page_size),
                                               sorts=CommonTools.initSorts(sorts=sorts)) 
    result = tasks2TaskDetailModels(db_result)
    
    return result

def search_count_by_params(do:FlowTask) -> int:
    return FlowTaskDBManager.select_count(do=do)


def get_flow_task_by_id(id:int)->TaskDetailModel:
    detial = FlowTaskDBManager.get_flow_task_by_id(id=id)
    result = tasks2TaskDetailModels([detial])
    return result[0]

def get_all_source_types() -> list[MetaDataBaseModel]:
    app = AppConfigManager()
    sub_source_items = meta_data_item_manager_core.get_meta_data_item_by_meta_code(code=app.get_flow_task_sub_source_meta_code())
    result = [ MetaDataBaseModel(id=int(item.business_code),des=item.name_en) for item in sub_source_items]
    return result

def get_all_task_status() -> list[MetaDataBaseModel]:
    result = []
    result.append(MetaDataBaseModel(id=FlowTaskStatusEnum.SUCCESS.value[1],des=FlowTaskStatusEnum.SUCCESS.value[2]))
    result.append(MetaDataBaseModel(id=FlowTaskStatusEnum.FAIL.value[1],des=FlowTaskStatusEnum.FAIL.value[2]))
    result.append(MetaDataBaseModel(id=FlowTaskStatusEnum.WAIT_EXE.value[1],des=FlowTaskStatusEnum.WAIT_EXE.value[2]))
    result.append(MetaDataBaseModel(id=FlowTaskStatusEnum.EXECUTION.value[1],des=FlowTaskStatusEnum.EXECUTION.value[2]))

    return result

