# start：调试时开启，正常执行时注释掉---------------------------------------------------------------------------------------
from easyrpa.models.base.request_header import RequestHeader
from easyrpa.tools import debug_tools
header = RequestHeader(user_id=1,trace_id="123",req_time=None)
message = '''{"message_key1":666,"message_key2":"mkv2","message_key3":{"mk1":"mkv1","mk2":908,"mk3":[5,6,9],"mk4":{"mmk1":784},"mk5":[{"mmk51":333,"mm52":"32"}]},"message_key4":[{"mk41":369,"mk42":"963"}]}'''
config = '''{"config_key1":123,"config_key2":"ckv2","config_key3":{"ck1":"cv1","ck2":234,"ck3":[1,2,3],"ck4":{"cck1":111},"ck5":[{"cck51":555,"cck52":"52"}]},"config_key4":[{"ck41":444,"ck42":"456"}]}'''
debug_tools.env_params_build_and_set(header=header,sub_source=1,flow_standard_message=message,flow_config=config)
# end：调试时开启，正常执行时注释掉-----------------------------------------------------------------------------------------


# 以下为正常流程代码
import os
import json
import ast

# 获取标准参数
print(os.environ.get("header"))
print(os.environ.get("source"))
print(os.environ.get("standard"))
print(os.environ.get("flow_config"))

# 将json字符串转换为dict取值
header = ast.literal_eval(os.environ.get("header"))
standart = json.loads(os.environ.get("standard"),object_hook=dict)
config = json.loads(os.environ.get("flow_config"),object_hook=dict)