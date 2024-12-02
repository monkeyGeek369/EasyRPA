from flask import Blueprint
from easyrpa.tools import str_tools,logs_tool,number_tool
from easyrpa.tools.request_tool import easyrpa_request_wrapper
from easyrpa.models.easy_rpa_exception import EasyRpaException
from easyrpa.enums.easy_rpa_exception_code_enum import EasyRpaExceptionCodeEnum
from easyrpa.tools.json_tools import JsonTool
from easyrpa.models.agent_models.heartbeat_check_req_dto import HeartbeatCheckReqDTO
from easyrpa.models.agent_models.robot_log_report_req_dto import RobotLogReportReqDTO


robot_api_bp =  Blueprint('robot_api',__name__)

@robot_api_bp.route('/robot/heartbeat', methods=['POST'])
@easyrpa_request_wrapper
def heartbeat_check(dto:HeartbeatCheckReqDTO) -> bool:
    pass

@robot_api_bp.route('/robot/delete', methods=['POST'])
@easyrpa_request_wrapper
def delete_robot(id:int) -> bool:
    pass

@robot_api_bp.route('/robot/log/report', methods=['POST'])
@easyrpa_request_wrapper
def robot_log_report(dto:RobotLogReportReqDTO) -> bool:
    pass