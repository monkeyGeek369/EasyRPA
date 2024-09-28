import unittest
from database.dispatch_job_db_manager import DispatchJobDBManager
from database.models import DispatchJob
from job import dispatch_job_manager

class DispatchJobTest(unittest.TestCase):
    def test_dispatch_job_create(self):
        job = DispatchJob(job_name='猴吉很忙youtube视频拉取',cron='0/10 0 0 * * *',flow_code='pull_youtube_web',flow_config_id=1,job_type=1)
        DispatchJobDBManager.create_dispatch_job(dispatch_job=job)

    def test_dispatch_job_update(self):
        job = DispatchJob(id=1,cron='*/10 * * * * *')
        DispatchJobDBManager.update_dispatch_job(data=job)

    def test_dispatch_job_exe(self):
        # search job
        job = DispatchJobDBManager.get_dispatch_job_by_id(id=1)
        # exe
        job_type_abc = dispatch_job_manager.get_job_type_impl(job_type=job.job_type)
        job_type_abc.execute_job(job=job)
