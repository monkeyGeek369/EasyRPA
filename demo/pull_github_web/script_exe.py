# start：调试时开启，正常执行时注释掉---------------------------------------------------------------------------------------
from easyrpa.models.base.request_header import RequestHeader
from easyrpa.tools import debug_tools
header = RequestHeader(user_id=1,trace_id="123",req_time=None)
message = '''{"home_url":"https://github.com","login_url":"https://github.com/login","search_key":"playwright","account":"123","password":"456"}'''
debug_tools.env_params_build_and_set(header=header,sub_source=1,flow_standard_message=message,flow_config=None)
# end：调试时开启，正常执行时注释掉-----------------------------------------------------------------------------------------
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