class Config():
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

    # 定时任务配置
    JOBS = [
        {
            'id': 'set_flag',   # 重置数据库flag
            'func': 'app.main.func:set_flag',
            'args': None,
            'trigger': {
                'type': 'cron', 
                'day_of_week': "0-6",	
                'hour': '14',	
                'minute': '09'
            }
        },{
            'id': 'at_all',     # 定时@全体
            'func': 'app.main.func:at_all',
            'args': None,
            'trigger': {
                'type': 'cron', 
                'day_of_week': "0-6",	
                'hour': '08',	
                'minute': '00'
            }
        },{
            'id': 'auto_remind',     # 自动提醒打卡
            'func': 'app.main.func:auto_remind',
            'args': None,
            'trigger': {
                'type': 'cron', 
                'day_of_week': "0-6",	
                'hour': '22',	
                'minute': '00'
            }
        },{
            'id': 'name_list',     # 自动提醒打卡
            'func': 'app.main.func:name_list',
            'args': None,
            'trigger': {
                'type': 'cron', 
                'day_of_week': "0-6",	
                'hour': '21',	
                'minute': '59'
            }
        }
    ]

    @staticmethod
    def init_app():
        pass

class DevelopmentConfig(Config):
    DEBUG = False,
    SQLALCHEMY_DATABASE_URI = 'mysql://root:password@localhost/test2'

class ProductionConfig(Config):
    DEBUG = True,
    SQLALCHEMY_DATABASE_URI = 'mysql://root:password@localhost/QQRobot'

config = {
    'Development': DevelopmentConfig,
    'Production0': ProductionConfig,
    'default': DevelopmentConfig
}