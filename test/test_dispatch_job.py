import unittest
from database.dispatch_job_db_manager import DispatchJobDBManager
from database.models import DispatchJob
from job import dispatch_job_manager

class DispatchJobTest(unittest.TestCase):
    def test_dispatch_job_create(self):
        job = DispatchJob(job_name='bilibili_monkeygeek_push_video',cron='0 45 22,23 * * *',flow_code='push_bilibili_from_youtube_web',flow_config_id=3,job_type=2)
        DispatchJobDBManager.create_dispatch_job(dispatch_job=job)

    def test_dispatch_job_update(self):
        job = DispatchJob(id=1,cron='0 0 22,23 * * *')
        DispatchJobDBManager.update_dispatch_job(data=job)

    def test_dispatch_job_exe(self):
        # search job
        job = DispatchJobDBManager.get_dispatch_job_by_id(id=2)
        # exe
        job_type_abc = dispatch_job_manager.get_job_type_impl(job_type=job.job_type)
        job_type_abc.execute_job(job=job)
