from database.robot_statu_db_manager import RobotStatuDBManager
from database.robot_log_db_manager import RobotLogDBManager
from database.models import RobotStatu,RobotLog
from easyrpa.enums.robot_status_type_enum import RobotStatusTypeEnum
from easyrpa.tools import number_tool
import datetime

def create_robot(robot_code:str,robot_ip:str,port:int,current_task_id:int):
    status = RobotStatusTypeEnum.LEISURE.value[1]
    if number_tool.num_is_not_empty(current_task_id):
        status = RobotStatusTypeEnum.RUNNING.value[1]

    robot = RobotStatu(
        robot_code=robot_code,
        robot_ip=robot_ip,
        status=status,
        port=port,
        current_task_id=current_task_id
    )

    RobotStatuDBManager.create_robot_statu(robot_statu=robot)

def get_robot_by_code(robot_code:str) -> RobotStatu:
    return RobotStatuDBManager.search_robot_statu_by_code(robot_code==robot_code)


def update_robot(robot_id:int,robot_code:str,robot_ip:str,port:int,current_task_id:int):
    status = RobotStatusTypeEnum.LEISURE.value[1]
    if number_tool.num_is_not_empty(current_task_id):
        status = RobotStatusTypeEnum.RUNNING.value[1]

    robot = RobotStatu(
        id= robot_id,
        robot_code=robot_code,
        robot_ip=robot_ip,
        status=status,
        port=port,
        current_task_id=current_task_id
    )
    RobotStatuDBManager.update_robot_statu(data=robot)

def closed_robot_check():
    import time
    while True:
        # wait 5 seconds
        time.sleep(10)

        # get all robots
        robots = RobotStatuDBManager.get_all_robot_statu()
        if robots is None or len(robots) == 0:
            continue

        # get current time
        now = int(datetime.datetime.now().timestamp())

        for robot in robots:
            # get update time
            update_time = robot.modify_time
            if update_time is None:
                # update
                RobotStatuDBManager.update_robot_statu(data=robot)
            else:
                update_time_timestamp = int(update_time.timestamp())
                if now - update_time_timestamp > (3*60*1000+30000):
                    robot.status = RobotStatusTypeEnum.CLOSED.value[1]
                    RobotStatuDBManager.update_robot_statu(data=robot)
    

