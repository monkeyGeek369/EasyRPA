# start：调试时开启，正常执行时注释掉---------------------------------------------------------------------------------------
from easyrpa.models.base.request_header import RequestHeader
from easyrpa.tools import debug_tools
header = RequestHeader(user_id=1,trace_id="123",req_time=None)
message = '''{"home_url":"https://github.com","login_url":"https://github.com/login","search_key":"playwright"}'''
config = '''{"account":"123","password":"456"}'''
debug_tools.env_params_build_and_set(header=header,sub_source=1,flow_standard_message=message,flow_config=config)
# end：调试时开启，正常执行时注释掉-----------------------------------------------------------------------------------------
from playwright.sync_api import sync_playwright
from playwright.sync_api import Browser
from playwright.sync_api import Page
import os
import ast
import json

def openPage(browser: Browser,message:dict) -> Page:
    page = browser.new_page()
    page.goto(message.get("home_url"), timeout=50000)
    return page

def search_playwright(page: Page,message:dict) -> None:
    pass

def login(page: Page,message:dict,config:dict) -> None:
    pass


def main():
    # 创建PlaywrightContextManager的实例
    
    manager = sync_playwright()
    
    # 手动调用start方法
    pw = manager.start()
    try:
        # 将json字符串转换为dict取值
        header = ast.literal_eval(os.environ.get("header"))
        standart = json.loads(os.environ.get("standard"),object_hook=dict)
        config = json.loads(os.environ.get("flow_config"),object_hook=dict)

        browser = pw.chromium.launch(headless=False,channel='chrome')
        # 登录
        page = openPage(browser=browser,message=standart)
        # 搜索playwright
        search_playwright(page=page,message=standart)
        # 填写vgm信息
        login(page=page,message=standart,config=config)
        
    except Exception as e:
        # 处理任何异常
        print(f"An error occurred: {e}")
    finally:
        # 无论是否发生异常，都调用stop方法来释放资源
        pw.stop()


if __name__ =='__main__':
    main()