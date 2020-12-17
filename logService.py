import logging
import traceback
from configuration import Configuration


# # logSaveFlag：是否开启log保存，True保存，False不保存
# logSaveFlag=True
# # logFileNameValue：log文件名
# logFileNameValue=autoCheckMysql.log
# # onlyOnceLogFlag：是否只存储最近一次运行的log，True为只存储最近一次运行的log，False为每次运行的log都存储在log文件
# onlyOnceLogFlag=True
# # logLevelValue：设置log等级，默认DEBUG
# logLevelValue=DEBUG
# # logFormatterValue：设置log存储格式，模式可参考logging模块的原生format格式
# logFormatterValue=%(asctime)s - %(levelname)s %(filename)s[line:%(lineno)d] - %(funcName)s: %(message)s

class LogService:
    config = Configuration().doc_config_dict

    def __init__(self):
        self.log_enable = None
        self.log_file_name = None
        self.only_save_once = None
        self.log_level = None
        self.log_format = None
        self.config_init()

    def config_init(self):
        self.log_enable = self.config['logSaveFlag']
        self.log_file_name = self.config['logFileNameValue']
        self.only_save_once = self.config['onlyOnceLogFlag']
        self.log_level = self.config['logLevelValue']
        self.log_format = self.config['logFormatterValue']

