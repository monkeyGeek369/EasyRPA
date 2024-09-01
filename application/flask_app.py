from flask import Flask

# 注册flask应用
app = Flask(__name__)

# 注册蓝图
#app.register_blueprint(agent_core_bp)