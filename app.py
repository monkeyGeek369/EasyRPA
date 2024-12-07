from application import flask_app
import atexit
from job.dispatch_job_manager import init_APSchedulerTool
from application import base_app,started_runner_app

# 初始化定时任务
scheduler_tool = init_APSchedulerTool()

# 注册job调度shutdown
atexit.register(scheduler_tool.shutdown)
# 初始化线程池
base_app.init_thread_pool()
# 注册线程池shutdown
atexit.register(base_app.shutdown_thread_pool)

# run on app started
started_runner_app.run_on_started()

if __name__ == '__main__':
    flask_app.run(host='0.0.0.0', port=5003, debug=True,use_reloader=False)
    
