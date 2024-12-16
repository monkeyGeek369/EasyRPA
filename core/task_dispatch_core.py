from database.models import FlowTask,Flow,FlowTaskLog
from easyrpa.models.agent_models.flow_task_exe_req_dto import FlowTaskExeReqDTO
import requests,random,datetime,pytz
from database.flow_task_db_manager import FlowTaskDBManager
from database.flow_task_log_db_manager import FlowTaskLogDBManager
from database.flow_db_manager import FlowDbManager
from easyrpa.enums.flow_task_status_enum import FlowTaskStatusEnum
from easyrpa.enums.log_type_enum import LogTypeEnum
from easyrpa.tools import request_tool,str_tools,local_store_tools,number_tool
from database.robot_statu_db_manager import RobotStatuDBManager
from easyrpa.models.easy_rpa_exception import EasyRpaException
from easyrpa.enums.easy_rpa_exception_code_enum import EasyRpaExceptionCodeEnum
from core import robot_manager_core,task_manager_core,flow_manager_core
from easyrpa.enums.robot_status_type_enum import RobotStatusTypeEnum
from easyrpa.tools.json_tools import JsonTool


def flow_task_dispatch(flow:Flow,flow_task:FlowTask,flow_exe_env:str) -> bool:
     is_dispatch_success = False

     try:
        # get leisure robot
        leisure_robot = None
        robots = RobotStatuDBManager.get_leisure_robot_statu()
        if robots is None or len(robots) == 0:
            return is_dispatch_success
        elif len(robots) == 1:
            leisure_robot = robots[0]
        else:
            # get random robot
            random_index = random.uniform(0, len(robots) - 1)
            leisure_robot = robots[int(random_index)]
        
        if robot_is_lock(robot_code=leisure_robot.robot_code):
            return is_dispatch_success
        else:
            robot_lock(robot_code=leisure_robot.robot_code)
            # update robot
            leisure_robot.status = RobotStatusTypeEnum.RUNNING.value[1]
            leisure_robot.current_task_id = flow_task.id
            robot_manager_core.update_robot(robot_id=leisure_robot.id,robot_code=leisure_robot.robot_code,robot_ip=leisure_robot.robot_ip,port=leisure_robot.port,current_task_id=flow_task.id)
            
        # build params
        flow_task_exe_req_dto = FlowTaskExeReqDTO(task_id=flow_task.id
                                                  ,site_id=flow_task.site_id
                                                  ,flow_id=flow_task.flow_id
                                                  ,flow_code=flow.flow_code
                                                  ,flow_name=flow.flow_name
                                                  ,flow_rpa_type=flow.flow_rpa_type
                                                  ,flow_exe_env=flow_exe_env
                                                  ,flow_standard_message=flow_task.flow_standard_message
                                                  ,flow_exe_script=flow.flow_exe_script
                                                  ,sub_source=flow_task.sub_source)
        # build url
        url = f"http://{leisure_robot.robot_ip}:{leisure_robot.port}/flow/task/async/exe"

        # add task log
        req_json = request_tool.request_base_model_json_builder(flow_task_exe_req_dto)
        if flow_task.retry_number is None or flow_task.retry_number <= 0:
            FlowTaskLogDBManager.create_flow_task_log(FlowTaskLog(task_id=flow_task.id,log_type=LogTypeEnum.TXT.value[1],message=f"adapt script message:{req_json}。"))
        
        # send request
        response = requests.post(url, json=req_json)
        is_success = False
        if response is not None and response.status_code == 200:
            result_txt = JsonTool.any_to_dict(response.text)
            if result_txt.get("code") == 200 and result_txt.get("data") == True:
                is_success = True
        
        # response handler
        if is_success:
            # update task status
            update_flow_task = FlowTask(id=flow_task.id,status=FlowTaskStatusEnum.EXECUTION.value[1])
            FlowTaskDBManager.update_flow_task(update_flow_task)

            # add task log
            FlowTaskLogDBManager.create_flow_task_log(FlowTaskLog(task_id=flow_task.id,log_type=LogTypeEnum.TXT.value[1],message=f"task dispatch success, sended to robot[{url}]。"))
            
            is_dispatch_success = True
        else:
            # update task status
            update_flow_task = FlowTask(id=flow_task.id,status=FlowTaskStatusEnum.WAIT_EXE.value[1])
            FlowTaskDBManager.update_flow_task(update_flow_task)

            # add task log
            FlowTaskLogDBManager.create_flow_task_log(FlowTaskLog(task_id=flow_task.id,log_type=LogTypeEnum.TXT.value[1],message=f"task dispatch error,robot[{url}] is busy。"))
     except Exception as e:
            # update task status error
            update_flow_task = FlowTask(id=flow_task.id,status=FlowTaskStatusEnum.FAIL.value[1])
            FlowTaskDBManager.update_flow_task(update_flow_task)

            # add task error log
            FlowTaskLogDBManager.create_flow_task_log(FlowTaskLog(task_id=flow_task.id,log_type=LogTypeEnum.TXT.value[1],message="task dispatch error,message:" + str(e)))

     finally:
        if leisure_robot is not None:
            robot_unlock(robot_code=leisure_robot.robot_code)
    
     return is_dispatch_success
     
