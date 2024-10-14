from application import flask_app
import atexit
from job.dispatch_job_manager import init_APSchedulerTool

# 初始化定时任务
scheduler_tool = init_APSchedulerTool()

# 注册job调度shutdown
atexit.register(scheduler_tool.shutdown)

if __name__ == '__main__':
    flask_app.run(host='0.0.0.0', port=50003, debug=True,use_reloader=False)
    
