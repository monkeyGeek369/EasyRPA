from easyrpa.models.flow.flow_task_subscribe_result_dto import FlowTaskSubscribeResultDTO
from easyrpa.models.flow.flow_task_subscribe_dto import FlowTaskSubscribeDTO
import check.flow_task_subscribe_dto_check as sub_check
from easyrpa.tools import request_tool
from database.flow_db_manager import FlowDbManager
from easyrpa.models.easy_rpa_exception import EasyRpaException
from easyrpa.enums.easy_rpa_exception_code_enum import EasyRpaExceptionCodeEnum
from database.flow_configuration_db_manager import FlowConfigurationDBManager
from database.models import FlowTask
from core.script_exe_core import *
from database.flow_task_db_manager import FlowTaskDBManager
from easyrpa.enums.flow_task_status_enum import FlowTaskStatusEnum
import json
from core.task_dispatch import flow_task_dispatch

def flow_task_subscribe(dto:FlowTaskSubscribeDTO)-> FlowTaskSubscribeResultDTO:
    flow_task = FlowTask()
    try:
        # 参数校验
        sub_check.flow_task_subscribe_dto_check(dto)

        # 获取当前用户
        header = request_tool.get_current_header()

        # 查询流程
        flow = FlowDbManager.get_flow_by_id(dto.flow_id)
        if not flow:
            raise EasyRpaException("""flow {} not found""".format(dto.flow_id),EasyRpaExceptionCodeEnum.DATA_NOT_FOUND.code,None,dto)

        # 查询流程配置
        flow_configuration = FlowConfigurationDBManager.get_flow_configuration_by_id(dto.flow_configuration_id)
        if not flow_configuration:
            raise EasyRpaException("""flow configuration {} not found""".format(dto.flow_configuration_id),EasyRpaExceptionCodeEnum.DATA_NOT_FOUND.code,None,dto)
        
        # 执行校验脚本
        request_check_script_exe("playwright",dto.request_standard_message,flow_configuration.check_script,dto.sub_source)

        # 执行适配脚本-获取流程报文字典
        dict_adapter_result = request_adapter_script_exe("playwright",dto.request_standard_message,flow_configuration.adapter_script,dto.sub_source)

        # 创建流程任务
        flow_task.flow_id = dto.flow_id
        flow_task.site_id = flow.site_id
        flow_task.biz_no = dto.biz_no
        flow_task.sub_source = dto.sub_source
        flow_task.status = FlowTaskStatusEnum.WAIT_EXE.code
        flow_task.request_standard_message = dto.request_standard_message
        flow_task.flow_standard_message = json.dumps(dict_adapter_result)
        FlowTaskDBManager.create_flow_task(flow_task)

        # 流程任务分发
        flow_task_dispatch(flow,flow_task)

        # 返回结果
        return FlowTaskSubscribeResultDTO(flow_task.id,True,"流程任务创建成功")
    except Exception as e:
        return FlowTaskSubscribeResultDTO(flow_task.id,False,str(e))