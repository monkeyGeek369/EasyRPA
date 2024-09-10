from easyrpa.script_exe.subprocess_python_script import subprocess_script_run,env_activate_command_builder
from easyrpa.models.base.script_exe_param_model import ScriptExeParamModel
from easyrpa.tools import request_tool
from easyrpa.tools.transfer_tools import any_to_str_dict_first_level,dict_to_str_dict_first_level
from easyrpa.tools.str_tools import str_to_str_dict
from easyrpa.models.easy_rpa_exception import EasyRpaException
from easyrpa.enums.easy_rpa_exception_code_enum import EasyRpaExceptionCodeEnum
from easyrpa.models.scripty_exe_result import ScriptExeResult
import json
from dataclasses import asdict
from easyrpa.tools import logs_tool

def request_check_script_exe(flow_exe_env:str,flow_standard_message:str
                             ,flow_exe_script:str,sub_source:int,flow_config:str) -> bool:
    """执行校验脚本

    Args:
        flow_exe_env (str): 指定执行环境
        flow_standard_message (str): 流程标准模型
        flow_exe_script (str): 执行脚本
        sub_source (int): 订阅来源

    Raises:
        EasyRpaException: 异常

    Returns:
        bool: true
    """
    # 执行脚本
    script_result = script_exe_base(flow_exe_env,flow_standard_message,flow_exe_script,sub_source,flow_config)

    # 执行结果处理
    if not script_result:
        raise EasyRpaException("script result is null",EasyRpaExceptionCodeEnum.EXECUTE_ERROR.code,None,flow_standard_message)
    if not script_result.status:
        raise EasyRpaException("script result status is error:" + script_result.error_msg,EasyRpaExceptionCodeEnum.EXECUTE_ERROR.code,None,script_result.print_str)

    return True

def request_adapter_script_exe(flow_exe_env:str,flow_standard_message:str
                             ,flow_exe_script:str,sub_source:int,flow_config:str) -> dict:
    
    # 执行脚本
    script_result = script_exe_base(flow_exe_env,flow_standard_message,flow_exe_script,sub_source,flow_config)

    # 执行结果处理
    if not script_result:
        raise EasyRpaException("script result is null",EasyRpaExceptionCodeEnum.EXECUTE_ERROR.code,None,flow_standard_message)
    if not script_result.status:
        raise EasyRpaException("script result status is error:" + script_result.error_msg,EasyRpaExceptionCodeEnum.EXECUTE_ERROR.code,None,script_result.print_str)
    if not script_result.result:
        raise EasyRpaException("script result result is null",EasyRpaExceptionCodeEnum.EXECUTE_ERROR.code,None,script_result.print_str)
    
    # 执行结果转dict
    dict_result = str_to_str_dict(script_result.result)
    return dict_result


def rpa_result_script_exe(flow_exe_env:str,rpa_result_message:str
                             ,flow_exe_script:str,sub_source:int,flow_config:str) -> ScriptExeResult:
    """执行rpa结果处理脚本

    Args:
        flow_exe_env (str): 指定执行环境
        rpa_result_message (str): rpa执行结果
        flow_exe_script (str): 执行脚本
        sub_source (int): 订阅来源

    Returns:
        ScriptExeResult: 执行结果模型
    """
    
    # 执行脚本
    script_result = script_exe_base(flow_exe_env,rpa_result_message,flow_exe_script,sub_source,flow_config)
    return script_result

def script_exe_base(flow_exe_env:str,flow_standard_message:str
                             ,flow_exe_script:str,sub_source:int
                             ,flow_config:str) -> ScriptExeResult:
    """脚本执行基础方法

    Args:
        flow_exe_env (str): 指定执行环境
        flow_standard_message (str): 流程标准模型
        flow_exe_script (str): 执行脚本
        sub_source (int): 订阅来源

    Returns:
        ScriptExeResult: 执行结果模型
    """

    # 构建执行参数
    script_param = ScriptExeParamModel(header=request_tool.get_current_header()
                                       ,source=sub_source
                                       ,standard=str_to_str_dict(flow_standard_message)
                                       ,flow_config=str_to_str_dict(flow_config))
    
    dict_data = asdict(script_param)
    param = any_to_str_dict_first_level(json.dumps(dict_data,default=str))

    # 日志记录参数传递
    logs_tool.log_business_info("script_exe_base","脚本执行参数记录",param)

    # 调用脚本执行器
    env_activate_command = env_activate_command_builder(flow_exe_env)
    script_result = subprocess_script_run(env_activate_command,"python",flow_exe_script,param)
    return script_result