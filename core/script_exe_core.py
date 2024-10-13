from easyrpa.script_exe.subprocess_python_script import subprocess_script_run,env_activate_command_builder
from easyrpa.models.base.script_exe_param_model import ScriptExeParamModel
from easyrpa.tools.transfer_tools import any_to_str_dict_first_level,dict_to_str_dict_first_level
from easyrpa.tools.str_tools import str_to_str_dict
from easyrpa.models.easy_rpa_exception import EasyRpaException
from easyrpa.enums.easy_rpa_exception_code_enum import EasyRpaExceptionCodeEnum
from easyrpa.models.scripty_exe_result import ScriptExeResult
from dataclasses import asdict
import easyrpa.tools.debug_tools as my_debug
from easyrpa.tools import logs_tool,str_tools
import json

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
    if script_result is None:
        raise EasyRpaException("script result is null",EasyRpaExceptionCodeEnum.EXECUTE_ERROR.value[1],None,flow_standard_message)
    if script_result.status is None or not script_result.status:
        raise EasyRpaException("script result status is error:" + script_result.error_msg,EasyRpaExceptionCodeEnum.EXECUTE_ERROR.value[1],None,script_result.print_str)

    return True

def request_adapter_script_exe(flow_exe_env:str,flow_standard_message:str
                             ,flow_exe_script:str,sub_source:int,flow_config:str) -> dict:
    """执行适配脚本

    Args:
        flow_exe_env (str): 流程执行环境
        flow_standard_message (str): 流程标准消息
        flow_exe_script (str): 流程执行脚本
        sub_source (int): 来源
        flow_config (str): 流程配置

    Raises:
        EasyRpaException: 异常信息

    Returns:
        dict: 返回结果
    """
    
    # 执行脚本
    script_result = script_exe_base(flow_exe_env,flow_standard_message,flow_exe_script,sub_source,flow_config)

    # 执行结果处理
    if not script_result:
        raise EasyRpaException("script result is null",EasyRpaExceptionCodeEnum.EXECUTE_ERROR.value[1],None,flow_standard_message)
    if not script_result.status:
        raise EasyRpaException("script result status is error:" + script_result.error_msg,EasyRpaExceptionCodeEnum.EXECUTE_ERROR.value[1],None,script_result.print_str)
    if not script_result.result:
        raise EasyRpaException("script result result is null",EasyRpaExceptionCodeEnum.EXECUTE_ERROR.value[1],None,script_result.print_str)
    
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
    logs_tool.log_business_info(title="rpa_result_script_exe",message="script_exe_base",data=script_result)

    # 执行结果异常
    if script_result is None or str_tools.str_is_empty(script_result.result):
        return script_result
    
    # 执行结果正常
    result_dict = json.loads(script_result.result)

    result = ScriptExeResult(status=result_dict.get("status")
                             ,error_msg=result_dict.get("error_msg")
                             ,print_str=result_dict.get("print_str")
                             ,result=result_dict.get("result")
                             ,code = result_dict.get("code"))

    return result

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
    param = my_debug.env_params_build(header=None,sub_source=sub_source,flow_standard_message=flow_standard_message,flow_config=flow_config)
    
    # 日志记录参数传递
    logs_tool.log_business_info("script_exe_base","脚本执行参数记录",param)

    # 调用脚本执行器
    env_activate_command = env_activate_command_builder(flow_exe_env)
    
    logs_tool.log_business_info("script_exe_base","环境激活命令",env_activate_command)
    script_result = subprocess_script_run(env_activate_command,"python",flow_exe_script,param)
    
    logs_tool.log_business_info("script_exe_base","脚本执行结果",script_result)
    return script_result