import unittest
from database.site_db_manager import SiteDbManager
from database.flow_db_manager import FlowDbManager
from database.models import Flow,FlowConfiguration
from database.flow_configuration_db_manager import FlowConfigurationDBManager


class TestDbTmpDataOperation(unittest.TestCase):
    def test_create_site(self):
        id = SiteDbManager.add_site("youtube","youtube website")
        print(id)
    
    def test_create_flow(self):
        code = """
from playwright import sync_api
import sys

print("123")

def test():
    print(len(sys.argv))
    print(sys.argv)
print("456")
test()
print("789")
"""
        new_flow = Flow(
            site_id=2,
            flow_code="download_youtube_website",
            flow_name="youtube video download",
            flow_rpa_type =1,
            flow_exe_env =1,
            flow_biz_type =1,
            max_retry_number =3,
            max_exe_time =300,
            retry_code = "network_error",
            request_check_script = code,
            request_adapt_script = code,
            flow_exe_script = code,
            flow_result_handle_script = code
        )
        id = FlowDbManager.create_flow(new_flow)
        print(id)

    def test_delete_flow(self):
        FlowDbManager.delete_flow(2)

    def test_create_flow_configuration(self):
        json_str = '''{"config_key1":123,"config_key2":"ckv2","config_key3":{"ck1":"cv1","ck2":234,"ck3":[1,2,3],"ck4":{"cck1":111},"ck5":[{"cck51":555,"cck52":"52"}]},"config_key4":[{"ck41":444,"ck42":"456"}]}'''
        flow_configuration = FlowConfiguration(flow_id=1,config_name="name",config_description="description",config_json=json_str)
        FlowConfigurationDBManager.create_flow_configuration(flow_configuration)

