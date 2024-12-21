from database.db_session import db_session,update_common_fields,create_common_fields
from database.models import RobotStatu
from easyrpa.tools import str_tools
from easyrpa.enums.robot_status_type_enum import RobotStatusTypeEnum



class RobotStatuDBManager:
    @db_session
    def get_all_robot_statu(session)->list[RobotStatu]:
        return session.query(RobotStatu).all()
    
    @db_session
    def get_leisure_robot_statu(session) -> list[RobotStatu]:
        return session.query(RobotStatu).filter(RobotStatu.status == RobotStatusTypeEnum.LEISURE.value[1]).all()

    @db_session
    def get_robot_statu_by_id(session, id):
        return session.query(RobotStatu).filter(RobotStatu.id == id).first()

    @db_session
    def create_robot_statu(session, robot_statu:RobotStatu):
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
        session.refresh(robot_statu)
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
            
            robot_statu.status = data.status
            robot_statu.port = data.port
            robot_statu.current_task_id = data.current_task_id

            update_common_fields(robot_statu)
            session.commit()
            session.refresh(robot_statu)
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
    
    @db_session
    def search_robot_statu_by_code(session, robot_code:str) -> RobotStatu:
        if str_tools.str_is_empty(robot_code):
            return None
        return session.query(RobotStatu).filter(RobotStatu.robot_code == robot_code).first()
    
    
    @db_session
    def select_page_list(session,do:RobotStatu,page: int,page_size: int,sorts: dict) -> list[RobotStatu]:
        # 构造排序条件
        sort_conditions = []
        if sorts is None or len(sorts) == 0:
            sort_conditions.append(getattr(RobotStatu, 'id').desc())
        else:
            for key, value in sorts.items():
                if value == 'asc':
                    sort_conditions.append(getattr(RobotStatu, key).asc())
                elif value == 'desc':
                    sort_conditions.append(getattr(RobotStatu, key).desc())

        # 执行查询
        query = session.query(RobotStatu).filter(
            RobotStatu.id == do.id if do.id is not None else True,
            RobotStatu.robot_code.contains(do.robot_code) if do.robot_code is not None else True,
            RobotStatu.robot_ip.contains(do.robot_ip) if do.robot_ip is not None else True,
            RobotStatu.status == do.status if do.status is not None else True,
            RobotStatu.current_task_id == do.current_task_id if do.current_task_id is not None else True,
            RobotStatu.created_id == do.created_id if do.created_id is not None else True,
            RobotStatu.modify_id == do.modify_id if do.modify_id is not None else True,
            RobotStatu.is_active == do.is_active if do.is_active is not None else True
            )
        if len(sort_conditions) > 0:
            query = query.order_by(*sort_conditions)
        query = query.limit(page_size).offset((page - 1) * page_size)

        # 返回结果
        return query.all()
    
    @db_session
    def select_count(session,do:RobotStatu) -> int:
        query = session.query(RobotStatu).filter(
            RobotStatu.id == do.id if do.id is not None else True,
            RobotStatu.robot_code.contains(do.robot_code) if do.robot_code is not None else True,
            RobotStatu.robot_ip.contains(do.robot_ip) if do.robot_ip is not None else True,
            RobotStatu.status == do.status if do.status is not None else True,
            RobotStatu.current_task_id == do.current_task_id if do.current_task_id is not None else True,
            RobotStatu.created_id == do.created_id if do.created_id is not None else True,
            RobotStatu.modify_id == do.modify_id if do.modify_id is not None else True,
            RobotStatu.is_active == do.is_active if do.is_active is not None else True
            )
        return query.count()
    
    @db_session
    def get_robot_statu_by_task_id(session, task_id:int) -> RobotStatu:
        return session.query(RobotStatu).filter(RobotStatu.current_task_id == task_id).first()
    