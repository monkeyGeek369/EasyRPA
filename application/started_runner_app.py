from easyrpa.tools.thread_pool_util import ThreadPoolUtil
from core import robot_manager_core

def run_on_started():
    # check robot is closed
    ThreadPoolUtil.submit_task("easyrpa_common",robot_manager_core.closed_robot_check,params=None)
