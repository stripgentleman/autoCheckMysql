import docx
import re


class MyDocx:
    def __init__(self, document_path):
        self.document = docx.Document(document_path)

    def get_text(self):
        text = self.document.text
        return text

    def get_table_list(self):
        table_list = self.document.tables
        return table_list

    @staticmethod
    def _get_table_all_rows(table):
        rows = table.rows
        return rows

    @staticmethod
    def _get_table_all_columns(table):
        columns = table.columns
        return columns

    @staticmethod
    def get_table_cell(table, row=None, column=None):
        if row is not None and column is not None:

            ret_cell = table.cell(row_idx=row, col_idx=column).text
            # all_rows = MyDocx._get_table_all_rows(table)
            # ret_cell = all_rows[row].cells[column].text
        elif row is not None and column is None:
            ret_cell = list()
            all_rows = MyDocx._get_table_all_rows(table)
            for cell in all_rows[row].cells:
                ret_cell.append(cell.text)
        elif row is None and column is not None:
            ret_cell = list()
            all_columns = MyDocx._get_table_all_columns(table)
            for cell in all_columns[column].cells:
                ret_cell.append(cell.text)
        else:
            ret_cell = None
        return ret_cell

    @staticmethod
    def check_table_sql(table):
        check_flag = MyDocx.get_table_cell(table=table, row=-3, column=1)
        # print(table._column_count)
        # cell_idx = 1 + (-2 * table._column_count)
        # print(cell_idx)
        # for cell in MyDocx.get_table_cell(table=table, row=0):
        #     print(cell)

        if check_flag == 'InnoDB':
            return True
        print(check_flag)
        return False

    @staticmethod
    def get_sql_table_list(table_list):
        sql_table_list = list()
        count = 0
        for table in table_list:
            if len(MyDocx._get_table_all_rows(table)) < 5:
                continue
            count += 1
            try:
                if MyDocx.check_table_sql(table=table):
                    sql_table_list.append(table)
            except:
                print('Error in table:' + str(MyDocx.get_table_cell(table=table, row=-3, column=1)) + u'表识别错误')
        return sql_table_list

    @staticmethod
    def get_table_info(table):
        if table is None:
            return None
        flag = True
        row = 1
        table_info = dict()
        # print(table)
        table_name = MyDocx.get_table_cell(table=table, row=-4, column=1)
        table_info['table_name'] = table_name
        table_info['params'] = dict()
        column_names = MyDocx.get_table_cell(table, row=0)
        name_num = 0
        type_num = 0
        null_num = 0
        only_num = 0
        index_num = 0
        comment_num = 0
        current_column = 0
        default_num = 0
        for column_name in column_names:
            if column_name.startswith(u'字段名'):
                name_num = current_column
            if column_name.startswith(u'字段类型'):
                type_num = current_column
            if column_name.startswith(u'空') or column_name.startswith(u'为空'):
                null_num = current_column
            if column_name.startswith(u'唯一'):
                only_num = current_column
            if column_name.startswith(u'索引'):
                index_num = current_column
            if column_name.startswith(u'COMMENT'):
                comment_num = current_column
            if column_name.startswith(u'默认值'):
                default_num = current_column
            current_column += 1
        try:
            while flag:
                param_map = dict()
                name = MyDocx.get_table_cell(table=table, row=row, column=name_num)
                param_map['type'] = MyDocx.get_table_cell(table=table, row=row, column=type_num).lower()
                is_null = MyDocx.get_table_cell(table=table, row=row, column=null_num).replace(' ', '').lower()
                if is_null == '是' or is_null == 'y' or is_null == 'yes':
                    param_map['is_null'] = 'y'
                else:
                    param_map['is_null'] = 'n'
                param_map['is_null_ori'] = MyDocx.get_table_cell(table=table, row=row, column=null_num).replace(' ', '')
                is_only = MyDocx.get_table_cell(table=table, row=row, column=only_num).replace(' ', '')
                if is_only == '是' or is_only == 'y' or is_only == 'yes':
                    param_map['is_only'] = 'y'
                else:
                    param_map['is_only'] = 'n'
                param_map['is_only_ori'] = MyDocx.get_table_cell(table=table, row=row, column=null_num).replace(' ', '')
                is_index = MyDocx.get_table_cell(table=table, row=row, column=index_num).replace(' ', '').lower()
                if is_index == '是' or is_index == 'y' or is_index == 'yes':
                    param_map['is_index'] = 'y'
                elif is_index == 'pri' or is_index == 'uni' or is_index == 'mul':
                    param_map['is_index'] = is_index.upper()
                else:
                    param_map['is_index'] = 'n'
                param_map['is_index_ori'] = MyDocx.get_table_cell(table=table, row=row, column=null_num).replace(' ', '')

                param_map['comment'] = MyDocx.get_table_cell(table=table, row=row, column=comment_num)
                if param_map['comment'] is None:
                    param_map['comment'] = ''
                if default_num != 0:
                    param_map['default'] = MyDocx.get_table_cell(table=table, row=row, column=default_num)
                table_info['params'][str(name)] = param_map
                row += 1
                # print(table_name)
                # print(name_num)
                # print(MyDocx.get_table_cell(table=table, row=row, column=name_num))
                if MyDocx.get_table_cell(table=table, row=row, column=0).startswith(u'数据'):
                    flag = False
            table_info['database_engine'] = MyDocx.get_table_cell(table=table, row=-3, column=1).lower()
            table_info['default_charset'] = MyDocx.get_table_cell(table=table, row=-2, column=1).lower()
            table_info['database_engine_ori'] = MyDocx.get_table_cell(table=table, row=-3, column=1)
            table_info['default_charset_ori'] = MyDocx.get_table_cell(table=table, row=-2, column=1)
            table_info['union_index_ori'] = MyDocx.get_table_cell(table=table, row=-1, column=1)
            table_info['union_index'] = dict()
            if len(table_info['union_index_ori']) > 3:
                key_name_list = re.findall('([A-z_0-9]+)\(', table_info['union_index_ori'])
                key_pos = 0
                for key_name in key_name_list:
                    table_info['union_index'][key_name] = list()
                    params_str_lists = re.findall('\(([A-z_,0-9]+)\)', table_info['union_index_ori'])
                    table_info['union_index'][key_name] = str(params_str_lists[key_pos]).split(',')
                    key_pos += 1
        except:
            print(str(table_name) + u'数据读取错误')
            table_info = None
        # print(table_info)
        return table_info

    def get_info_list(self):
        sql_table_list = self.get_sql_table_list(self.get_table_list())
        info_list = list()
        for sql_table in sql_table_list:
            # print(sql_table)
            table_info = self.get_table_info(sql_table)
            info_list.append(table_info)
        return info_list


if __name__ == '__main__':
    # my = MyDocx('./广告业务后台-数据字典.docx')
    my = MyDocx('./运维管理系统项目-数据字典V1.0.docx')
    tl = my.get_info_list()
    for t in tl:
        print(t)




