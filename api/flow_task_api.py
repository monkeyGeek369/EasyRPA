from flask import Blueprint
from core.script_exe_core import rpa_result_script_exe
from easyrpa.tools.request_tool import easyrpa_request_wrapper
from easyrpa.models.easy_rpa_exception import EasyRpaException
from easyrpa.enums.easy_rpa_exception_code_enum import EasyRpaExceptionCodeEnum
from check.flow_task_check import flow_task_exe_res_dto_check
from database.flow_db_manager import FlowDbManager
from database.flow_task_db_manager import FlowTaskDBManager
from database.flow_task_db_manager import FlowTaskLogDBManager
from easyrpa.models.scripty_exe_result import ScriptExeResult
from easyrpa.enums.log_type_enum import LogTypeEnum
import json
from database.models import FlowTask,FlowTaskLog
from easyrpa.models.agent_models.flow_task_exe_res_dto import FlowTaskExeResDTO
from easyrpa.tools import str_tools,logs_tool,number_tool
from easyrpa.enums.flow_task_status_enum import FlowTaskStatusEnum
from core.flow_manager_core import get_flow_exe_env_meta_data
from dataclasses import asdict
from core.flow_task_exe_result_notify_core import flow_task_exe_result_notify
from easyrpa.models.flow.flow_task_exe_result_notify_dto import FlowTaskExeResultNotifyDTO
from configuration.app_config_manager import AppConfigManager
from models.task.task_search_req_model import TaskSearchReqModel
from models.task.task_search_res_model import TaskSearchResModel
from core import task_manager_core
from easyrpa.tools.json_tools import JsonTool

flow_task_bp =  Blueprint('flow_task',__name__)

