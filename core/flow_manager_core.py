from easyrpa.models.flow.flow_task_subscribe_result_dto import FlowTaskSubscribeResultDTO
from easyrpa.models.flow.flow_task_subscribe_dto import FlowTaskSubscribeDTO
import check.flow_task_subscribe_dto_check as sub_check
from easyrpa.tools import request_tool 

def flow_task_subscribe(dto:FlowTaskSubscribeDTO)-> FlowTaskSubscribeResultDTO:
    try:
        # 参数校验
        sub_check.flow_task_subscribe_dto_check(dto)

        # 获取当前用户
        header = request_tool.get_current_header()

        # 查询流程

        # 查询流程配置

        # 执行校验脚本

        # 执行适配脚本

        # 获取流程报文

        # 创建流程任务

        # 流程任务分发

    except Exception as e:
        return FlowTaskSubscribeResultDTO()