class TestDemoPullGithubWeb(unittest.TestCase):
    def test_create_site(self):
        id = SiteDbManager.add_site("demo","pull github web demo")
        print(id)

    def test_create_flow(self):
        request_check_script = """
import os
import ast
import json
from easyrpa.models.easy_rpa_exception import EasyRpaException
from easyrpa.enums.easy_rpa_exception_code_enum import EasyRpaExceptionCodeEnum
from easyrpa.tools import number_tool,str_tools

# 将json字符串转换为dict取值
header = ast.literal_eval(os.environ.get("header"))
standart = json.loads(os.environ.get("standard"),object_hook=dict)
config = json.loads(os.environ.get("flow_config"),object_hook=dict)

# 校验header
if not header or len(header) <= 0:
    raise EasyRpaException("header params is null",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,header)
if number_tool.num_is_empty(header.get("user_id")):
    raise EasyRpaException("user_id params is null",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,header)
if str_tools.str_is_empty(header.get("trace_id")):
    raise EasyRpaException("trace_id params is null",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,header)

# 校验标准参数
if not standart or len(standart) <= 0:
    raise EasyRpaException("standard params is null",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,standart)
if str_tools.str_is_empty(standart.get("home_url")):
    raise EasyRpaException("home_url params is null",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,standart)
if str_tools.str_is_empty(standart.get("login_url")):
    raise EasyRpaException("login_url params is null",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,standart)
if str_tools.str_is_empty(standart.get("search_key")):
    raise EasyRpaException("search_key params is null",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,standart)

# 校验配置参数
if not config or len(config) <= 0:
    raise EasyRpaException("flow_config params is null",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,config)
if str_tools.str_is_empty(config.get("account")):
    raise EasyRpaException("account params is null",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,config)
if str_tools.str_is_empty(config.get("password")):
    raise EasyRpaException("password params is null",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,config)
"""
        request_adapt_script = """
import os
import ast
import json

# 将json字符串转换为dict取值
header = ast.literal_eval(os.environ.get("header"))
standart = json.loads(os.environ.get("standard"),object_hook=dict)
config = json.loads(os.environ.get("flow_config"),object_hook=dict)

# 构建json字符串对象
dict_params = {
    "home_url":standart.get("home_url"),
    "login_url":standart.get("login_url"),
    "search_key":standart.get("search_key"),
    "account":config.get("account"),
    "password":config.get("password")
}

print(json.dumps(dict_params))
"""
        flow_exe_script = """
from playwright.sync_api import sync_playwright
from playwright.sync_api import Browser
from playwright.sync_api import Page
import os
import json

def openPage(browser: Browser,message:dict) -> Page:
    page = browser.new_page()
    page.goto(message.get("home_url"), timeout=50000)
    return page

def search_playwright(page: Page,message:dict) -> None:
    page.locator("qbsearch-input").click()
    # 等待页面加载
    page.wait_for_load_state(state="networkidle")
    page.locator("//*[@id='query-builder-test']").fill(message.get("search_key"))
    # 等待页面加载
    page.wait_for_load_state(state="networkidle")
    page.wait_for_timeout(2000)
    page.locator("//*[@id='query-builder-test']").press("Enter")
    # 等待页面加载
    page.wait_for_load_state(state="networkidle")
    page.get_by_role("link", name="microsoft/playwright",exact=True).click()
    # 等待页面加载
    page.wait_for_load_state(state="networkidle")
    # 异常页面处理
    # todo


def login(page: Page,message:dict) -> str:
    page.goto(message.get("login_url"), timeout=50000)
    # 等待页面加载
    page.wait_for_load_state(state="networkidle")
    page.locator("//*[@id='login_field']").fill(message.get("account"))
    page.locator("//*[@id='password']").fill(message.get("password"))
    page.wait_for_timeout(2000)
    page.get_by_role("button",name="Sign in",exact=True).click()
    page.wait_for_timeout(2000)
    # 获取错误提示信息
    is_error = page.locator("#js-flash-container").is_visible()
    if is_error:
        return "login_error"
    else:
        return "login_success"

def main():
    # 创建PlaywrightContextManager的实例
    
    manager = sync_playwright()
    
    # 手动调用start方法
    pw = manager.start()
    try:
        # 将json字符串转换为dict取值
        standart = json.loads(os.environ.get("standard"),object_hook=dict)

        browser = pw.chromium.launch(headless=False,channel='chrome')
        # 打开页面
        page = openPage(browser=browser,message=standart)
        # 搜索playwright
        search_playwright(page=page,message=standart)
        # 登录
        result = login(page=page,message=standart)

        print(result)
        
    except Exception as e:
        # 处理任何异常
        print(f"An error occurred: {e}")
    finally:
        # 无论是否发生异常，都调用stop方法来释放资源
        pw.stop()


if __name__ =='__main__':
    main()
"""
        flow_result_handle_script = """

from easyrpa.models.easy_rpa_exception import EasyRpaException
from easyrpa.enums.easy_rpa_exception_code_enum import EasyRpaExceptionCodeEnum
from easyrpa.enums.rpa_exe_result_code_enum import RpaExeResultCodeEnum
from easyrpa.models.scripty_exe_result import ScriptExeResult
import os
import json

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

print(json.dumps(result))
"""

        FlowDbManager.update_flow(Flow(id=3
                                       ,request_check_script=request_check_script
                                       ,request_adapt_script=request_adapt_script
                                       ,flow_exe_script=flow_exe_script
                                       ,flow_result_handle_script=flow_result_handle_script))

        # new_flow = Flow(
        #     site_id=3,
        #     flow_code="pull_github_web",
        #     flow_name="pull github web demo",
        #     flow_rpa_type =1,
        #     flow_exe_env =1,
        #     flow_biz_type =1,
        #     max_retry_number =3,
        #     max_exe_time =300,
        #     retry_code = "10001",
        #     request_check_script = request_check_script,
        #     request_adapt_script = request_adapt_script,
        #     flow_exe_script = flow_exe_script,
        #     flow_result_handle_script = flow_result_handle_script
        # )
        # id = FlowDbManager.create_flow(new_flow)
        # print(id)
        
    def test_create_flow_configuration(self):
        json_str = '''{"account":"123","password":"456"}'''
        flow_configuration = FlowConfiguration(flow_id=2,config_name="demo_config",config_description="pull github web demo config",config_json=json_str)
        FlowConfigurationDBManager.create_flow_configuration(flow_configuration)

