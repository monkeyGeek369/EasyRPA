from flask import Blueprint
from core.script_exe_core import response_result_script_exe
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
from dataclasses import asdict
from core.flow_task_exe_result_notify_core import flow_task_exe_result_notify
from easyrpa.models.flow.flow_task_exe_result_notify_dto import FlowTaskExeResultNotifyDTO
from models.task.task_search_req_model import TaskSearchReqModel
from models.task.task_search_res_model import TaskSearchResModel
from models.task_log.task_log_search_req_model import TaskLogSearchReqModel
from models.task_log.task_log_search_res_model import TaskLogSearchResModel
from core import task_manager_core,task_dispatch_core
from easyrpa.tools.json_tools import JsonTool
from models.task.task_detail_model import TaskDetailModel
from models.base.meta_data_base_model import MetaDataBaseModel


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
        sub_source=req.get("sub_source"),
        status=req.get("status"),
        error_msg=req.get("error_msg"),
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
                                    ,result=dto.result
                                    ,error_msg=dto.error_msg
                                    ,code=dto.code)
        response_result_message = json.dumps(asdict(exe_result),ensure_ascii=False)

        # 更新任务+记录日志
        flow_task = FlowTaskDBManager.update_flow_task(FlowTask(id= flow_task.id,task_result_message=response_result_message))
        FlowTaskLogDBManager.create_flow_task_log(FlowTaskLog(task_id= flow_task.id
                                                            ,log_type=LogTypeEnum.TASK_RESULT.value[1]
                                                            ,message="""rpa result: {}""".format(response_result_message)))

        # 执行返回值脚本
        dict_response_result = response_result_script_exe(flow_code=flow.flow_code,response_message=response_result_message,flow_exe_script=flow.flow_result_handle_script,sub_source=dto.sub_source,flow_config=None)
        logs_tool.log_business_info(title="flow_task_result_handler",message="response_result_script_exe",data=dict_response_result)
        dict_response_result_json = json.dumps(asdict(dict_response_result),ensure_ascii=False)
        logs_tool.log_business_info(title="flow_task_result_handler",message="dict_response_result_json",data=dict_response_result_json)
        
        # 更新任务+记录日志
        result_status = FlowTaskStatusEnum.SUCCESS.value[1] if dict_response_result.status else FlowTaskStatusEnum.FAIL.value[1]
        logs_tool.log_business_info(title="flow_task_result_handler",message="result_status",data=result_status)
        flow_task = FlowTaskDBManager.update_flow_task(FlowTask(id= flow_task.id
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
        flow_task = FlowTaskDBManager.update_flow_task(FlowTask(id= flow_task.id
                                                    ,status=FlowTaskStatusEnum.FAIL.value[1]))
        FlowTaskLogDBManager.create_flow_task_log(FlowTaskLog(task_id= flow_task.id
                                                            ,log_type=LogTypeEnum.TASK_RESULT.value[1]
                                                            ,message="""rpa script exe error: {}""".format(str(e))))
    finally:
        # task retry
        if flow_task.status != FlowTaskStatusEnum.SUCCESS.value[1]:
            task_dispatch_core.task_retry(task=flow_task)
        else:
            waiting_tasks = task_manager_core.search_waiting_tasks()
            if waiting_tasks:
                task_dispatch_core.task_retry(task=waiting_tasks[0])
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

@flow_task_bp.route('/flow/task/one', methods=['POST'])
@easyrpa_request_wrapper
def get_flow_task_by_id(id:int)->TaskDetailModel:
    return task_manager_core.get_flow_task_by_id(id=id)

@flow_task_bp.route('/flow/subSource/all', methods=['POST'])
@easyrpa_request_wrapper
def get_all_sub_source(param) -> list[MetaDataBaseModel]:
    return task_manager_core.get_all_source_types()

@flow_task_bp.route('/flow/taskStatus/all', methods=['POST'])
@easyrpa_request_wrapper
def get_all_task_status(param) -> list[MetaDataBaseModel]:
    return task_manager_core.get_all_task_status()

@flow_task_bp.route('/flow/task/log/search', methods=['POST'])
@easyrpa_request_wrapper
def search_flow_task_logs(dto:TaskLogSearchReqModel) -> TaskLogSearchResModel:
    # base check
    if number_tool.num_is_empty(dto.get("page")):
        raise EasyRpaException("search page is empty",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,dto)
    if number_tool.num_is_empty(dto.get("page_size")):
        raise EasyRpaException("search page size is empty",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,dto)
    
    # dto to do
    log_obj = FlowTaskLog()
    log_obj.id = dto.get("id")
    log_obj.task_id=dto.get("task_id")

    # search from db
    search_result = task_manager_core.search_task_logs_by_params(do=log_obj,page=dto.get("page"),page_size=dto.get("page_size"),sorts=dto.get("sorts"))
    
    # search count
    total = task_manager_core.search_task_log_count_by_params(do=log_obj)

    # return
    result = TaskLogSearchResModel(
        total=total,
        data=search_result,
        sorts=dto.get("sorts")
    )

    return JsonTool.any_to_dict(result)