@flow_task_bp.route('/flow/task/result/handler', methods=['POST'])
@easyrpa_request_wrapper
def flow_task_result_handler(req:FlowTaskExeResDTO) -> bool:
    dto = FlowTaskExeResDTO(
        task_id=req.get("task_id"),
        site_id=req.get("site_id"),
        flow_id=req.get("flow_id"),
        flow_code=req.get("flow_code"),
        flow_name=req.get("flow_name"),
        flow_rpa_type=req.get("flow_rpa_type"),
        flow_exe_env=req.get("flow_exe_env"),
        sub_source=req.get("sub_source"),
        status=req.get("status"),
        error_msg=req.get("error_msg"),
        print_str=req.get("print_str"),
        result=req.get("result"),
        code=req.get("code")
    )

    # 查询流程任务
    flow_task = FlowTaskDBManager.get_flow_task_by_id(dto.task_id)
    if flow_task is None:
        raise EasyRpaException("""flow task {} not found""".format(dto.task_id),EasyRpaExceptionCodeEnum.DATA_NOT_FOUND.value[1],None,dto)
    
    try:
        # 基础校验
        flow_task_exe_res_dto_check(dto)

        # 查询流程
        flow = FlowDbManager.get_flow_by_id(dto.flow_id)
        if flow is None:
            raise EasyRpaException("""flow {} not found""".format(dto.flow_id),EasyRpaExceptionCodeEnum.DATA_NOT_FOUND.value[1],None,dto)
        if str_tools.str_is_empty(flow.flow_result_handle_script):
            raise EasyRpaException("""flow {} not found flow result handle script""".format(dto.flow_id),EasyRpaExceptionCodeEnum.DATA_NOT_FOUND.value[1],None,dto)
        
        # 获取rpa执行结果
        exe_result = ScriptExeResult(status=dto.status
                                    ,print_str=dto.print_str
                                    ,result=dto.result
                                    ,error_msg=dto.error_msg
                                    ,code=dto.code)
        rpa_result_message = json.dumps(asdict(exe_result),ensure_ascii=False)

        # 更新任务+记录日志
        FlowTaskDBManager.update_flow_task(FlowTask(id= flow_task.id,task_result_message=rpa_result_message))
        FlowTaskLogDBManager.create_flow_task_log(FlowTaskLog(task_id= flow_task.id
                                                            ,log_type=LogTypeEnum.TASK_RESULT.value[1]
                                                            ,message="""rpa result: {}""".format(rpa_result_message)))
        
        # 获取执行环境
        app = AppConfigManager()
        conda_env = app.get_console_default_conda_env()

        # 执行返回值脚本
        dict_response_result = rpa_result_script_exe(flow_exe_env=conda_env
                                                    ,rpa_result_message=rpa_result_message
                                                    ,flow_exe_script=flow.flow_result_handle_script
                                                    ,sub_source=dto.sub_source
                                                    ,flow_config=None)
        logs_tool.log_business_info(title="flow_task_result_handler",message="rpa_result_script_exe",data=dict_response_result)
        dict_response_result_json = json.dumps(asdict(dict_response_result),ensure_ascii=False)
        logs_tool.log_business_info(title="flow_task_result_handler",message="dict_response_result_json",data=dict_response_result_json)
        
        # 更新任务+记录日志
        result_status = FlowTaskStatusEnum.SUCCESS.value[1] if dict_response_result.status else FlowTaskStatusEnum.FAIL.value[1]
        logs_tool.log_business_info(title="flow_task_result_handler",message="result_status",data=result_status)
        FlowTaskDBManager.update_flow_task(FlowTask(id= flow_task.id
                                                    ,result_code = dict_response_result.code
                                                    ,result_message = dict_response_result.error_msg
                                                    ,result_data = dict_response_result.result
                                                    ,flow_result_handle_message=dict_response_result_json
                                                    ,status= result_status))
        logs_tool.log_business_info(title="flow_task_result_handler",message="update_flow_task",data=None)
        FlowTaskLogDBManager.create_flow_task_log(FlowTaskLog(task_id= flow_task.id
                                                            ,log_type=LogTypeEnum.TASK_RESULT.value[1]
                                                            ,message="""rpa script result: {}""".format(dict_response_result_json)))
        logs_tool.log_business_info(title="flow_task_result_handler",message="create_flow_task_log",data=None)

        # 执行结果来源推送
        notify = FlowTaskExeResultNotifyDTO(
            site_id=flow_task.site_id
            ,flow_id=flow_task.flow_id
            ,flow_task_id=flow_task.id
            ,flow_config_id=flow_task.flow_config_id
            ,biz_no=flow_task.biz_no
            ,sub_source=flow_task.sub_source
            ,status=result_status
            ,result_code=dict_response_result.code
            ,result_message=dict_response_result.error_msg
            ,result_data=dict_response_result.result
            ,screenshot_base64=None
            ,created_id=flow_task.created_id
            ,created_time=flow_task.created_time
        )
        flow_task_exe_result_notify(notify)

        # api返回
        return True
    except Exception as e:
        logs_tool.log_business_error(title="flow_task_result_handler",message="flow task result handler error",data=dto,exc_info=e)
        # 更新任务+记录日志
        FlowTaskDBManager.update_flow_task(FlowTask(id= flow_task.id
                                                    ,status=FlowTaskStatusEnum.FAIL.value[1]))
        FlowTaskLogDBManager.create_flow_task_log(FlowTaskLog(task_id= flow_task.id
                                                            ,log_type=LogTypeEnum.TASK_RESULT.value[1]
                                                            ,message="""rpa script exe error: {}""".format(str(e))))
    return False

@flow_task_bp.route('/flow/task/search', methods=['POST'])
@easyrpa_request_wrapper
def search_flow_tasks(dto:TaskSearchReqModel) -> TaskSearchResModel:
    # base check
    if number_tool.num_is_empty(dto.get("page")):
        raise EasyRpaException("search page is empty",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,dto)
    if number_tool.num_is_empty(dto.get("page_size")):
        raise EasyRpaException("search page size is empty",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,dto)
    
    # dto to do
    task_obj = FlowTask()
    task_obj.id = dto.get("id")
    task_obj.site_id=dto.get("site_id")
    task_obj.flow_id=dto.get("flow_id")
    task_obj.biz_no=dto.get("biz_no")
    task_obj.sub_source=dto.get("sub_source")
    task_obj.status=dto.get("status")
    task_obj.result_code=dto.get("result_code")
    task_obj.result_message=dto.get("result_message")
    task_obj.result_data=dto.get("result_data")
    task_obj.is_active = dto.get("is_active")

    # search from db
    search_result = task_manager_core.search_tasks_by_params(do=task_obj,page=dto.get("page"),page_size=dto.get("page_size"),sorts=dto.get("sorts"))
    
    # search count
    total = task_manager_core.search_count_by_params(do=task_obj)

    # return
    result = TaskSearchResModel(
        total=total,
        data=search_result,
        sorts=dto.get("sorts")
    )

    return JsonTool.any_to_dict(result)
