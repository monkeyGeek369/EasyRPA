from flask import Flask
from api.flow_task_api import flow_task_bp

# 注册flask应用
app = Flask(__name__)

# 注册蓝图
app.register_blueprint(flow_task_bp)