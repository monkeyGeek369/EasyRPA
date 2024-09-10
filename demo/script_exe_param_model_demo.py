# 本demo用于展示如何获取ScriptExeParamModel对象、如何取值
from easyrpa.models.base.script_exe_param_model import ScriptExeParamModel
import os

print(os.environ.get("ACSVCPORT"))