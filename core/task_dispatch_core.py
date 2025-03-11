from database.models import FlowTask,Flow,FlowTaskLog,DispatchHandlerData,DispatchRecord
from easyrpa.models.agent_models.flow_task_exe_req_dto import FlowTaskExeReqDTO
import requests,random,datetime,threading
from database.flow_task_db_manager import FlowTaskDBManager
from database.flow_task_log_db_manager import FlowTaskLogDBManager
from database.flow_db_manager import FlowDbManager
from easyrpa.enums.flow_task_status_enum import FlowTaskStatusEnum
from easyrpa.enums.log_type_enum import LogTypeEnum
from easyrpa.tools import request_tool,str_tools,local_store_tools,number_tool,blake3_tool
from database.robot_statu_db_manager import RobotStatuDBManager
from easyrpa.models.easy_rpa_exception import EasyRpaException
from easyrpa.enums.easy_rpa_exception_code_enum import EasyRpaExceptionCodeEnum
from core import robot_manager_core,task_manager_core,flow_manager_core
from easyrpa.enums.robot_status_type_enum import RobotStatusTypeEnum
from easyrpa.tools.json_tools import JsonTool
from database.dispatch_handler_data_db_manager import DispatchHandlerDataDBManager
from easyrpa.enums.job_status_enum import JobStatusEnum
from database.dispatch_record_db_manager import DispatchRecordDBManager

# local obj
thread_lock_robot_lock = threading.RLock()
thread_lock_robot_unlock = threading.RLock()

def flow_task_dispatch(flow:Flow,flow_task:FlowTask) -> bool:
     is_dispatch_success = False
     is_this_lock = False

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
        
        is_this_lock = robot_lock(robot_code=leisure_robot.robot_code)
        if not is_this_lock:
            return is_dispatch_success
        else:
            # update robot
            leisure_robot.status = RobotStatusTypeEnum.RUNNING.value[1]
            leisure_robot.current_task_id = flow_task.id
            robot_manager_core.update_robot(robot_id=leisure_robot.id,robot_code=leisure_robot.robot_code,robot_ip=leisure_robot.robot_ip,port=leisure_robot.port,current_task_id=flow_task.id)
            
        # dispatch success when have robot
        is_dispatch_success = True
        
        # update retry number
        new_task_retry_number = (flow_task.retry_number if flow_task.retry_number is not None else 0)
        new_task_retry_number = new_task_retry_number + 1
        update_task_retry = FlowTask(id=flow_task.id,retry_number=new_task_retry_number)
        FlowTaskDBManager.update_flow_task(update_task_retry)
        FlowTaskLogDBManager.create_flow_task_log(FlowTaskLog(task_id=flow_task.id,log_type=LogTypeEnum.TXT.value[1],message=f"dispatch success , current exe number is {new_task_retry_number} "))

        # get script hash
        hash_tools = blake3_tool.Blake3Tool(salt=flow.flow_code,key="script_exe")
        script_hash = hash_tools.hash(data=flow.flow_exe_script)
        if str_tools.str_is_empty(script_hash):
            raise EasyRpaException("flow exe script hash generate error",EasyRpaExceptionCodeEnum.EXECUTE_ERROR.value[1],None,flow.flow_code)

        # build params
        flow_task_exe_req_dto = FlowTaskExeReqDTO(task_id=flow_task.id
                                                  ,site_id=flow_task.site_id
                                                  ,flow_id=flow_task.flow_id
                                                  ,flow_code=flow.flow_code
                                                  ,flow_name=flow.flow_name
                                                  ,flow_rpa_type=flow.flow_rpa_type
                                                  ,flow_standard_message=flow_task.flow_standard_message
                                                  ,script_hash=script_hash
                                                  ,sub_source=flow_task.sub_source
                                                  ,max_exe_time=flow.max_exe_time)
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
        if leisure_robot is not None and is_this_lock:
            robot_unlock(robot_code=leisure_robot.robot_code)
    
     return is_dispatch_success
     
