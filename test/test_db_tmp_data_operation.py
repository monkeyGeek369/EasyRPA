import unittest
from database.site_db_manager import SiteDbManager
from database.flow_db_manager import FlowDbManager
from database.models import Flow


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
