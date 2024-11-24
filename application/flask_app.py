from flask import Flask
from api.flow_task_api import flow_task_bp
from api.job_api import job_api_bp
from api.site_api import site_api_bp
from api.flow_config_api import flow_config_api_bp
from api.meta_data_api import meta_data_api_bp
from api.meta_data_item_api import meta_data_item_api_bp
from api.flow_api import flow_api_bp
from api.job_record_api import job_record_api_bp

# 注册flask应用
app = Flask(__name__)

# 注册蓝图
app.register_blueprint(flow_task_bp)
app.register_blueprint(job_api_bp)
app.register_blueprint(site_api_bp)
app.register_blueprint(flow_config_api_bp)
app.register_blueprint(meta_data_api_bp)
app.register_blueprint(meta_data_item_api_bp)
app.register_blueprint(flow_api_bp)
app.register_blueprint(job_record_api_bp)