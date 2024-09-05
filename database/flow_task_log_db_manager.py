from database.db_session import db_session,update_common_fields,create_common_fields
from database.models import FlowTaskLog

class FlowTaskLogDBManager:

    @db_session
    def get_all_flow_task_log(session):
        return session.query(FlowTaskLog).all()

    @db_session
    def get_flow_task_log_by_id(session, id):
        return session.query(FlowTaskLog).filter(FlowTaskLog.id == id).first()

    @db_session
    def create_flow_task_log(session, flow_task_log:FlowTaskLog):
        if not flow_task_log:
            raise ValueError("Flow task log cannot be empty")
        
        # task_id不可以为空
        if not flow_task_log.task_id:
            raise ValueError("Task ID cannot be empty")
        
        # log_type不可以为空
        if not flow_task_log.log_type:
            raise ValueError("Log type cannot be empty")
        
        create_common_fields(flow_task_log)
        session.add(flow_task_log)
        session.commit()
        return flow_task_log

    @db_session
    def update_flow_task_log(session, data:FlowTaskLog):
        # id不可以为空
        if not data.id:
            raise ValueError("Log ID cannot be empty")

        flow_task_log = session.query(FlowTaskLog).filter(FlowTaskLog.id == data.id).first()
        if flow_task_log:
            # task_id不为空则更新
            if data.task_id:
                flow_task_log.task_id = data.task_id
            
            # log_type不为空则更新
            if data.log_type:
                flow_task_log.log_type = data.log_type

            # message不为空则更新
            if data.message:
                flow_task_log.message = data.message
            
            # screenshot不为空则更新
            if data.screenshot:
                flow_task_log.screenshot = data.screenshot

            # robot_ip不为空则更新
            if data.robot_ip:
                flow_task_log.robot_ip = data.robot_ip

            update_common_fields(flow_task_log)
            session.commit()
            return flow_task_log
        return None

    @db_session
    def delete_flow_task_log(session, id):
        # id不可以为空
        if not id:
            raise ValueError("Log ID cannot be empty")
        flow_task_log = session.query(FlowTaskLog).filter(FlowTaskLog.id == id).first()
        if flow_task_log:
            session.delete(flow_task_log)
            session.commit()
            return True
        return False