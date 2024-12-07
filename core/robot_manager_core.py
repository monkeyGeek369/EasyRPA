from database.robot_statu_db_manager import RobotStatuDBManager
from database.robot_log_db_manager import RobotLogDBManager
from database.models import RobotStatu,RobotLog
from easyrpa.enums.robot_status_type_enum import RobotStatusTypeEnum
from easyrpa.tools import number_tool,local_store_tools,str_tools
import requests

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
    refresh_robot_store(add_key=robot_code,delete_key=None,value=robot)


def get_robot_by_code(robot_code:str) -> RobotStatu:
    # get robot from local store
    robot = get_robot_from_store(key=robot_code)
    if robot is not None:
        return robot
    robot = RobotStatuDBManager.search_robot_statu_by_code(robot_code==robot_code)
    refresh_robot_store(add_key=robot_code,delete_key=None,value=robot)
    return robot


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
    refresh_robot_store(add_key=robot_code,delete_key=None,value=robot)

def closed_robot_check():
    import time
    while True:
        # wait 10 seconds
        time.sleep(10)

        # get all robots
        robots = RobotStatuDBManager.get_all_robot_statu()
        if robots is None or len(robots) == 0:
            continue

        for robot in robots:
            is_closed = False

            # base info check
            if robot is None:
                is_closed = True
            if robot.robot_code is None:
                is_closed = True
            if robot.robot_ip is None:
                is_closed = True
            if robot.port is None:
                is_closed = True

            # update robot
            refresh_robot_store(add_key=robot.robot_code,delete_key=None,value=robot)

            # health check
            url = f"http://{robot.robot_ip}:{robot.port}/health/test"

            try:
                response = requests.get(url)
                if response is None or response.code != 200:
                    is_closed = True
            except:
                is_closed = True

            if is_closed:
                robot.status = RobotStatusTypeEnum.CLOSED.value[1]
                RobotStatuDBManager.update_robot_statu(data=robot)
                refresh_robot_store(add_key=robot.robot_code,delete_key=None,value=robot)
    
def delete_robot(robot_code:str):
    if str_tools.str_is_empty(robot_code):
        return False
    
    robot = RobotStatuDBManager.search_robot_statu_by_code(robot_code=robot_code)
    if robot is None:
        return False

    id = robot.id
    # delete robot statu
    RobotStatuDBManager.delete_robot_statu(id=id)
    # delete robot log
    RobotLogDBManager.delete_robot_log_by_robot_id(robot_id=id)
    # delete robot from local
    refresh_robot_store(add_key=None,delete_key=robot_code,value=None)

def add_robot_log(robot_id:int,task_id:int,log_type:int,message:str):
    log = RobotLog(
        robot_id=robot_id,
        task_id=task_id,
        log_type=log_type,
        message=message
    )
    RobotLogDBManager.create_robot_log(robot_log=log)

def refresh_robot_store(add_key:str,value,delete_key:str):
    if delete_key is not None:
        local_store_tools.delete_data(key=delete_key)

    if add_key is not None:
        local_store_tools.update_data(key=add_key,value=value)

def get_robot_from_store(key:str) -> RobotStatu:
    return local_store_tools.get_data(key=key)