def robot_lock(robot_code:str) -> bool:
    with thread_lock_robot_lock:
        if str_tools.str_is_empty(robot_code):
            raise EasyRpaException("robot code is empty",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,robot_code)
        
        locked_robots = local_store_tools.get_data(key="locked_robots")

        if locked_robots is None:
            local_store_tools.add_data(key="locked_robots",value = [robot_code])
            return True
        else:
            if robot_code not in locked_robots:
                locked_robots.append(robot_code)
                local_store_tools.update_data(key="locked_robots",value = locked_robots)
                return True
            else:
                return False

def robot_unlock(robot_code:str):
    with thread_lock_robot_unlock:
        if str_tools.str_is_empty(robot_code):
            raise EasyRpaException("robot code is empty",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,robot_code)
        
        locked_robots = local_store_tools.get_data(key="locked_robots")

        if locked_robots is not None:
            if robot_code in locked_robots:
                locked_robots.remove(robot_code)
                local_store_tools.update_data(key="locked_robots",value = locked_robots)

def check_waiting_task(params):
    while True:
        # get all waiting tasks
        waiting_tasks = task_manager_core.search_waiting_tasks()
        if waiting_tasks is not None and len(waiting_tasks) > 0:
            for waiting_task in waiting_tasks:
                task_retry(waiting_task)
        
        # get all execution tasks
        execution_tasks = task_manager_core.search_execution_tasks()
        if execution_tasks is not None and len(execution_tasks) > 0:
            for execution_task in execution_tasks:
                task_retry(execution_task)

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
        if number_tool.num_is_empty(flow.max_exe_time):
            raise EasyRpaException("flow max exe time is empty",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,task.result_code)
        if number_tool.num_is_empty(flow.max_retry_number):
            raise EasyRpaException("flow max retry number is empty",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,task.result_code)
        
        # max retry number
        if number_tool.num_is_not_empty(task.retry_number) and task.retry_number >= flow.max_retry_number:
            raise EasyRpaException("task retry number is over max retry number",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,task.result_code)

        # max waiting time , default 24 hours
        current_time = int(datetime.datetime.now().timestamp())
        created_time = int(task.created_time.timestamp())
        time_span = current_time - created_time
        if time_span > (24 * 60 * 60):
            raise EasyRpaException("task exe time is over max wait time(24 hours)",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,task.result_code)

        # executing task handler
        if task.status == FlowTaskStatusEnum.EXECUTION.value[1]:
            return

        # retry code
        if str_tools.str_is_empty(flow.retry_code):
            raise EasyRpaException("flow retry code is empty, can not retry",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,task.result_code)
        retry_codes = flow.retry_code.split(",")
        if number_tool.num_is_not_empty(task.result_code) and str(task.result_code) not in retry_codes:
            raise EasyRpaException("retry code not config, can not retry",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,task.result_code)

        # dispatch task
        result = flow_task_dispatch(flow=flow,flow_task=task)

        # update task
        update_flow_task = None
        if not result:
            update_flow_task = FlowTask(id=task.id,status=FlowTaskStatusEnum.WAIT_EXE.value[1])
        
        if update_flow_task is not None:
            FlowTaskDBManager.update_flow_task(update_flow_task)
    except Exception as e:
        update_flow_task = FlowTask(id=task.id,status=FlowTaskStatusEnum.FAIL.value[1])
        FlowTaskDBManager.update_flow_task(update_flow_task)
        FlowTaskLogDBManager.create_flow_task_log(FlowTaskLog(task_id=task.id,log_type=LogTypeEnum.TXT.value[1],message="task retry error , message: " + str(e)))

        if task.biz_no is not None:
            record = DispatchRecordDBManager.get_dispatch_record_by_id(id=int(task.biz_no))
            
            if record is not None:
                # update job record
                up_record = DispatchRecord(id=record.id,
                                        status=JobStatusEnum.DISPATCH_FAIL.value[1],
                                        result_message=str(e))
                DispatchRecordDBManager.update_dispatch_record(data=up_record)
                # update handler data
                if record.handler_data_id is not None:
                    DispatchHandlerDataDBManager.update_dispatch_handler_data(data=DispatchHandlerData(id=record.handler_data_id,status=JobStatusEnum.DISPATCH_FAIL.value[1]))

        # get next waiting task
        waiting_tasks = task_manager_core.search_waiting_tasks()
        if waiting_tasks is not None and len(waiting_tasks) > 0:
            task_retry(task=waiting_tasks[0])
        