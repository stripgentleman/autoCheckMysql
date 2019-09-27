from mysqlExecute import MysqlExecute
from myDocx import MyDocx
import pymysql
import myExcel
import time


def _update_index_info( _table_index):
    index_info = dict()
    for _key in _table_index:
        if _key['Column_name'] not in index_info.keys():
            index_info[_key['Column_name']] = dict()
        index_info[_key['Column_name']]['is_index'] = 'y'
        if _key['Non_unique'] == 0 or _key['Non_unique'] == '0':
            index_info[_key['Column_name']]['is_only'] = 'y'
        else:
            index_info[_key['Column_name']]['is_only'] = 'n'
        if _key['Null'] == 'YES':
            index_info[_key['Column_name']]['is_null'] = 'y'
        else:
            index_info[_key['Column_name']]['is_null'] = 'n'


def check(_table_info, _desc):
    if _desc is None:
        return False
    _check_res = list()
    _check_flag = False
    for param in _desc:
        if param['Field'] in _table_info['params'].keys():
            type_flag = _table_info['params'][param['Field']]['type'] == param['Type']
            key_flag = check_key(_param=param, _table_info=_table_info)
            null_flag = check_null(_param=param, _table_info=_table_info)
            index_flag = check_index(_param=param, _table_info=_table_info)
            _check_flag = type_flag and key_flag and null_flag and index_flag
            param['checked'] = 'yes'
            _table_info['params'][param['Field']]['checked'] = 'yes'
            if _check_flag is False:
                err_map = dict()
                err_map[param['Field']] = dict()
                if type_flag is False:
                    err_map[param['Field']]['type_err'] = u'数据字典：' + str(_table_info['params'][param['Field']]['type']) + u'  数据库：' + str(param['Type'])
                if key_flag is False:
                    err_map[param['Field']]['is_only_err'] = u'数据字典：' + str(_table_info['params'][param['Field']]['is_only']) + u'  数据库：' + str(param['Key'])
                if null_flag is False:
                    err_map[param['Field']]['is_null_err'] = u'数据字典：' + str(_table_info['params'][param['Field']]['is_null']) + u'  数据库：' + str(param['Null'])
                if index_flag is False:
                    err_map[param['Field']]['index_err'] = u'数据字典：' + str(_table_info['params'][param['Field']]['is_index']) + u'  数据库：' + str(param['Key'])
                _check_res.append(err_map)
        if 'checked' not in param.keys():
            err_map = dict()
            err_map[param['Field']] = dict()
            err_map[param['Field']]['exist'] = u'数据字典缺失字段'
            _check_res.append(err_map)
    for param_name in _table_info['params'].keys():
        if 'checked' not in _table_info['params'][param_name].keys():
            err_map = dict()
            err_map[param_name] = dict()
            err_map[param_name]['exist'] = u'数据库缺失字段'
            _check_res.append(err_map)
    return _check_res


def check_key(_param, _table_info):
    if _param['Key'] == 'PRI' or _param['Key'] == 'UNI':
        if _table_info['params'][_param['Field']]['is_only'] == 'y':
            return True
        else:
            return False
    elif _param['Key'] == '' or _param['Key'] == 'MUL':
        if _table_info['params'][_param['Field']]['is_only'] == 'n' or _table_info['params'][_param['Field']]['is_only'] == '':
            return True
        else:
            return False
    return False


def check_null(_param, _table_info):
    if _table_info['params'][_param['Field']]['is_null'] == 'n' and _param['Null'] == 'NO':
        return True
    elif _table_info['params'][_param['Field']]['is_null'] == 'y' and _param['Null'] == 'YES':
        return True
    else:
        return False


def check_index(_param, _table_info):
    if _param['Key'] == 'PRI' or _param['Key'] == 'UNI' or _param['Key'] == 'MUL':
        if _table_info['params'][_param['Field']]['is_index'] == 'y' \
                or _table_info['params'][_param['Field']]['is_index'] == u'主键' \
                or _table_info['params'][_param['Field']]['is_index'] == _param['Key']:
            return True
        else:
            return False
    else:
        if _param['Key'] == '':
            if _table_info['params'][_param['Field']]['is_index'] == 'n' or _table_info['params'][_param['Field']]['is_index'] == '':
                return True
            else:
                return False
        return False


def check_run(_database, _docx):
    filename = round(time.time())
    excel = myExcel.MyExcel('./' + str(filename) + '.xlsx')
    desc = None
    table_info_list = _docx.get_info_list()
    for table_info in table_info_list:
        table_name = table_info['table_name']
        try:
            desc = _database.get_desc(table_name=table_name)
        except pymysql.err.ProgrammingError as err:
            print(err)
            continue
        check_err = check(_table_info=table_info, _desc=desc)
        excel.write(check_err, table_name)
        excel.save()


if __name__ == '__main__':
    mysql = MysqlExecute(host='', user='root', password='test', db='')
    data_info = MyDocx('./test.docx')
    check_run(_database=mysql, _docx=data_info)


