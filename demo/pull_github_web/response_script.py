# start：调试时开启，正常执行时注释掉---------------------------------------------------------------------------------------
from easyrpa.models.base.request_header import RequestHeader
from easyrpa.tools import debug_tools
header = RequestHeader(user_id=1,trace_id="123",req_time=None)
message = '''{"status":true,"error_msg":"success","result":"login_success","code":"99999"}'''
debug_tools.env_params_build_and_set(header=header,sub_source=1,flow_standard_message=message,flow_config=None)
# end：调试时开启，正常执行时注释掉-----------------------------------------------------------------------------------------

from easyrpa.models.easy_rpa_exception import EasyRpaException
from easyrpa.enums.easy_rpa_exception_code_enum import EasyRpaExceptionCodeEnum
from easyrpa.enums.rpa_exe_result_code_enum import RpaExeResultCodeEnum
from easyrpa.models.scripty_exe_result import ScriptExeResult
import os
import json,jsonpickle

# 将json字符串转换为dict取值
standart = json.loads(os.environ.get("standard"),object_hook=dict)

if not standart:
    raise EasyRpaException("rpa execution result is null",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,standart)

# 构建回执结果
status=standart.get("status")
error_msg=standart.get("error_msg")
data =standart.get("result")
code = '99999'

if status:
    data = data + "执行成功"
else:
    data = data + "执行失败"
    code = str(RpaExeResultCodeEnum.FLOW_EXE_ERROR.value[1])

result = ScriptExeResult(status=status,error_msg=error_msg,print_str=None,result=data,code = code)

print(jsonpickle.encode(result))
