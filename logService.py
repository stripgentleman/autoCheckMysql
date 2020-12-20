import logging
import traceback
from configuration import Configuration
import sys



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
    INFO = logging.INFO
    ERROR = logging.ERROR
    DEBUG = logging.DEBUG
    WARNING = logging.WARNING
    CRITICAL = logging.CRITICAL
    NOTSET = logging.NOTSET
    FATAL = logging.FATAL

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

    def log_for_call_method(self, log_level):
        def log_method(fun):
            def make_log(*args, **kwargs):
                if self.log_enable:
                    params = ''
                    for arg in args:
                        params += f'{arg},'
                    for kwarg in kwargs:
                        params += f'{kwarg}={kwargs[kwarg]},'
                    self.log(fun.__qualname__ + f'({params[:-1]})执行', log_level)
                    try:
                        fun(*args, **kwargs)
                    except Exception as e:
                        # ttype, tvalue, ttraceback = sys.exc_info()
                        # traceback_str = ''
                        # for traceback_info in traceback.format_exception(ttype, tvalue, ttraceback):
                        #     traceback_str += traceback_info
                        # print(ttype, tvalue, end="\n")
                        # i = 1
                        # while ttraceback:
                        #     print("第{}层堆栈信息".format(i))
                        #     tracebackCode = ttraceback.tb_frame.f_code
                        #     print("文件名：{}".format(tracebackCode.co_filename))
                        #     print("函数或者模块名：{}".format(tracebackCode.co_name))
                        #     ttraceback = ttraceback.tb_next
                        #     i += 1
                        # 等效
                        self.log(fun.__qualname__ + f'({params[:-1]})' + "调用出错，错误信息如下：\n" + traceback.format_exc(), self.ERROR)
                        raise e
                    self.log(fun.__qualname__ + f'({params[:-1]})执行结束', log_level)
            return make_log
        return log_method

    def log(self,message,level):
        print(message)

    # def init_log_setting(self, ):




if __name__ == '__main__':
    logger = LogService()

    @logger.log_for_call_method('DEBUG')
    def aaa(c,d):
        print(c/d)


    # aaa(c=1,b=0)

    class a:
        @logger.log_for_call_method('DEBUG')
        def b(self,bb):
            print(bb)

        @staticmethod
        @logger.log_for_call_method('DEBUG')
        def c(cc):
            print(cc)

    test = a()
    ll = list([1,2,3])
    test.b(ll)
    test.c('222222')
