from database.db_session import db_session,update_common_fields,create_common_fields
from database.models import DispatchRecord
from easyrpa.tools import str_tools,number_tool

class DispatchRecordDBManager:

    @db_session
    def get_all_dispatch_records(session):
        return session.query(DispatchRecord).all()
    
    @db_session
    def get_dispatch_record_by_id(session, id) -> DispatchRecord:
        if number_tool.num_is_empty(id):
            return None
        return session.query(DispatchRecord).filter(DispatchRecord.id == id).first()
    
    @db_session
    def create_dispatch_record(session, dispatch_record:DispatchRecord) -> DispatchRecord:
        # job_id不可以为空
        if number_tool.num_is_empty(dispatch_record.job_id):
            raise ValueError("Job ID cannot be empty")
        
        # status不可以为空
        if number_tool.num_is_empty(dispatch_record.status):
            raise ValueError("Status cannot be empty")
        
        create_common_fields(dispatch_record)
        session.add(dispatch_record)
        session.commit()
        session.refresh(dispatch_record)
        return dispatch_record
    
    @db_session
    def update_dispatch_record(session, data:DispatchRecord):
        if number_tool.num_is_empty(data.id):
            raise ValueError("Dispatch Record ID cannot be empty")
        
        dispatch_record = session.query(DispatchRecord).filter(DispatchRecord.id == data.id).first()

        if dispatch_record is not None:
            # job_id不为空则可更新
            if number_tool.num_is_not_empty(data.job_id):
                dispatch_record.job_id = data.job_id

            # flow_task_id不为空则可更新
            if number_tool.num_is_not_empty(data.flow_task_id):
                dispatch_record.flow_task_id = data.flow_task_id

            # status不为空则可更新
            if number_tool.num_is_not_empty(data.status):
                dispatch_record.status = data.status

            # result_message不为空则可更新
            if str_tools.str_is_not_empty(data.result_message):
                dispatch_record.result_message = data.result_message
            
            if number_tool.num_is_not_empty(data.handler_data_id):
                dispatch_record.handler_data_id = data.handler_data_id

            update_common_fields(dispatch_record)
            session.commit()
            session.refresh(dispatch_record)
            return dispatch_record
        return None
    
    @db_session
    def delete_dispatch_record(session, id):
        if number_tool.num_is_empty(id):
            raise ValueError("Dispatch Record ID cannot be empty")

        dispatch_record = session.query(DispatchRecord).filter(DispatchRecord.id == id).first()

        if dispatch_record is not None:
            session.delete(dispatch_record)
            session.commit()
            return True
        return False
    
    @db_session
    def delete_dispatch_record_by_job_id(session, job_id):
        if number_tool.num_is_empty(job_id):
            raise ValueError("Job ID cannot be empty")

        session.query(DispatchRecord).filter(DispatchRecord.job_id == job_id).delete()
        session.commit()
    
    @db_session
    def select_page_list(session,do:DispatchRecord,page: int,page_size: int,sorts: dict) -> list[DispatchRecord]:
        # 构造排序条件
        sort_conditions = []
        if sorts is None or len(sorts) == 0:
            sort_conditions.append(getattr(DispatchRecord, 'id').desc())
        else:
            for key, value in sorts.items():
                if value == 'asc':
                    sort_conditions.append(getattr(DispatchRecord, key).asc())
                elif value == 'desc':
                    sort_conditions.append(getattr(DispatchRecord, key).desc())

        # 执行查询
        query = session.query(DispatchRecord).filter(
            DispatchRecord.id == do.id if do.id is not None else True,
            DispatchRecord.job_id == do.job_id if do.job_id is not None else True,
            DispatchRecord.flow_task_id == do.flow_task_id if do.flow_task_id is not None else True,
            DispatchRecord.status == do.status if do.status is not None else True,
            DispatchRecord.created_id == do.created_id if do.created_id is not None else True,
            DispatchRecord.modify_id == do.modify_id if do.modify_id is not None else True,
            DispatchRecord.is_active == do.is_active if do.is_active is not None else True
            )
        if len(sort_conditions) > 0:
            query = query.order_by(*sort_conditions)
        query = query.limit(page_size).offset((page - 1) * page_size)

        # 返回结果
        return query.all()
    
    @db_session
    def select_count(session,do:DispatchRecord) -> int:
        query = session.query(DispatchRecord).filter(
            DispatchRecord.id == do.id if do.id is not None else True,
            DispatchRecord.job_id == do.job_id if do.job_id is not None else True,
            DispatchRecord.flow_task_id == do.flow_task_id if do.flow_task_id is not None else True,
            DispatchRecord.status == do.status if do.status is not None else True,
            DispatchRecord.created_id == do.created_id if do.created_id is not None else True,
            DispatchRecord.modify_id == do.modify_id if do.modify_id is not None else True,
            DispatchRecord.is_active == do.is_active if do.is_active is not None else True
            )
        return query.count()
    
    @db_session
    def select_dispatch_records_by_ids(session, ids: list[int]) -> list[DispatchRecord]:
        if ids is None or len(ids) == 0:
            return []
        return session.query(DispatchRecord).filter(DispatchRecord.id.in_(ids)).all()
    