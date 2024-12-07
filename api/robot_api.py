from flask import Blueprint
from easyrpa.tools import str_tools,logs_tool,number_tool
from easyrpa.tools.request_tool import easyrpa_request_wrapper
from easyrpa.models.easy_rpa_exception import EasyRpaException
from easyrpa.enums.easy_rpa_exception_code_enum import EasyRpaExceptionCodeEnum
from easyrpa.tools.json_tools import JsonTool
from easyrpa.models.agent_models.heartbeat_check_req_dto import HeartbeatCheckReqDTO
from easyrpa.models.agent_models.robot_log_report_req_dto import RobotLogReportReqDTO
from core import robot_manager_core
from easyrpa.enums.robot_status_type_enum import RobotStatusTypeEnum


robot_api_bp =  Blueprint('robot_api',__name__)

@robot_api_bp.route('/robot/heartbeat', methods=['POST'])
@easyrpa_request_wrapper
def heartbeat_check(dto:HeartbeatCheckReqDTO) -> bool:
    if str_tools.str_is_empty(dto.get("robot_code")):
        raise EasyRpaException("robot code is empty",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,dto)

    # search robot by robot code
    search_res = robot_manager_core.get_robot_by_code(robot_code=dto.get("robot_code"))

    if search_res is None:
        # insert robot
        robot_manager_core.create_robot(robot_code=dto.get("robot_code"),robot_ip=dto.get("robot_ip"),
                                        port=dto.get("port"),current_task_id=dto.get("task_id"))
    else:
        # update robot
        robot_manager_core.update_robot(robot_id=search_res.id,robot_code=dto.get("robot_code"),robot_ip=dto.get("robot_ip"),
                                        port=dto.get("port"),current_task_id=dto.get("task_id"))

    return True

@robot_api_bp.route('/robot/delete', methods=['POST'])
@easyrpa_request_wrapper
def delete_robot(id:int) -> bool:
    # delete robot and robot log
    robot_manager_core.delete_robot(id=id)
    return True

@robot_api_bp.route('/robot/log/report', methods=['POST'])
@easyrpa_request_wrapper
def robot_log_report(dto:RobotLogReportReqDTO) -> bool:
    # base check
    if str_tools.str_is_empty(dto.robot_code):
        raise EasyRpaException("robot code is empty",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,dto)
    if number_tool.num_is_empty(dto.log_type):
        raise EasyRpaException("log type is empty",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,dto)

    # search robot by robot code
    robot = robot_manager_core.get_robot_by_code(robot_code=dto.robot_code)
    if robot is None:
        raise EasyRpaException("robot not found",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,dto)

    # update robot task
    if number_tool.num_is_not_empty(dto.task_id) and robot.current_task_id != dto.task_id:
        robot.current_task_id = dto.task_id
        robot.status = RobotStatusTypeEnum.RUNNING.value[1]

    # insert robot log
    robot_manager_core.add_robot_log(robot_id=robot.id,task_id=dto.task_id,log_type=dto.log_type,message=dto.message)
    return True