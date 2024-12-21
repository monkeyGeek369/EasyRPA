from database.db_session import db_session,update_common_fields,create_common_fields
from database.models import FlowTaskLog
from robot_statu_db_manager import RobotStatuDBManager

class FlowTaskLogDBManager:

    @db_session
    def get_all_flow_task_log(session):
        return session.query(FlowTaskLog).all()

    @db_session
    def get_flow_task_log_by_id(session, id):
        return session.query(FlowTaskLog).filter(FlowTaskLog.id == id).first()

    @db_session
    def create_flow_task_log(session, flow_task_log:FlowTaskLog):

        # task_id不可以为空
        if not flow_task_log.task_id:
            raise ValueError("Task ID cannot be empty")
        
        # log_type不可以为空
        if not flow_task_log.log_type:
            raise ValueError("Log type cannot be empty")
        
        # set current robot ip
        robot = RobotStatuDBManager.get_robot_statu_by_task_id(task_id=flow_task_log.task_id)
        if robot:
            flow_task_log.robot_ip = robot.robot_ip
        
        create_common_fields(flow_task_log)
        session.add(flow_task_log)
        session.commit()
        session.refresh(flow_task_log)
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

            # set current robot ip
            robot = RobotStatuDBManager.get_robot_statu_by_task_id(task_id=flow_task_log.task_id)
            # robot_ip不为空则更新
            if data.robot_ip:
                flow_task_log.robot_ip = data.robot_ip
            elif robot:
                flow_task_log.robot_ip = robot.robot_ip

            update_common_fields(flow_task_log)
            session.commit()
            session.refresh(flow_task_log)
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
    
    @db_session
    def select_page_list(session,do:FlowTaskLog,page: int,page_size: int,sorts: dict) -> list[FlowTaskLog]:
        # 构造排序条件
        sort_conditions = []
        if sorts is None or len(sorts) == 0:
            sort_conditions.append(getattr(FlowTaskLog, 'id').desc())
        else:
            for key, value in sorts.items():
                if value == 'asc':
                    sort_conditions.append(getattr(FlowTaskLog, key).asc())
                elif value == 'desc':
                    sort_conditions.append(getattr(FlowTaskLog, key).desc())

        # 执行查询
        query = session.query(FlowTaskLog).filter(
            FlowTaskLog.id == do.id if do.id is not None else True,
            FlowTaskLog.task_id == do.task_id if do.task_id is not None else True,
            FlowTaskLog.created_id == do.created_id if do.created_id is not None else True,
            FlowTaskLog.modify_id == do.modify_id if do.modify_id is not None else True,
            FlowTaskLog.is_active == do.is_active if do.is_active is not None else True
            )
        if len(sort_conditions) > 0:
            query = query.order_by(*sort_conditions)
        query = query.limit(page_size).offset((page - 1) * page_size)

        # 返回结果
        return query.all()
    
    @db_session
    def select_count(session,do:FlowTaskLog) -> int:
        query = session.query(FlowTaskLog).filter(
            FlowTaskLog.id == do.id if do.id is not None else True,
            FlowTaskLog.task_id == do.task_id if do.task_id is not None else True,
            FlowTaskLog.created_id == do.created_id if do.created_id is not None else True,
            FlowTaskLog.modify_id == do.modify_id if do.modify_id is not None else True,
            FlowTaskLog.is_active == do.is_active if do.is_active is not None else True
            )
        return query.count()
    