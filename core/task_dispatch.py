from database.models import FlowTask,Flow,FlowTaskLog
from easyrpa.models.agent_models.flow_task_exe_req_dto import FlowTaskExeReqDTO
import requests
from database.flow_task_db_manager import FlowTaskDBManager
from database.flow_task_log_db_manager import FlowTaskLogDBManager
from easyrpa.enums.flow_task_status_enum import FlowTaskStatusEnum
from easyrpa.enums.log_type_enum import LogTypeEnum


def flow_task_dispatch(flow:Flow,flow_task:FlowTask):
     # 获取可用机器人-todo：先简单实现
     url = "http://127.0.0.1:5006/flow/task/async/exe"

     try:
        # 构造请求参数
        flow_task_exe_req_dto = FlowTaskExeReqDTO()
        flow_task_exe_req_dto.task_id = flow_task.id
        flow_task_exe_req_dto.site_id = flow_task.site_id
        flow_task_exe_req_dto.flow_id = flow_task.flow_id
        flow_task_exe_req_dto.flow_code = flow.flow_code
        flow_task_exe_req_dto.flow_name = flow.flow_name
        flow_task_exe_req_dto.flow_rpa_type = flow.flow_rpa_type
        flow_task_exe_req_dto.flow_exe_env = flow.flow_exe_env
        flow_task_exe_req_dto.flow_standard_message = flow_task.flow_standard_message
        flow_task_exe_req_dto.flow_exe_script = flow.flow_exe_script
        flow_task_exe_req_dto.sub_source = flow_task.sub_source
        
        # 将任务执行请求以post方式发送到机器人
        response = requests.post(url, json=flow_task_exe_req_dto)

        # 调度结果处理
        if response.status_code == 200:
            # 任务状态修改为执行中
            update_flow_task = FlowTask(id=flow_task.id,status=FlowTaskStatusEnum.EXECUTION.code)
            FlowTaskDBManager.update_flow_task(update_flow_task)

            # 记录任务日志
            FlowTaskLogDBManager.create_flow_task_log(FlowTaskLog(task_id=flow_task.id,log_type=LogTypeEnum.TXT.code,message=f"流程任务调度成功，已经成功发送至机器人[{url}]。"))
        else:
            # 任务状态-执行失败
            update_flow_task = FlowTask(id=flow_task.id,status=FlowTaskStatusEnum.FAIL.code)
            FlowTaskDBManager.update_flow_task(update_flow_task)

            # 记录任务日志
            FlowTaskLogDBManager.create_flow_task_log(FlowTaskLog(task_id=flow_task.id,log_type=LogTypeEnum.TXT.code,message=response.text))
     except Exception as e:
            # 任务状态-执行失败
            update_flow_task = FlowTask(id=flow_task.id,status=FlowTaskStatusEnum.FAIL.code)
            FlowTaskDBManager.update_flow_task(update_flow_task)

            # 记录任务日志
            FlowTaskLogDBManager.create_flow_task_log(FlowTaskLog(task_id=flow_task.id,log_type=LogTypeEnum.TXT.code,message=str(e)))
     