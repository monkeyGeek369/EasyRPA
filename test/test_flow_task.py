import unittest
from core.flow_manager_core import flow_task_subscribe
from easyrpa.models.flow.flow_task_subscribe_dto import FlowTaskSubscribeDTO

class TestFlowTask(unittest.TestCase):
    def test_flow_task(self):
        message = '''{"message_key1":666,"message_key2":"mkv2","message_key3":{"mk1":"mkv1","mk2":908,"mk3":[5,6,9],"mk4":{"mmk1":784},"mk5":[{"mmk51":333,"mm52":"32"}]},"message_key4":[{"mk41":369,"mk42":"963"}]}'''
        flow_task_subscribe_dto = FlowTaskSubscribeDTO(flow_id=1
                                                       ,flow_configuration_id=1
                                                       ,biz_no="123"
                                                       ,sub_source=1
                                                       ,request_standard_message=message)
        flow_task_subscribe(flow_task_subscribe_dto)

    def test_demo_pull_github_web_task(self):
        message = '''{"home_url":"https://github.com","login_url":"https://github.com/login","search_key":"playwright"}'''
        flow_task_subscribe_dto = FlowTaskSubscribeDTO(flow_id=3
                                                       ,flow_code=''
                                                       ,flow_configuration_id=2
                                                       ,biz_no="123"
                                                       ,sub_source=1
                                                       ,request_standard_message=message)
        flow_task_subscribe(flow_task_subscribe_dto)

    def test_pull_youtube_web_task(self):
        message = '''{}'''
        flow_task_subscribe_dto = FlowTaskSubscribeDTO(flow_id=1
                                                       ,flow_configuration_id=1
                                                       ,flow_code=''
                                                       ,biz_no="123456"
                                                       ,sub_source=1
                                                       ,request_standard_message=message)
        flow_task_subscribe(flow_task_subscribe_dto)