import unittest
from database.site_db_manager import SiteDbManager
from database.flow_db_manager import FlowDbManager
from database.models import Flow,FlowConfiguration,MetaData,MetaDataItem
from database.flow_configuration_db_manager import FlowConfigurationDBManager
from database.meta_data_db_manager import MetaDataDbManager
from database.meta_data_item_db_manager import MetaDataItemDbManager


class TestDbTmpDataOperation(unittest.TestCase):
    def test_create_site(self):
        id = SiteDbManager.add_site("bilibili","bilibili website")
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
        json_str = '''{"website":"https://www.bilibili.com","chrome_user_data_dir":["C","data","chrome"]}'''
        flow_configuration = FlowConfiguration(flow_id=1,config_name="bilibili",config_description="bilibili push video",config_json=json_str)
        FlowConfigurationDBManager.create_flow_configuration(flow_configuration)

    def test_create_metadata(self):
        #meta = MetaData(name="流程执行环境",code="flow_exe_env",description="flow execute environment metadata")
        #MetaDataDbManager.create_meta_data(meta=meta)

        meta = MetaData(name="流程任务订阅来源",code="sub_source",description="flow task subscription source metadata")
        MetaDataDbManager.create_meta_data(meta=meta)

    def test_create_metadata_item(self):
        # 执行环境元数据
        #meta_item_pl = MetaDataItem(meta_id=1,business_code="1",name_en="playwright",name_cn="无")
        #meta_item_yt = MetaDataItem(meta_id=1,business_code="2",name_en="ytdlp",name_cn="无")
        #MetaDataItemDbManager.create_meta_data_item(item=meta_item_pl)
        #MetaDataItemDbManager.create_meta_data_item(item=meta_item_yt)

        # 任务订阅来源元数据
        meta_item_job = MetaDataItem(meta_id=2,business_code="1",name_en="easyrpa_job_dispatch",name_cn="easyrpa inner job dispatch")
        MetaDataItemDbManager.create_meta_data_item(item=meta_item_job)

