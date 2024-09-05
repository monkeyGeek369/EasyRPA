from database.db_session import db_session,update_common_fields,create_common_fields
from database.models import RobotStatu



class RobotStatuDBManager:
    @db_session
    def get_all_robot_statu(session):
        return session.query(RobotStatu).all()

    @db_session
    def get_robot_statu_by_id(session, id):
        return session.query(RobotStatu).filter(RobotStatu.id == id).first()

    @db_session
    def create_robot_statu(session, robot_statu:RobotStatu):
        # robot_statu不可以为空
        if not robot_statu:
            raise ValueError("RobotStatu cannot be empty")
        
        # robot_ip不可以为空
        if not robot_statu.robot_ip:
            raise ValueError("Robot ip cannot be empty")
        
        # robot_code不可以为空
        if not robot_statu.robot_code:
            raise ValueError("Robot code cannot be empty")
        
        # 不可以创建已经存在的robot_ip
        if session.query(RobotStatu).filter(RobotStatu.robot_ip == robot_statu.robot_ip).first():
            raise ValueError("Robot ip already exists")

        # 不可以创建已经存在的robot_code
        if session.query(RobotStatu).filter(RobotStatu.robot_code == robot_statu.robot_code).first():
            raise ValueError("Robot code already exists")
        
        create_common_fields(robot_statu)
        session.add(robot_statu)
        session.commit()
        return robot_statu

    @db_session
    def update_robot_statu(session, data:RobotStatu):
        # id不可以为空
        if not data.id:
            raise ValueError("RobotStatu ID cannot be empty")
        
        robot_statu = session.query(RobotStatu).filter(RobotStatu.id == data.id).first()
        if robot_statu:
            # 如果更新code，则只有在code除自己外唯一时才更新，否则报错
            if data.robot_code and data.robot_code != robot_statu.robot_code:
                if session.query(RobotStatu).filter(RobotStatu.robot_code == data.robot_code).filter(RobotStatu.id != data.id).first():
                    raise ValueError("Robot code already exists")
                robot_statu.robot_code = data.robot_code
            # 如果更新ip，则只有在ip除自己外唯一时才更新，否则报错
            if data.robot_ip and data.robot_ip != robot_statu.robot_ip:
                if session.query(RobotStatu).filter(RobotStatu.robot_ip == data.robot_ip).filter(RobotStatu.id != data.id).first():
                    raise ValueError("Robot ip already exists")
                robot_statu.robot_ip = data.robot_ip

            update_common_fields(robot_statu)
            session.commit()
            return robot_statu
        return None

    @db_session
    def delete_robot_statu(session, id):
        robot_statu = session.query(RobotStatu).filter(RobotStatu.id == id).first()
        if robot_statu:
            session.delete(robot_statu)
            session.commit()
            return True
        return False