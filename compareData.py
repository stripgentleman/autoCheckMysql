import mysqlExecute
import myDocx


class DocxInfo:
    def __init__(self, document_path):
        self.docx_info = myDocx.MyDocx(document_path=document_path)
        self.table_info_list = self.docx_info.get_info_list()



'''
输出的docx信息格式：（依据数据字典模板1.2定）
{'table_name': 'report',
 'params': {'report_id': {'type': 'Int(8)','type_ori': 'Int(8)', 'is_null': 'n', 'is_only': 'y', 'is_index': 'y', 'is_null_ori': 'n', 'is_only_ori': 'y', 'is_index_ori': 'y', 'comment_ori': '自增主键id，从10000开始自增。系统生成的报告编号。', 'comment':'自增主键id，从10000开始自增。系统生成的报告编号。','default_ori': '',  'default':'',checked:'no'},
            'result': {'type': 'tinyint(1)','type_ori': 'Int(8)', 'is_null': 'n', 'is_only': 'n', 'is_index': 'n', 'is_null_ori': 'n', 'is_only_ori': 'y', 'is_index_ori': 'y', 'comment_ori': '巡检记录是n存在异常；系统自动生成，巡检结果；0正常，1异常', 'comment':'巡检记录是n存在异常；系统自动生成，巡检结果；0正常，1异常' 'default_ori': '0',  'default':'',checked:'no'},
            'creator': {'type': 'varchar(16)','type_ori': 'Int(8)', 'is_null': 'n', 'is_only': 'n', 'is_index': 'n', 'is_null_ori': 'n', 'is_only_ori': 'y', 'is_index_ori': 'y', 'comment_ori': '创建人', 'comment':'创建人' 'default_ori': '', 'default':'', checked:'no'},
            'create_time': {'type': 'timestamp','type_ori': 'Int(8)', 'is_null': 'n', 'is_only': 'n', 'is_index': 'n', 'is_null_ori': 'n', 'is_only_ori': 'y', 'is_index_ori': 'y', 'comment_ori': '创建时间', 'comment':'创建时间' 'default_ori': 'CURRENT_TIMESTAMP', 'default':'',checked:'no'},
            'updater': {'type': 'varchar(16)','type_ori': 'Int(8)', 'is_null': 'n', 'is_only': 'n', 'is_index': 'n', 'is_null_ori': 'n', 'is_only_ori': 'y', 'is_index_ori': 'y', 'comment_ori': '编辑人', 'comment':'编辑人' 'default_ori': '', 'default':'',checked:'no'},
            'update_time': {'type': 'timestamp','type_ori': 'Int(8)', 'is_null': 'n', 'is_only': 'n', 'is_index': 'n', 'is_null_ori': 'n', 'is_only_ori': 'y', 'is_index_ori': 'y', 'comment_ori': '编辑时间', 'comment':'编辑时间' 'default_ori': 'CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP', 'default':'',checked:'no'}}
'database_engine': 'InnoDB',
'default_charset': 'utf8',
'union_index_ori': 'Aaa(dsadsa,dsads),dsad_sa(dsads,dsadsa)',
'union_index': {'Aaa': ['dsads', 'dsadsa'], 'dsad_sa': ['dsads', 'dsadsa']}
}
'''


class MysqlInfo:
    def __init__(self, host=None, port=3306, user=None, password=None, db=None, charset='utf8'):
        self.mysql_info = mysqlExecute.MysqlExecute(host=host, port=port, user=user, password=password, db=db, charset=charset)

    '''
    get_table_info
    输出的mysql信息格式：（依据数据字典模板1.2定）
    {'param_info': {'id': {'type': 'int(11)', 'is_null': 'n', 'is_only': 'y', 'is_index': 'PRI', 'auto_increment': 'y', default:'', 'comment': '主键', checked:'no'},
                    'schedule_code': {'type': 'char(23)', 'is_null': 'n', 'is_only': 'y', 'is_index': 'UNI', default:'', 'comment': '排期编号 投放策略编号+3位数递增', checked:'no'},
                    'date': {'type': 'date', 'is_null': 'n', 'is_only': 'n', 'is_index': '', default:'', 'comment': '投放日期, checked:'no''},
                    'amount': {'type': 'varchar(11)', 'is_null': 'n', 'is_only': 'n', 'is_index': 'MUL', default:'', 'comment': '在该日期的投放量,单位次', checked:'no'},
                    'create_time': {'type': 'timestamp', 'is_null': 'n', 'is_only': 'n', 'is_index': '',  default:'','comment': '创建时间', checked:'no'},
                    'creator': {'type': 'varchar(32)', 'is_null': 'n', 'is_only': 'n', 'is_index': '', default:'', 'comment': '创建人', checked:'no'},
                    'update_time': {'type': 'timestamp', 'is_null': 'n', 'is_only': 'n', 'is_index': '', default:'', 'comment': '更新时间', checked:'no'},
                    'updater': {'type': 'varchar(32)', 'is_null': 'n', 'is_only': 'n', 'is_index': '', default:'', 'comment': '修改人', checked:'no'}, 
                    'test': {'type': 'geomcollection', 'is_null': 'n', 'is_only': 'n', 'is_index': 'MUL' default:'',}},
    'table_name': 'schedule_daily_schedule',
    'database_engine': 'InnoDB',
    'default_charset': 'utf8',
    'database_engine_ori': 'InnoDB',
    'default_charset_ori': 'utf8',
    'union_index_ori':'',
    'comment': '排期每日排期表'
    'union_index':{'PRIMARY_KEY': ['id', 'schedule_code'], 'schedule_code': ['schedule_code', 'amount']}
    }
    '''
    def get_table_info(self, table_name):
        return self.mysql_info.make_table_info(table_name)

    '''
    get_table_list
    输出的mysql信息格式:
    [table_name1, table_name2, ...]
    '''
    def get_table_list(self):
        return self.mysql_info.get_table_list()


if __name__ == '__main__':
    qq = MysqlInfo(host='127.0.0.1', user='root', password='123456', db='mytest')
    qq.get_table_info('schedule_daily_schedule')
