from database.robot_statu_db_manager import RobotStatuDBManager
from database.robot_log_db_manager import RobotLogDBManager
from database.models import RobotStatu,RobotLog
from easyrpa.enums.robot_status_type_enum import RobotStatusTypeEnum
from easyrpa.tools import number_tool,local_store_tools,str_tools,request_tool
from easyrpa.models.base.sort_base_model import SortBaseModel
from models.robot.robot_detail_model import RobotDetailModel
from models.robot.robot_log_detail_model import RobotLogDetailModel
from easyrpa.tools.json_tools import JsonTool
from easyrpa.tools.common_tools import CommonTools
from transfer import robot_transfer
from easyrpa.models.easy_rpa_exception import EasyRpaException
from easyrpa.enums.easy_rpa_exception_code_enum import EasyRpaExceptionCodeEnum
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
    robot = RobotStatuDBManager.search_robot_statu_by_code(robot_code=robot_code)
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

def closed_robot_check(params):
    while True:
        import time
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
                req_json = request_tool.request_base_model_json_builder("test")
                response = requests.get(url,json=req_json)
                if response is None:
                    is_closed = True
                else:
                    result = JsonTool.any_to_dict(response.text)
                    if result.get("code") != 200:
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

def search_robots_by_params(do:RobotStatu,page: int,page_size: int,sorts: list[SortBaseModel]) -> list[RobotDetailModel]:
    # search db
    db_result = RobotStatuDBManager.select_page_list(do=do,
                                               page=CommonTools.initPage(page=page),
                                               page_size=CommonTools.initPageSize(pageSize=page_size),
                                               sorts=CommonTools.initSorts(sorts=sorts)) 
    result = robot_transfer.robots2RobotDetailModels(db_result)
    return result

def search_robot_count_by_params(do:RobotStatu) -> int:
    return RobotStatuDBManager.select_count(do=do)

def search_robot_logs_by_params(do:RobotLog,page: int,page_size: int,sorts: list[SortBaseModel]) -> list[RobotLogDetailModel]:
    # search db
    db_result = RobotLogDBManager.select_page_list(do=do,
                                               page=CommonTools.initPage(page=page),
                                               page_size=CommonTools.initPageSize(pageSize=page_size),
                                               sorts=CommonTools.initSorts(sorts=sorts)) 
    result = robot_transfer.robotLogs2RobotLogDetailModels(db_result)
    return result

def search_robot_log_count_by_params(do:RobotLog) -> int:
    return RobotLogDBManager.select_count(do=do)

def delete_robot_log(robot_id:int) -> bool:
    if number_tool.num_is_empty(robot_id):
        raise EasyRpaException("robot id is empty",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,robot_id)
    
    return RobotLogDBManager.delete_robot_log_by_robot_id(robot_id=robot_id)

def release_robot(robot_code:str) -> bool:
    if str_tools.str_is_empty(robot_code):
        raise EasyRpaException("robot code is empty",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,robot_code)
    
    robot = get_robot_by_code(robot_code=robot_code)

    if robot is None:
        return False
    
    # update robot
    robot.status = RobotStatusTypeEnum.CLOSED.value[1]
    robot.current_task_id = None
    RobotStatuDBManager.update_robot_statu(data=robot)

    # request agent
    url = f"http://{robot.robot_ip}:{robot.port}/release/agent"
    req_json = request_tool.request_base_model_json_builder("release")
    requests.get(url,json=req_json)
    
    return True