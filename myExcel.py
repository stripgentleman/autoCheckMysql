import openpyxl


class MyExcel:
    def __init__(self, _path):
        self.table_column = 1
        self.name_column = 2
        self.type_column = 3
        self.only_column = 4
        self.null_column = 5
        self.index_column = 6
        self.exist_column = 7
        self._file_path = _path
        self._wxl = openpyxl.Workbook()
        self._sheet = self._wxl.create_sheet(title='err', index=0)
        self._sheet.cell(row=1, column=self.table_column).value = '表名'
        self._sheet.cell(row=1, column=self.name_column).value = '字段名'
        self._sheet.cell(row=1, column=self.type_column).value = '类型'
        self._sheet.cell(row=1, column=self.only_column).value = '唯一'
        self._sheet.cell(row=1, column=self.null_column).value = '为空'
        self._sheet.cell(row=1, column=self.index_column).value = '索引'
        self._sheet.cell(row=1, column=self.exist_column).value = '缺失性'

    def write(self, _err_data, _table_name):
        current_row = self._sheet.max_row + 1
        for _err_map in _err_data:
            for _err_param in _err_map.keys():
                self._sheet.cell(row=current_row, column=self.table_column).value = _table_name
                self._sheet.cell(row=current_row, column=self.name_column).value = _err_param
                for _err in _err_map[_err_param]:
                    if _err == 'type_err':
                        self._sheet.cell(row=current_row, column=self.type_column).value = _err_map[_err_param]['type_err']
                    if _err == 'is_only_err':
                        self._sheet.cell(row=current_row, column=self.only_column).value = _err_map[_err_param]['is_only_err']
                    if _err == 'is_null_err':
                        self._sheet.cell(row=current_row, column=self.null_column).value = _err_map[_err_param]['is_null_err']
                    if _err == 'index_err':
                        self._sheet.cell(row=current_row, column=self.index_column).value = _err_map[_err_param]['index_err']
                    if _err == 'exist':
                        self._sheet.cell(row=current_row, column=self.exist_column).value = _err_map[_err_param]['exist']
            current_row += 1

    def save(self):
        self._wxl.save(self._file_path)
        self._wxl.close()
