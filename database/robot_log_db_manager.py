from database.db_session import db_session,update_common_fields,create_common_fields
from database.models import RobotLog

class RobotLogDBManager:

    @db_session
    def get_all_robot_log(session):
        return session.query(RobotLog).all()

    @db_session
    def get_robot_log_by_id(session, id):
        return session.query(RobotLog).filter(RobotLog.id == id).first()

    @db_session
    def create_robot_log(session, robot_log:RobotLog):
        # robot_id不可以为空
        if not robot_log.robot_id:
            raise ValueError("Robot ID cannot be empty")
        
        # log_type不可以为空
        if not robot_log.log_type:
            raise ValueError("Log type cannot be empty")
        
        # message不可以为空
        if not robot_log.message:
            raise ValueError("Message cannot be empty")
        
        create_common_fields(robot_log)
        session.add(robot_log)
        session.commit()
        session.refresh(robot_log)
        return robot_log

    @db_session
    def update_robot_log(session, data:RobotLog):
        # id不可以为空
        if not data.id:
            raise ValueError("ID cannot be empty")

        robot_log = session.query(RobotLog).filter(RobotLog.id == data.id).first()
        if robot_log:

            # robot_id不为空时才更新
            if data.robot_id:
                robot_log.robot_id = data.robot_id
            
            # task_id不为空时才更新
            if data.task_id:
                robot_log.task_id = data.task_id
            
            # log_type不为空时才更新
            if data.log_type:
                robot_log.log_type = data.log_type
            
            # message不为空时才更新
            if data.message:
                robot_log.message = data.message
            
            update_common_fields(robot_log)
            session.commit()
            session.refresh(robot_log)
            return robot_log
        return None

    @db_session
    def delete_robot_log(session, id):
         # id不可以为空
        if not id:
            raise ValueError("ID cannot be empty")
        robot_log = session.query(RobotLog).filter(RobotLog.id == id).first()
        if robot_log:
            session.delete(robot_log)
            session.commit()
            return True
        return False
    
    @db_session
    def delete_robot_log_by_robot_id(session, robot_id:int):
        session.query(RobotLog).filter(RobotLog.robot_id == robot_id).delete()
        session.commit()
        return True
    
    @db_session
    def select_page_list(session,do:RobotLog,page: int,page_size: int,sorts: dict) -> list[RobotLog]:
        # 构造排序条件
        sort_conditions = []
        if sorts is None or len(sorts) == 0:
            sort_conditions.append(getattr(RobotLog, 'id').desc())
        else:
            for key, value in sorts.items():
                if value == 'asc':
                    sort_conditions.append(getattr(RobotLog, key).asc())
                elif value == 'desc':
                    sort_conditions.append(getattr(RobotLog, key).desc())

        # 执行查询
        query = session.query(RobotLog).filter(
            RobotLog.id == do.id if do.id is not None else True,
            RobotLog.robot_id == do.robot_id if do.robot_id is not None else True,
            RobotLog.task_id == do.task_id if do.task_id is not None else True,
            RobotLog.log_type == do.log_type if do.log_type is not None else True,
            RobotLog.created_id == do.created_id if do.created_id is not None else True,
            RobotLog.modify_id == do.modify_id if do.modify_id is not None else True,
            RobotLog.is_active == do.is_active if do.is_active is not None else True
            )
        if len(sort_conditions) > 0:
            query = query.order_by(*sort_conditions)
        query = query.limit(page_size).offset((page - 1) * page_size)

        # 返回结果
        return query.all()
    
    @db_session
    def select_count(session,do:RobotLog) -> int:
        query = session.query(RobotLog).filter(
            RobotLog.id == do.id if do.id is not None else True,
            RobotLog.robot_id == do.robot_id if do.robot_id is not None else True,
            RobotLog.task_id == do.task_id if do.task_id is not None else True,
            RobotLog.log_type == do.log_type if do.log_type is not None else True,
            RobotLog.created_id == do.created_id if do.created_id is not None else True,
            RobotLog.modify_id == do.modify_id if do.modify_id is not None else True,
            RobotLog.is_active == do.is_active if do.is_active is not None else True
            )
        return query.count()
    