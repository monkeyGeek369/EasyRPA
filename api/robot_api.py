from flask import Blueprint
from easyrpa.tools import str_tools,number_tool
from easyrpa.tools.request_tool import easyrpa_request_wrapper
from easyrpa.models.easy_rpa_exception import EasyRpaException
from easyrpa.enums.easy_rpa_exception_code_enum import EasyRpaExceptionCodeEnum
from easyrpa.tools.json_tools import JsonTool
from easyrpa.models.agent_models.heartbeat_check_req_dto import HeartbeatCheckReqDTO
from easyrpa.models.agent_models.robot_log_report_req_dto import RobotLogReportReqDTO
from core import robot_manager_core
from easyrpa.enums.robot_status_type_enum import RobotStatusTypeEnum
from easyrpa.enums.sys_log_type_enum import SysLogTypeEnum
from models.robot.robot_search_req_model import RobotSearchReqModel
from models.robot.robot_search_res_model import RobotSearchResModel
from models.robot.robot_log_search_req_model import RobotLogSearchReqModel
from models.robot.robot_log_search_res_model import RobotLogSearchResModel
from database.models import RobotStatu,RobotLog
from models.base.meta_data_base_model import MetaDataBaseModel


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
def delete_robot(code:str) -> bool:
    # delete robot and robot log
    robot_manager_core.delete_robot(robot_code=code)
    return True

@robot_api_bp.route('/robot/log/report', methods=['POST'])
@easyrpa_request_wrapper
def robot_log_report(dto:RobotLogReportReqDTO) -> bool:
    # base check
    if str_tools.str_is_empty(dto.get("robot_code")):
        raise EasyRpaException("robot code is empty",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,dto)
    if number_tool.num_is_empty(dto.get("log_type")):
        raise EasyRpaException("log type is empty",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,dto)

    # search robot by robot code
    robot = robot_manager_core.get_robot_by_code(robot_code=dto.get("robot_code"))
    if robot is None:
        raise EasyRpaException("robot not found",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,dto)

    # update robot task
    if number_tool.num_is_not_empty(dto.get("task_id")) and robot.current_task_id != dto.get("task_id"):
        robot.current_task_id = dto.get("task_id")
        robot.status = RobotStatusTypeEnum.RUNNING.value[1]

    # insert robot log
    robot_manager_core.add_robot_log(robot_id=robot.id,task_id=dto.get("task_id"),log_type=dto.get("log_type"),message=dto.get("message"))
    return True

@robot_api_bp.route('/robot/search/robots', methods=['POST'])
@easyrpa_request_wrapper
def search_robots(dto:RobotSearchReqModel) -> RobotSearchResModel:
    # base check
    if number_tool.num_is_empty(dto.get("page")):
        raise EasyRpaException("search page is empty",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,dto)
    if number_tool.num_is_empty(dto.get("page_size")):
        raise EasyRpaException("search page size is empty",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,dto)
    
    # dto to do
    obj = RobotStatu()
    obj.robot_code = dto.get("robot_code")
    obj.robot_ip = dto.get("robot_ip")
    obj.status = dto.get("status")
    obj.current_task_id = dto.get("current_task_id")

    # search from db
    search_result = robot_manager_core.search_robots_by_params(do=obj,page=dto.get("page"),page_size=dto.get("page_size"),sorts=dto.get("sorts"))
    
    # search count
    total = robot_manager_core.search_robot_count_by_params(do=obj)

    # return
    result = RobotSearchResModel(
        total=total,
        data=search_result,
        sorts=dto.get("sorts")
    )

    return JsonTool.any_to_dict(result)

@robot_api_bp.route('/robot/search/logs', methods=['POST'])
@easyrpa_request_wrapper
def search_robot_logs(dto:RobotLogSearchReqModel) -> RobotLogSearchResModel:
    # base check
    if number_tool.num_is_empty(dto.get("page")):
        raise EasyRpaException("search page is empty",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,dto)
    if number_tool.num_is_empty(dto.get("page_size")):
        raise EasyRpaException("search page size is empty",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,dto)
    
    # dto to do
    obj = RobotLog()
    obj.robot_id = dto.get("robot_id")
    obj.task_id = dto.get("task_id")
    obj.log_type = dto.get("log_type")

    # search from db
    search_result = robot_manager_core.search_robot_logs_by_params(do=obj,page=dto.get("page"),page_size=dto.get("page_size"),sorts=dto.get("sorts"))
    
    # search count
    total = robot_manager_core.search_robot_log_count_by_params(do=obj)

    # return
    result = RobotLogSearchResModel(
        total=total,
        data=search_result,
        sorts=dto.get("sorts")
    )

    return JsonTool.any_to_dict(result)

@robot_api_bp.route('/robot/delete/logs', methods=['POST'])
@easyrpa_request_wrapper
def delete_robot_log(robot_id:int) -> bool:
    robot_manager_core.delete_robot_log(robot_id=robot_id)
    return True

@robot_api_bp.route('/robot/status', methods=['POST'])
@easyrpa_request_wrapper
def get_all_robot_status(dto) ->list[MetaDataBaseModel]:
    results = []
    results.append(MetaDataBaseModel(id=RobotStatusTypeEnum.CLOSED.value[1],des=RobotStatusTypeEnum.CLOSED.value[2]))
    results.append(MetaDataBaseModel(id=RobotStatusTypeEnum.LEISURE.value[1],des=RobotStatusTypeEnum.LEISURE.value[2]))
    results.append(MetaDataBaseModel(id=RobotStatusTypeEnum.RUNNING.value[1],des=RobotStatusTypeEnum.RUNNING.value[2]))
    return JsonTool.any_to_dict(results)

@robot_api_bp.route('/sys/log/types', methods=['POST'])
@easyrpa_request_wrapper
def get_all_sys_log_types(dto) -> list[MetaDataBaseModel]:
    results = []
    results.append(MetaDataBaseModel(id=SysLogTypeEnum.INFO.value[1],des=SysLogTypeEnum.INFO.value[2]))
    results.append(MetaDataBaseModel(id=SysLogTypeEnum.WARN.value[1],des=SysLogTypeEnum.WARN.value[2]))
    results.append(MetaDataBaseModel(id=SysLogTypeEnum.DEBUG.value[1],des=SysLogTypeEnum.DEBUG.value[2]))
    results.append(MetaDataBaseModel(id=SysLogTypeEnum.BIZ.value[1],des=SysLogTypeEnum.BIZ.value[2]))
    return JsonTool.any_to_dict(results)
