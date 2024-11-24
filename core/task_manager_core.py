from database.flow_task_db_manager import FlowTaskDBManager
from database.models import FlowTask

def get_flow_task_db_by_ids(ids:list[int])->list[FlowTask]:
    if not ids:
        return []
    return FlowTaskDBManager.get_flow_task_by_ids(ids=ids)