class TestDemoPullGithubWeb(unittest.TestCase):
    def test_create_site(self):
        id = SiteDbManager.add_site("demo","pull github web demo")
        print(id)

    def test_create_flow(self):
        request_check_script = """
from easyrpa.models.easy_rpa_exception import EasyRpaException
from easyrpa.enums.easy_rpa_exception_code_enum import EasyRpaExceptionCodeEnum
from easyrpa.enums.rpa_exe_result_code_enum import RpaExeResultCodeEnum
from easyrpa.models.scripty_exe_result import ScriptExeResult
import os
import json,jsonpickle

# 将json字符串转换为dict取值
standart = json.loads(os.environ.get("standard"),object_hook=dict)

if standart is None:
    raise EasyRpaException("rpa execution result is null",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,standart)

# 构建回执结果
status=standart.get("status")
error_msg=standart.get("error_msg")
data =standart.get("result")
code = "99999"

# 判断是否真正的拿到了数据
if data is not None and str(data).lower() == "true":
    status = True
    code = str(RpaExeResultCodeEnum.SUCCESS.value[1])
else:
    status = False
    code = str(RpaExeResultCodeEnum.FLOW_EXE_ERROR.value[1])

result = ScriptExeResult(status=status,error_msg=error_msg,print_str=None,result=data,code = code)

print(jsonpickle.encode(result))
"""
        request_adapt_script = """
import os
import json

# 将json字符串转换为dict取值
adapt_result = json.loads(os.environ.get("standard"),object_hook=dict)

config = json.loads(os.environ.get("flow_config"),object_hook=dict)
if config is not None and len(config) > 0:
    adapt_result["website"] = config.get("website")
    adapt_result["chrome_user_data_dir"] = config.get("chrome_user_data_dir")

# 必须保证key/value由双引号包裹，否则后续取值是问题
print(json.dumps(adapt_result))
"""
        flow_exe_script = """
import os
import json
from playwright.sync_api import sync_playwright
from yt_dlp import YoutubeDL

def download_video(standart: dict) -> str:
    result = None

    # 下载参数
    ops = {
        'format':'bv+ba/b',
        #'format':'bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4] / bv*+ba/b',
        'outtmpl':'%(title)s.%(ext)s'
    }

    info_dict = None
    with YoutubeDL(ops) as ydl:
        try:
            # 提取信息
            info_dict = ydl.extract_info(url=standart.get("webpage_url"), download=True)
        except Exception as e:
            # 处理任何异常
            print(f"download_video error: {e}")
    
    # duilder result
    if info_dict is not None:
        result = info_dict.get("title")+"."+info_dict.get("ext")
    return result

def upload_video(path:str,standart:dict) -> bool:
    if path is None or path == "":
        return False
    
    result = True

    dir = standart.get("chrome_user_data_dir")
    data_dir = f"{dir[0]}:\{dir[1]}\{dir[2]}"
    #print("check1")
    try:
        with sync_playwright() as playwright:
            #print("check2")
            # 持久化模式
            browser = playwright.chromium.launch_persistent_context(user_data_dir=data_dir,headless=False,channel="chrome")
            #print("check3")
            page = browser.pages[0]
            #print("check4")
            page.goto(standart.get("website"))
            #print("check5")

            # 进入上传页面
            page.wait_for_timeout(2000)
            #print("check6")
            with browser.expect_page() as new_page_info:
                #print("check7")
                page.get_by_text("投稿").click()
                #print("check8")
            #print("check9")
            new_page = new_page_info.value
            #print("check10")
    
            # 上传文件
            new_page.wait_for_timeout(2000)
            with new_page.expect_file_chooser() as fc_info:
                new_page.locator("css=div.bcc-upload-wrapper").click()
                file_chooser = fc_info.value
                file_chooser.set_files(path)
            
            # 点掉初始化提示
            try:
                new_page.wait_for_timeout(2000)
                new_page.get_by_role("button").filter(has_text="知道了").click()
            except:
                pass

            # 填写简介
            new_page.locator("css=div.ql-editor.ql-blank").first.fill(standart.get("title"))

            # 提交
            new_page.wait_for_timeout(10000)
            new_page.get_by_text("立即投稿").click()
            new_page.wait_for_timeout(5000)
            browser.close()
    except Exception as e:
        # 处理任何异常
        print(f"upload_video error: {e}")
        result = False
    finally:
        # 删除本地视频
        if os.path.exists(path):
            os.remove(path)
            print(f"The file {path} has been deleted.")
        else:
            print(f"The file {path} does not exist.")

    return result
    

def main():
    # 将json字符串转换为dict取值
    standart = json.loads(os.environ.get("standard"),object_hook=dict)

    # download video
    video_path = download_video(standart)
    if video_path is None:
       return

    # 上传视频
    result = upload_video(video_path,standart)
    print(result)

if __name__ =="__main__":
    main()
"""
        flow_result_handle_script = """
from easyrpa.models.easy_rpa_exception import EasyRpaException
from easyrpa.enums.easy_rpa_exception_code_enum import EasyRpaExceptionCodeEnum
from easyrpa.enums.rpa_exe_result_code_enum import RpaExeResultCodeEnum
from easyrpa.models.scripty_exe_result import ScriptExeResult
import os
import json,jsonpickle

# 将json字符串转换为dict取值
standart = json.loads(os.environ.get("standard"),object_hook=dict)

if standart is None:
    raise EasyRpaException("rpa execution result is null",EasyRpaExceptionCodeEnum.DATA_NULL.value[1],None,standart)

# 构建回执结果
status=standart.get("status")
error_msg=standart.get("error_msg")
data =standart.get("result")
code = "99999"

# 判断是否真正的拿到了数据
if data is not None and str(data).lower() == "true":
    status = True
    code = str(RpaExeResultCodeEnum.SUCCESS.value[1])
else:
    status = False
    code = str(RpaExeResultCodeEnum.FLOW_EXE_ERROR.value[1])

result = ScriptExeResult(status=status,error_msg=error_msg,print_str=None,result=data,code = code)

print(jsonpickle.encode(result))
"""

        FlowDbManager.update_flow(Flow(id=4
                                       ,request_check_script=request_check_script
                                       ,request_adapt_script=request_adapt_script
                                       ,flow_exe_script=flow_exe_script
                                       ,flow_result_handle_script=flow_result_handle_script))

        # new_flow = Flow(
        #      site_id=4,
        #      flow_code="push_bilibili_from_youtube_web",
        #      flow_name="push bilibili from youtube web",
        #      flow_rpa_type =1,
        #      flow_exe_env =1,
        #      flow_biz_type =2,
        #      max_retry_number =3,
        #      max_exe_time =300,
        #      retry_code = "10001",
        #      request_check_script = request_check_script,
        #      request_adapt_script = request_adapt_script,
        #      flow_exe_script = flow_exe_script,
        #      flow_result_handle_script = flow_result_handle_script
        #  )
        # id = FlowDbManager.create_flow(new_flow)
        # print(id)
        
    def test_create_flow_configuration(self):
        json_str = '''{"account":"123","password":"456"}'''
        flow_configuration = FlowConfiguration(flow_id=2,config_name="demo_config",config_description="pull github web demo config",config_json=json_str)
        FlowConfigurationDBManager.create_flow_configuration(flow_configuration)