def robot_lock(robot_code:str):
    if str_tools.str_is_empty(robot_code):
        raise EasyRpaException("robot code is empty",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,robot_code)
    
    locked_robots = local_store_tools.get_data(key="locked_robots")

    if locked_robots is None:
        local_store_tools.add_data(key="locked_robots",value = [robot_code])
    else:
        if robot_code not in locked_robots:
            locked_robots.append(robot_code)
            local_store_tools.update_data(key="locked_robots",value = locked_robots)

def robot_unlock(robot_code:str):
    if str_tools.str_is_empty(robot_code):
        raise EasyRpaException("robot code is empty",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,robot_code)
    
    locked_robots = local_store_tools.get_data(key="locked_robots")

    if locked_robots is not None:
        if robot_code in locked_robots:
            locked_robots.remove(robot_code)
            local_store_tools.update_data(key="locked_robots",value = locked_robots)

def robot_is_lock(robot_code:str) -> bool:
    if str_tools.str_is_empty(robot_code):
        raise EasyRpaException("robot code is empty",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,robot_code)
    
    locked_robots = local_store_tools.get_data(key="locked_robots")

    if locked_robots is not None:
        if robot_code in locked_robots:
            return True
    return False

def check_waiting_task(params):
    while True:
        # get all waiting tasks
        waiting_tasks = task_manager_core.search_waiting_tasks()
        if waiting_tasks is None or len(waiting_tasks) == 0:
            continue
        else:
            for waiting_task in waiting_tasks:
                task_retry(waiting_task)
        
        import time
        # wait one minutes
        time.sleep(60)


def task_retry(task:FlowTask):
    try:
        # base check
        if number_tool.num_is_empty(task.flow_id):
            raise EasyRpaException("flow id is empty",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,task.flow_id)

        # task status
        if task.status == FlowTaskStatusEnum.SUCCESS.value[1]:
            return

        # search flow
        flow = FlowDbManager.get_flow_by_id(flow_id=task.flow_id)
        if flow is None:
            raise EasyRpaException("flow not found",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,task.flow_id)
        
        # retry code
        if str_tools.str_is_empty(flow.retry_code):
            raise EasyRpaException("flow retry code is empty, can not retry",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,task.result_code)
        retry_codes = flow.retry_code.split(",")
        if number_tool.num_is_not_empty(task.result_code) and str(task.result_code) not in retry_codes:
            raise EasyRpaException("retry code not config, can not retry",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,task.result_code)

        # max retry number
        if number_tool.num_is_empty(flow.max_retry_number):
            raise EasyRpaException("flow max retry number is empty",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,task.result_code)
        if number_tool.num_is_not_empty(task.retry_number) and task.retry_number >= flow.max_retry_number:
            raise EasyRpaException("task retry number is over max retry number",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,task.result_code)

        # max retry time
        if number_tool.num_is_empty(flow.max_exe_time):
            raise EasyRpaException("flow max exe time is empty",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,task.result_code)
        current_time = int(datetime.datetime.now().timestamp())
        created_time = int(task.created_time.timestamp())
        time_span = current_time - created_time
        if time_span > (flow.max_exe_time * 1000):
            raise EasyRpaException("task exe time is over max exe time",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,task.result_code)

        # search flow exe env
        rpa_exe_env = flow_manager_core.get_flow_exe_env_meta_data(flow_exe_env=flow.flow_exe_env)
        if rpa_exe_env is None or str_tools.str_is_empty(rpa_exe_env.name_en):
            raise EasyRpaException("flow exe env not found",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,task.result_code)

        # dispatch task
        result = flow_task_dispatch(flow=flow,flow_task=task,flow_exe_env=rpa_exe_env.name_en)

        # update task
        if result:
            update_flow_task = FlowTask(id=task.id,retry_number=(task.retry_number if task.retry_number is not None else 0)+1)
        else:
            update_flow_task = FlowTask(id=task.id,retry_number=(task.retry_number if task.retry_number is not None else 0)+1,status=FlowTaskStatusEnum.WAIT_EXE.value[1])
        FlowTaskDBManager.update_flow_task(update_flow_task)
    except Exception as e:
        update_flow_task = FlowTask(id=task.id,status=FlowTaskStatusEnum.FAIL.value[1])
        FlowTaskDBManager.update_flow_task(update_flow_task)
        FlowTaskLogDBManager.create_flow_task_log(FlowTaskLog(task_id=task.id,log_type=LogTypeEnum.TXT.value[1],message="task retry error , message: " + str(e)))
        