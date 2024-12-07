from easyrpa.tools.thread_pool_util import ThreadPoolUtil
from core import robot_manager_core,task_dispatch_core

def run_on_started():
    # check robot is closed
    ThreadPoolUtil.submit_task("easyrpa_common",robot_manager_core.closed_robot_check,params=123)
    # check waiting task
    ThreadPoolUtil.submit_task("easyrpa_common",task_dispatch_core.check_waiting_task,params=123)
