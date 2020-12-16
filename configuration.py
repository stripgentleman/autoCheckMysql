

class Configuration:
    STATIC_FLAG = '[static]'
    DOC_FLAG = '[doc]'
    MYSQL_FLAG = '[mysql]'
    EXCEL_FLAG = '[excel]'
    CONFIG_FILE = './config'
    FLAG_METHOD = [
        ('[doc]', 'get_doc_config'),
        ('[excel]', 'get_excel_config'),
        ('[mysql]', 'get_mysql_config'),
        ('[log]', 'get_log_config'),
    ]

    def __init__(self):
        self.doc_config_dict = dict()
        self.mysql_config_dict = dict()
        self.excel_config_dict = dict()
        self.log_config_dict = dict()
        self.init_config_dict()

    def init_config_dict(self):
        flag = Configuration.STATIC_FLAG
        config_file = open(Configuration.CONFIG_FILE, encoding='utf8')
        for config_str in config_file:
            config_str = config_str.replace('\n', '').replace('\r', '')
            if len(config_str) < 2:
                continue
            if config_str[0] == '#':
                continue
            if config_str[0] == '[':
                flag = Configuration.set_flag(config_str)
                continue
            for flag_method in Configuration.FLAG_METHOD:
                if flag == flag_method[0]:
                    fun = getattr(self, flag_method[1])
                    fun(config_str)

    def get_doc_config(self, config_str):
        config_list = config_str.split('=')
        if str(config_list[0])[-4:] == 'Flag':
            if config_list[1] == 'True':
                self.doc_config_dict[config_list[0]] = True
            elif config_list[1] == 'False':
                self.doc_config_dict[config_list[0]] = False
            else:
                print('配置信息错误(应该是True或False)：' + config_list[0] + '=' + config_list[1] + '\n')
                return False
        if str(config_list[0])[-6:] == 'Column':
            if config_list[1].isdigit():
                self.doc_config_dict[config_list[0]] = int(config_list[1])
            else:
                print('配置信息错误(应该int型正整数)：' + config_list[0] + '=' + config_list[1] + '\n')
                return False
        if str(config_list[0])[-5:] == 'Value':
            self.doc_config_dict[config_list[0]] = config_list[1]
        if str(config_list[0])[-8:] == 'Position':
            position_list = config_list[1].replace('(', '').replace(')', '').split(',')
            for num in position_list:
                if num.lstrip('-').isdigit():
                    self.doc_config_dict[config_list[0]] = dict()
                    self.doc_config_dict[config_list[0]]['row'] = position_list[0]
                    self.doc_config_dict[config_list[0]]['col'] = position_list[1]
                else:
                    print('配置信息错误(应该int型整数坐标)：' + config_list[0] + '=' + config_list[1] + '\n')
                    return False

    def get_mysql_config(self, config_str):
        return None

    def get_excel_config(self, config_str):
        return None

    def get_log_config(self, config_str):
        config_list = config_str.split('=')
        if str(config_list[0])[-4:] == 'Flag':
            if config_list[1] == 'True':
                self.doc_config_dict[config_list[0]] = True
            elif config_list[1] == 'False':
                self.doc_config_dict[config_list[0]] = False
            else:
                print('配置信息错误(应该是True或False)：' + config_list[0] + '=' + config_list[1] + '\n')
                return False
        if str(config_list[0])[-5:] == 'Value':
            self.doc_config_dict[config_list[0]] = config_list[1]

    @staticmethod
    def set_flag(config_str):
        return config_str


if __name__ == '__main__':
    aa = Configuration()
    print(aa.doc_config_dict)
