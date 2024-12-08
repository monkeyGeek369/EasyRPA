from models.robot.robot_detail_model import RobotDetailModel
from models.robot.robot_log_detail_model import RobotLogDetailModel
from database.models import RobotStatu,RobotLog
from easyrpa.enums.robot_status_type_enum import RobotStatusTypeEnum
from easyrpa.enums.sys_log_type_enum import SysLogTypeEnum

def robot2RobotDetailModel(dto:RobotStatu) -> RobotDetailModel:
    # copy
    detail = RobotDetailModel(
        id=dto.id,
        robot_code=dto.robot_code,
        robot_ip=dto.robot_ip,
        status=dto.status,
        status_name=RobotStatusTypeEnum.get_by_id(dto.status).value[2],
        port=dto.port,
        current_task_id=dto.current_task_id,
        created_id=dto.created_id,
        created_time=dto.created_time,
        modify_id=dto.modify_id,
        modify_time=dto.modify_time,
        trace_id=dto.trace_id,
        is_active=dto.is_active
    )

    return detail

def robots2RobotDetailModels(dtos:list[RobotStatu]) -> list[RobotDetailModel]:
    return [robot2RobotDetailModel(item) for item in dtos]

def robotLog2RobotLogDetailModel(dto:RobotLog) -> RobotLogDetailModel:
    # copy
    detail = RobotLogDetailModel(
        id=dto.id,
        robot_id=dto.robot_id,
        task_id=dto.task_id,
        log_type=dto.log_type,
        log_type_name=SysLogTypeEnum.get_by_id(dto.log_type).value[2],
        message=dto.message,
        created_id=dto.created_id,
        created_time=dto.created_time,
        modify_id=dto.modify_id,
        modify_time=dto.modify_time,
        trace_id=dto.trace_id,
        is_active=dto.is_active
    )

    return detail

def robotLogs2RobotLogDetailModels(dtos:list[RobotLog]) -> list[RobotLogDetailModel]:
    return [robotLog2RobotLogDetailModel(item) for item in dtos]
