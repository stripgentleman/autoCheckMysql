import pymysql
# import MyDocx


class MysqlExecute:
    def __init__(self, host=None, port=3306, user=None, password=None, db=None, charset='utf8'):
        self.db_connection = pymysql.connect(host=host, port=port, user=user, password=password, db=db, charset=charset)
        self.db_cursor = self.db_connection.cursor()
        self.set_cursor_dict()

    def set_cursor_dict(self):
        self.db_cursor = self.db_connection.cursor(cursor=pymysql.cursors.DictCursor)

    def set_cursor_tuple(self):
        self.db_cursor = self.db_connection.cursor()

    def db_execute(self, sql_str=None):
        self.db_cursor.execute(sql_str)
        ret = self.db_cursor.fetchall()
        return ret

    def get_desc(self, table_name):
        return self.db_execute('desc ' + str(table_name))

    def get_index(self, table_name):
        return self.db_execute('show index from ' + str(table_name))


if __name__ == '__main__':
    qq = MysqlExecute(host='172.20.4.235', user='root', password='test', db='addatasys')
    qq.set_cursor_dict()
    print(qq.get_index('strategy_draft'))

