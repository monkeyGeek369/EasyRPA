from flask import Blueprint
from easyrpa.tools import str_tools,logs_tool,number_tool
from easyrpa.tools.request_tool import easyrpa_request_wrapper
from easyrpa.models.easy_rpa_exception import EasyRpaException
from easyrpa.enums.easy_rpa_exception_code_enum import EasyRpaExceptionCodeEnum
from easyrpa.tools.json_tools import JsonTool


robot_api_bp =  Blueprint('robot_api',__name__)

@robot_api_bp.route('/robot/heartbeat', methods=['POST'])
@easyrpa_request_wrapper
def heartbeat_check():
    # https://www.cnblogs.com/xpvincent/p/10053618.html
    # 如何生成唯一不变机器码？
    # https://blog.csdn.net/TaiBai_435_/article/details/122010188
    pass

@robot_api_bp.route('/robot/delete', methods=['POST'])
@easyrpa_request_wrapper
def delete_robot():
    pass

@robot_api_bp.route('/robot/log/report', methods=['POST'])
@easyrpa_request_wrapper
def robot_log_report():
    pass