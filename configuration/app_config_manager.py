import configparser

class AppConfigManager:

    def get_app_config(self):
        config = configparser.ConfigParser()
        config.read('configuration/app_config.ini', encoding='utf-8')
        app = config['app']
        return app
    
    def get_flow_exe_env_meta_code(self) -> str:
        return self.get_app_config()['flow_exe_env_meta_code']
    
    def get_flow_task_sub_source_meta_code(self) -> str:
        return self.get_app_config()['flow_task_sub_source_meta_code']
    
    def get_flow_task_sub_source_inner_job_dispatch_name_en(self) -> str:
        return self.get_app_config()['flow_task_sub_source_inner_job_dispatch_name_en']
    
    def get_scheduler_type(self) -> str:
        return self.get_app_config()['scheduler_type']
    
    def get_executors_default_thread_pool_max_workers(self) -> int:
        return self.get_app_config()['executors_default_thread_pool_max_workers']
    
    def get_executors_default_process_pool_max_workers(self) -> int:
        return self.get_app_config()['executors_default_process_pool_max_workers']
    
    def get_job_default_coalesce(self) -> bool:
        return self.get_app_config()['job_default_coalesce']
    
    def get_job_default_max_instances(self) -> int:
        return self.get_app_config()['job_default_max_instances']
    
    def get_job_default_misfire_grace_time(self) -> int:
        return self.get_app_config()['job_default_misfire_grace_time']
    
    def get_job_timezone(self) -> str:
        return self.get_app_config()['job_timezone']
    
    def get_jobstores_default(self) -> str:
        return self.get_app_config()['jobstores_default']
    
    def isRegisterJobOnAppStart(self) -> bool:
        config_str = str(self.get_app_config()['register_dispatch_job_on_app_startup']).lower()
        return False if config_str == 'false' else True
    
    def get_console_default_conda_env(self) -> str:
        return self.get_app_config()['console_default_conda_env']