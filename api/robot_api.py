from flask import Blueprint
from easyrpa.tools import str_tools,logs_tool,number_tool
from easyrpa.tools.request_tool import easyrpa_request_wrapper
from easyrpa.models.easy_rpa_exception import EasyRpaException
from easyrpa.enums.easy_rpa_exception_code_enum import EasyRpaExceptionCodeEnum
from easyrpa.tools.json_tools import JsonTool
from easyrpa.models.agent_models.heartbeat_check_req_dto import HeartbeatCheckReqDTO
from easyrpa.models.agent_models.robot_log_report_req_dto import RobotLogReportReqDTO
from core import robot_manager_core


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
    pass

@robot_api_bp.route('/robot/log/report', methods=['POST'])
@easyrpa_request_wrapper
def robot_log_report(dto:RobotLogReportReqDTO) -> bool:
    pass