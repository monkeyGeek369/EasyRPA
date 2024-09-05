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
        
        # task_id不可以为空
        if not robot_log.task_id:
            raise ValueError("Task ID cannot be empty")
        
        # log_type不可以为空
        if not robot_log.log_type:
            raise ValueError("Log type cannot be empty")
        
        # message不可以为空
        if not robot_log.message:
            raise ValueError("Message cannot be empty")
        
        create_common_fields(robot_log)
        session.add(robot_log)
        session.commit()
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