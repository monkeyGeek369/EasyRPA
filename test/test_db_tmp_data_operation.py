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



