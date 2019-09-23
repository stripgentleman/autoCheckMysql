import docx


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
            ret_cell = table.rows[row].cells[column].text
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
        check_flag = MyDocx.get_table_cell(table=table, row=-2, column=0)
        if check_flag == '数据库引擎':
            return True
        # print(check_flag)
        return False

    @staticmethod
    def get_sql_table_list(table_list):
        sql_table_list = list()
        count = 0
        for table in table_list:
            count += 1
            try:
                if MyDocx.check_table_sql(table=table):
                    sql_table_list.append(table)
            except:
                print('Error in table:' + u'第' + str(count) + u'个表识别错误')
        return sql_table_list

    @staticmethod
    def get_table_info(table):
        if table is None:
            return None
        flag = True
        row = 1
        table_info = dict()
        table_name = MyDocx.get_table_cell(table=table, row=-3, column=1)
        table_info['table_name'] = table_name
        table_info['params'] = dict()
        column_names = MyDocx.get_table_cell(table, row=0)
        name_num = 0
        type_num = 0
        null_num = 0
        only_num = 0
        index_num = 0
        desc_num = 0
        current_column = 0
        for column_name in column_names:
            if column_name.startswith(u'字段名'):
                name_num = current_column
            if column_name.startswith(u'字段类型'):
                type_num = current_column
            if column_name.startswith(u'空'):
                null_num = current_column
            if column_name.startswith(u'唯一'):
                only_num = current_column
            if column_name.startswith(u'索引'):
                index_num = current_column
            if column_name.startswith(u'注释'):
                desc_num = current_column
            current_column += 1
        while flag:
            param_map = dict()
            name = MyDocx.get_table_cell(table=table, row=row, column=name_num)
            param_map['type'] = MyDocx.get_table_cell(table=table, row=row, column=type_num)
            param_map['is_null'] = MyDocx.get_table_cell(table=table, row=row, column=null_num)
            param_map['is_only'] = MyDocx.get_table_cell(table=table, row=row, column=only_num)
            param_map['is_index'] = MyDocx.get_table_cell(table=table, row=row, column=index_num)
            param_map['desc'] = MyDocx.get_table_cell(table=table, row=row, column=desc_num)
            table_info['params'][str(name)] = param_map
            row += 1
            if MyDocx.get_table_cell(table=table, row=row, column=0).startswith(u'数据库'):
                flag = False
        return table_info

    def get_info_list(self):
        sql_table_list = self.get_sql_table_list(self.get_table_list())
        info_list = list()
        for sql_table in sql_table_list:
            table_info = self.get_table_info(sql_table)
            info_list.append(table_info)
        return info_list


if __name__ == '__main__':
    my = MyDocx('./test.docx')
    tl = my.get_info_list()
    for t1 in tl:
        print(t1)



