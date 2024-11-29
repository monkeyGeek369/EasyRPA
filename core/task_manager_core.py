from database.flow_task_db_manager import FlowTaskDBManager
from database.models import FlowTask
from easyrpa.models.base.sort_base_model import SortBaseModel
from models.task.task_detail_model import TaskDetailModel
from easyrpa.tools.common_tools import CommonTools
from transfer.flow_task_transfer import tasks2TaskDetailModels

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