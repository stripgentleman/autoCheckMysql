import pymysql
import re
# import MyDocx


class MysqlExecute:
    def __init__(self, host=None, port=3306, user=None, password=None, db=None, charset='utf8'):
        self.db_connection = pymysql.connect(host=host, port=port, user=user, password=password, db=db, charset=charset)
        self.db_cursor = self.db_connection.cursor()
        self.set_cursor_dict()
        self.db_name = db

    def set_cursor_dict(self):
        self.db_cursor = self.db_connection.cursor(cursor=pymysql.cursors.DictCursor)

    def set_cursor_tuple(self):
        self.db_cursor = self.db_connection.cursor()

    def db_execute(self, sql_str=None):
        self.db_cursor.execute(sql_str)
        ret = self.db_cursor.fetchall()
        return ret

    def get_desc(self, table_name):
        # print('desc `' + str(table_name) + '`')
        return self.db_execute('desc `' + str(table_name) + '`')

    def get_index(self, table_name):
        # print('show index from `' + str(table_name) + '`')
        return self.db_execute('show index from `' + str(table_name) + '`')

    def get_create_table(self, table_name):
        # print('show create table `' + table_name + '`')
        return self.db_execute('show create table `' + table_name + '`')

    def make_table_info(self, table_name):
        ret_info = dict()
        ret_info['union_index'] = dict()
        ret_info['union_index_ori'] = ''
        create_str = str(self.get_create_table(table_name)[0]['Create Table'])
        create_str_list = self.get_brackets_contents_for_str(create_str, 1)
        params_create_str = create_str_list[0]
        post_create_str = create_str_list[2]
        params_desc = params_create_str.split('\n')
        temp_index = 0
        for temp in params_desc:
            if temp == '' or temp == ' ':
                params_desc.pop(temp_index)
                temp_index += 1
                continue
            if temp[-1] != ',':
                params_desc[temp_index] += ','
            temp_index += 1

        table_info = self.get_param_info_from_create_str(params_desc)

        for key_type in table_info[0]:
            if key_type == 'PRI':
                if len(table_info[0][key_type]['params_name']) > 1:
                    ret_info['union_index']['PRIMARY_KEY'] = list()
                    ret_info['union_index_ori'] += 'PRIMARY_KEY('
                    for param in table_info[0][key_type]['params_name']:
                        ret_info['union_index']['PRIMARY_KEY'].append(param)
                        ret_info['union_index_ori'] += param
                        ret_info['union_index_ori'] += ','
                    ret_info['union_index_ori'] = ret_info['union_index_ori'][:-1]+'),'
                for pri_col in table_info[0][key_type]['params_name']:
                    table_info[1][pri_col]['is_only'] = 'y'
                    table_info[1][pri_col]['is_index'] = 'PRI'
            else:
                for key_name in table_info[0][key_type]:
                    if len(table_info[0][key_type][key_name]['params']) > 1:
                        ret_info['union_index'][key_name] = list()
                        ret_info['union_index_ori'] += key_name
                        ret_info['union_index_ori'] += '('
                        for param in table_info[0][key_type][key_name]['params']:
                            ret_info['union_index'][key_name].append(param)
                            ret_info['union_index_ori'] += param
                            ret_info['union_index_ori'] += ','
                        ret_info['union_index_ori'] = ret_info['union_index_ori'][:-1] + '),'
                    for col_name in table_info[0][key_type][key_name]['params']:
                        table_info[1][col_name]['is_index'] = key_type
                        if table_info[1][col_name]['is_only'] == 'n':
                            table_info[1][col_name]['is_only'] = table_info[0][key_type][key_name]['is_only']
                        if table_info[1][col_name]['is_only'] == 'y':
                            continue
        ret_info['param_info'] = table_info[1]
        ret_info['table_name'] = table_name
        ret_info['database_engine'] = re.findall('ENGINE=([A-z0-9]+) ', post_create_str)[0].lower()
        ret_info['default_charset'] = re.findall('DEFAULT CHARSET=([A-z0-9]+) ', post_create_str)[0].lower()
        ret_info['union_index_ori'] = ret_info['union_index_ori'][:-1]
        ret_info['comment'] = ''
        if len(re.findall('COMMENT=\'(.*)\'', post_create_str)) > 1:
            ret_info['comment'] = re.findall('COMMENT=\'(.*)\'', post_create_str)[0]
        return ret_info

        # print(params_desc[-2])

    def get_table_list(self):
        ori_table_list = self.db_execute('show tables')
        table_list = list()
        for table in ori_table_list:
            table_list.append(table['Tables_in_' + self.db_name])
        return table_list

    @staticmethod
    def get_param_info_from_create_str(_str_list):
        param_info = dict()
        index_info = dict()
        for current_str in _str_list:
            pre_char = ''
            current_word = ''
            start_end_flag = False
            omitted_flag = False  # 省略判断flag
            name_flag = False  # 反引号flag
            brackets_flag = False
            word_list = list()
            for current_char in current_str:
                if current_char == '`' and pre_char != '\\' and pre_char != '(':
                    name_flag = not name_flag
                    # start_end_flag = not start_end_flag
                    pre_char = current_char
                    # continue
                if current_char == '\'' and pre_char != '\\':
                    omitted_flag = not omitted_flag
                    # print(omitted_flag)
                    start_end_flag = not start_end_flag
                    # print(start_end_flag)
                    pre_char = current_char
                    # continue
                if omitted_flag is False:
                    if current_char == ')':
                        brackets_flag = False
                    if brackets_flag is False:
                        if current_char != ' ' and current_char != '' and current_char != ',' and current_char != '`' and current_char != '\'':
                            start_end_flag = True
                        if current_char == ' ' or current_char == '' or (current_char == ',' and pre_char == ')') or (current_char == ',' and pre_char != '`'):
                        # if current_char == ' ' or current_char == '' or (current_char == ',' and pre_char == ')'):
                            start_end_flag = False
                    if current_char == '(':
                        brackets_flag = True
                if start_end_flag:
                    current_word += current_char
                pre_char = current_char
                if start_end_flag is False and current_word != '' and current_word != ' ':
                    word_list.append(current_word)
                    # print(current_word)
                    current_word = ''
            if '`'in word_list[0]:
                param_name = word_list[0].replace('`', '')
                param_info[param_name] = dict()
                param_info[param_name]['type'] = word_list[1]
                param_info[param_name]['is_null'] = 'y'
                param_info[param_name]['is_only'] = 'n'
                param_info[param_name]['is_index'] = 'n'
                param_info[param_name]['default'] = ''
                param_info[param_name]['comment'] = ''
                not_flag = False
                default_flag = False
                comment_flag = False
                for word in word_list[2:]:
                    if word == 'unsigned':
                        param_info[param_name]['type'] += ' unsigned'
                        continue
                    if word == 'NOT':
                        not_flag = True
                        continue
                    if word == 'DEFAULT':
                        default_flag = True
                        continue
                    if word == 'COMMENT':
                        comment_flag = True
                        continue
                    if word == 'AUTO_INCREMENT':
                        param_info[param_name]['auto_increment'] = 'y'
                        continue
                    if comment_flag:
                        param_info[param_name]['comment'] = word.replace('\'', '')
                        default_flag = False
                        continue
                    if default_flag:
                        param_info[param_name]['default'] = word.replace('\'', '')
                        default_flag = False
                        continue
                    if not_flag:
                        param_info[param_name]['is_null'] = 'n'
                        not_flag = False
                        continue
            if word_list[0] + word_list[1] == 'PRIMARYKEY':
                if 'PRI' not in index_info:
                    index_info['PRI'] = dict()
                index_info['PRI']['params_name'] = word_list[2].replace('(', '').replace(')', '').replace('`', '').split(',')
                if 'USING' in word_list:
                    # print(word_list)
                    index_info['PRI']['__type__'] = word_list[word_list.index('USING')+1]
            if word_list[0] == 'KEY':
                if 'MUL' not in index_info:
                    index_info['MUL'] = dict()
                    # index_info['MUL']['params_name'] = dict()
                key_name = word_list[1].replace('`', '')
                index_info['MUL'][key_name] = dict()
                index_info['MUL'][key_name]['is_only'] = 'n'
                index_info['MUL'][key_name]['params'] = word_list[2].replace('(', '').replace(')', '').replace('`', '').split(',')
                if 'USING' in word_list:
                    index_info['MUL'][key_name]['__type__'] = word_list[word_list.index('USING') + 1]
            if word_list[0] + word_list[1] == 'UNIQUEKEY':
                params_list = word_list[3].replace('(', '').replace(')', '').replace('`', '').split(',')
                if len(params_list) > 1:
                    index_type = 'MUL'
                else:
                    index_type = 'UNI'
                if index_type not in index_info:
                    index_info[index_type] = dict()
                    # index_info[index_type]['params_name'] = dict()
                key_name = word_list[2].replace('`', '')
                index_info[index_type][key_name] = dict()
                index_info[index_type][key_name]['is_only'] = 'y'
                index_info[index_type][key_name]['params'] = params_list
                if 'USING' in word_list:
                    index_info[index_type][key_name]['__type__'] = word_list[word_list.index('USING') + 1]
            if word_list[0] + word_list[1] == 'SPATIALKEY' or word_list[0] + word_list[1] == 'FULLTEXTKEY':
                index_type = 'MUL'
                if index_type not in index_info:
                    index_info[index_type] = dict()
                    # index_info[index_type]['params_name'] = dict()
                key_name = word_list[2].replace('`', '')
                index_info[index_type][key_name] = dict()
                index_info[index_type][key_name]['is_only'] = 'n'
                index_info[index_type][key_name]['params'] = word_list[3].replace('(', '').replace(')', '').replace('`', '').split(',')
                if 'USING' in word_list:
                    index_info[index_type][key_name]['__type__'] = word_list[word_list.index('USING') + 1]
        # print(param_info)
        return index_info, param_info

    @staticmethod
    def get_brackets_contents_for_str(_str, level):
        if level < 0:
            return None
        current_level = 0
        pre_char = ''
        res_str = ''
        pre_str = ''
        pre_flag = True
        post_str = ''
        post_flag = False
        omitted_flag = False    # 省略判断flag
        for current_char in _str:
            if omitted_flag is False:
                if current_char == ')' and pre_char != '\\':
                    # print(pre_char)
                    current_level -= 1
                    if current_level < level:
                        # print(post_flag)
                        post_flag = True
            if current_char == '\'' and pre_char != '\\':
                omitted_flag = not omitted_flag
            if current_level >= level:
                res_str += current_char
            if omitted_flag is False:
                if current_char == '(' and pre_char != '\\':
                    current_level += 1
                    if current_level == level:
                        pre_flag = False
                # if current_char == ')':
                #     current_level -= 1
            if current_level < level:
                if pre_flag:
                    pre_str += current_char
                if post_flag:
                    post_str += current_char
            pre_char = current_char
        # print(post_str)
        # print(pre_str)
        post_str += ' '
        return res_str, pre_str, post_str


if __name__ == '__main__':
    qq = MysqlExecute(host='127.0.0.1', user='root', password='123456', db='mytest')
    # qq.set_cursor_dict()
    # print(qq.get_create_table('schedule_daily_schedule'))
    print(qq.make_table_info('schedule_daily_schedule'))
    # print(qq.get_desc('schedule_daily_schedule'))
    # print('\'')
    # print(qq.get_table_list())
