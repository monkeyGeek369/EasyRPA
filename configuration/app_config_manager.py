import configparser

class AppConfigManager:

    def get_app_config(self):
        config = configparser.ConfigParser()
        config.read('configuration/app_config.ini')
        app = config['app']
        return app
    
    def get_flow_exe_env_meta_code(self) -> str:
        return self.get_app_config()['flow_exe_env_meta_code']