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

            update_common_fields(dispatch_record)
            session.commit()
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