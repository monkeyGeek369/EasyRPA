from database.models import FlowTask,Flow,FlowTaskLog
from easyrpa.models.agent_models.flow_task_exe_req_dto import FlowTaskExeReqDTO
import requests
from database.flow_task_db_manager import FlowTaskDBManager
from database.flow_task_log_db_manager import FlowTaskLogDBManager
from easyrpa.enums.flow_task_status_enum import FlowTaskStatusEnum
from easyrpa.enums.log_type_enum import LogTypeEnum
from easyrpa.tools import request_tool


def flow_task_dispatch(flow:Flow,flow_task:FlowTask,flow_exe_env:str):
     # 获取可用机器人-todo：先简单实现
     url = "http://192.168.2.178:5006/flow/task/async/exe"

     try:
        # 构造请求参数
        flow_task_exe_req_dto = FlowTaskExeReqDTO(task_id=flow_task.id
                                                  ,site_id=flow_task.site_id
                                                  ,flow_id=flow_task.flow_id
                                                  ,flow_code=flow.flow_code
                                                  ,flow_name=flow.flow_name
                                                  ,flow_rpa_type=flow.flow_rpa_type
                                                  ,flow_exe_env=flow_exe_env
                                                  ,flow_standard_message=flow_task.flow_standard_message
                                                  ,flow_exe_script=flow.flow_exe_script
                                                  ,sub_source=flow_task.sub_source)
        
        # 将任务执行请求以post方式发送到机器人
        req_json = request_tool.request_base_model_json_builder(flow_task_exe_req_dto)
        response = requests.post(url, json=req_json)
        
        # 请求数据记录
        FlowTaskLogDBManager.create_flow_task_log(FlowTaskLog(task_id=flow_task.id,log_type=LogTypeEnum.TXT.value[1],message=f"adapt script message:{req_json}。"))

        # 调度结果处理
        if response.status_code == 200:
            # 任务状态修改为执行中
            update_flow_task = FlowTask(id=flow_task.id,status=FlowTaskStatusEnum.EXECUTION.value[1])
            FlowTaskDBManager.update_flow_task(update_flow_task)

            # 记录任务日志
            FlowTaskLogDBManager.create_flow_task_log(FlowTaskLog(task_id=flow_task.id,log_type=LogTypeEnum.TXT.value[1],message=f"流程任务调度成功，已经成功发送至机器人[{url}]。"))
        else:
            # 任务状态-执行失败
            update_flow_task = FlowTask(id=flow_task.id,status=FlowTaskStatusEnum.FAIL.value[1])
            FlowTaskDBManager.update_flow_task(update_flow_task)

            # 记录任务日志
            FlowTaskLogDBManager.create_flow_task_log(FlowTaskLog(task_id=flow_task.id,log_type=LogTypeEnum.TXT.value[1],message=response.text))
     except Exception as e:
            # 任务状态-执行失败
            update_flow_task = FlowTask(id=flow_task.id,status=FlowTaskStatusEnum.FAIL.value[1])
            FlowTaskDBManager.update_flow_task(update_flow_task)

            # 记录任务日志
            FlowTaskLogDBManager.create_flow_task_log(FlowTaskLog(task_id=flow_task.id,log_type=LogTypeEnum.TXT.value[1],message=str(e)))
     