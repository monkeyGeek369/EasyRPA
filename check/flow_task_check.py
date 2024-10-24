from easyrpa.models.agent_models.flow_task_exe_res_dto import FlowTaskExeResDTO
from easyrpa.models.easy_rpa_exception import EasyRpaException
from easyrpa.enums.easy_rpa_exception_code_enum import EasyRpaExceptionCodeEnum
from easyrpa.tools import number_tool
from easyrpa.tools import str_tools

def flow_task_exe_res_dto_check(dto:FlowTaskExeResDTO):
    if number_tool.num_is_empty(dto.task_id):
        raise EasyRpaException("task id is empty",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,dto)
    if number_tool.num_is_empty(dto.site_id):
        raise EasyRpaException("site id is empty",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,dto)
    if number_tool.num_is_empty(dto.flow_id):
        raise EasyRpaException("flow id is empty",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,dto)
    if str_tools.str_is_empty(dto.flow_code):
        raise EasyRpaException("flow code is empty",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,dto)
    if str_tools.str_is_empty(dto.flow_name):
        raise EasyRpaException("flow name is empty",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,dto)
    if number_tool.num_is_empty(dto.sub_source):
        raise EasyRpaException("subscribe source is empty",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,dto)
    if dto.status is None:
        raise EasyRpaException("status is empty",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,dto)
    return True