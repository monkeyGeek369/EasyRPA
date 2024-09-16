from flask import Blueprint
from flask import jsonify,Blueprint,request
from easyrpa.tools import logs_tool
from core.script_exe_core import rpa_result_script_exe
from transfer.flow_task_transfer import request_json_to_FlowTaskExeResDTO
from easyrpa.tools.request_tool import easyrpa_request_wrapper
from easyrpa.models.easy_rpa_exception import EasyRpaException
from easyrpa.enums.easy_rpa_exception_code_enum import EasyRpaExceptionCodeEnum
from check.flow_task_check import flow_task_exe_res_dto_check
from database.flow_db_manager import FlowDbManager
from database.flow_configuration_db_manager import FlowConfigurationDBManager
from database.flow_task_db_manager import FlowTaskDBManager
from database.flow_task_db_manager import FlowTaskLogDBManager
from easyrpa.models.scripty_exe_result import ScriptExeResult
from easyrpa.enums.log_type_enum import LogTypeEnum
import jsonpickle
from database.models import FlowTask,FlowTaskLog
from easyrpa.models.agent_models.flow_task_exe_res_dto import FlowTaskExeResDTO
from easyrpa.tools import str_tools

flow_task_bp =  Blueprint('flow_task',__name__)

@flow_task_bp.route('/flow/task/result/handler', methods=['POST'])
@easyrpa_request_wrapper
def flow_task_result_handler(dto:FlowTaskExeResDTO) -> bool:
    if dto is None:
        raise EasyRpaException("request is empty",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None)

    # 基础校验
    flow_task_exe_res_dto_check(dto)

    # 查询流程任务
    flow_task = FlowTaskDBManager.get_flow_task_by_id(dto.task_id)
    if flow_task is None:
        raise EasyRpaException("""flow task {} not found""".format(dto.task_id),EasyRpaExceptionCodeEnum.DATA_NOT_FOUND.value[1],None,dto)

    # 查询流程
    flow = FlowDbManager.get_flow_by_id(dto.flow_id)
    if flow is None:
        raise EasyRpaException("""flow {} not found""".format(dto.flow_id),EasyRpaExceptionCodeEnum.DATA_NOT_FOUND.value[1],None,dto)
    if str_tools.str_is_empty(flow.request_check_script):
        raise EasyRpaException("""flow {} not found check script""".format(dto.flow_id),EasyRpaExceptionCodeEnum.DATA_NOT_FOUND.value[1],None,dto)
    if str_tools.str_is_empty(flow.request_adapt_script):
        raise EasyRpaException("""flow {} not found adapt script""".format(dto.flow_id),EasyRpaExceptionCodeEnum.DATA_NOT_FOUND.value[1],None,dto)

    # 获取rpa执行结果
    exe_result = ScriptExeResult(status=dto.status
                                 ,print_str=dto.print_str
                                 ,result=dto.result
                                 ,error_msg=dto.error_msg
                                 ,code=dto.code)
    rpa_result_message = jsonpickle.encode(exe_result)

    # 更新任务+记录日志
    FlowTaskDBManager.update_flow_task(FlowTask(id= flow_task.id,task_result_message=rpa_result_message))
    FlowTaskLogDBManager.create_flow_task_log(FlowTaskLog(task_id= flow_task.id
                                                          ,log_type=LogTypeEnum.TASK_RESULT.value[1]
                                                          ,message="""rpa result: {}""".format(rpa_result_message)))

    # 执行返回值脚本
    dict_response_result = rpa_result_script_exe(flow_exe_env="playwright"
                                                 ,rpa_result_message=rpa_result_message
                                                 ,flow_exe_script=flow.flow_result_handle_script
                                                 ,sub_source=dto.sub_source
                                                 ,flow_config=None)
    dict_response_result_json = jsonpickle.encode(dict_response_result)
    
    # 更新任务+记录日志
    FlowTaskDBManager.update_flow_task(FlowTask(id= flow_task.id
                                                ,result_code = dict_response_result.code
                                                ,result_message = dict_response_result.error_msg
                                                ,result_data = dict_response_result.result
                                                ,flow_result_handle_message=dict_response_result_json))
    FlowTaskLogDBManager.create_flow_task_log(FlowTaskLog(task_id= flow_task.id
                                                          ,log_type=LogTypeEnum.TASK_RESULT.value[1]
                                                          ,message="""rpa script result: {}""".format(dict_response_result_json)))

    # 执行结果来源推送 todo

    # api返回
    return True