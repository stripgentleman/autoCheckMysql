# from mysqlExecute import MysqlExecute
# from myDocx import MyDocx
from compareData import MysqlInfo
from compareData import DocxInfo
from configuration import Configuration

import pymysql
import myExcel
import time


def check(_doc_table_info, _database_table_info):
    doc_config = Configuration().doc_config_dict
    if _database_table_info is None:
        return False
    _check_res = list()
    err_map = dict()
    err_map['table'] = dict()
    err_map['params'] = dict()
    _check_flag = False
    database_params_info = _database_table_info['param_info']
    doc_params_info = _doc_table_info['params']
    for param_name in database_params_info:
        if param_name in doc_params_info.keys():
            type_flag = doc_params_info[param_name]['type'] == database_params_info[param_name]['type']
            key_flag = check_only(_database_param_info=database_params_info[param_name], _doc_param_info=doc_params_info[param_name])
            null_flag = check_null(_database_param_info=database_params_info[param_name], _doc_param_info=doc_params_info[param_name])
            index_flag = check_index(_database_param_info=database_params_info[param_name], _doc_param_info=doc_params_info[param_name])
            default_flag = check_default(_database_param_info=database_params_info[param_name], _doc_param_info=doc_params_info[param_name])
            comment_flag = check_comment(_database_param_info=database_params_info[param_name], _doc_param_info=doc_params_info[param_name])
            _check_flag = type_flag and key_flag and null_flag and index_flag and default_flag and comment_flag
            database_params_info[param_name]['checked'] = 'yes'
            doc_params_info[param_name]['checked'] = 'yes'
            if _check_flag is False:
                err_map['params'][param_name] = dict()
                if type_flag is False:
                    err_map['params'][param_name]['type_err'] = u'数据字典：' + str(doc_params_info[param_name]['type_ori']) + u'  数据库：' + str(database_params_info[param_name]['type'])
                if key_flag is False:
                    err_map['params'][param_name]['is_only_err'] = u'数据字典：' + str(doc_params_info[param_name]['is_only_ori']) + u'  数据库：' + str(database_params_info[param_name]['is_only'])
                if null_flag is False:
                    err_map['params'][param_name]['is_null_err'] = u'数据字典：' + str(doc_params_info[param_name]['is_null_ori']) + u'  数据库：' + str(database_params_info[param_name]['is_null'])
                if index_flag is False:
                    err_map['params'][param_name]['index_err'] = u'数据字典：' + str(doc_params_info[param_name]['is_index_ori']) + u'  数据库：' + str(database_params_info[param_name]['is_index'])
                if default_flag is False:
                    err_map['params'][param_name]['default_err'] = u'数据字典：' + str(doc_params_info[param_name]['default_ori']) + u'  数据库：' + str(database_params_info[param_name]['default'])
                if comment_flag is False:
                    err_map['params'][param_name]['comment_err'] = u'数据字典：' + str(doc_params_info[param_name]['comment_ori']) + u'  数据库：' + str(database_params_info[param_name]['comment'])
    for param_name in database_params_info.keys():
        if 'checked' not in database_params_info[param_name].keys():
            err_map['params'][param_name] = dict()
            err_map['params'][param_name]['exist'] = u'数据字典缺失字段'
    for param_name in doc_params_info.keys():
        if 'checked' not in doc_params_info[param_name].keys():
            err_map['params'][param_name] = dict()
            err_map['params'][param_name]['exist'] = u'数据库缺失字段'

    database_engine_flag = True
    union_index_flag = True
    default_charset_flag = True
    if doc_config['tableEngineFlag']:
        database_engine_flag = database_engine_check(_database_table_info=_database_table_info, _doc_table_info=_doc_table_info)
    if doc_config['unionIndexFlag']:
        union_index_flag = union_index_check(_database_table_info=_database_table_info, _doc_table_info=_doc_table_info)
    if doc_config['tableDefaultCharsetFlag']:
        default_charset_flag = default_charset_check(_database_table_info=_database_table_info, _doc_table_info=_doc_table_info)

    if database_engine_flag is False or union_index_flag is False or default_charset_flag is False:
        if database_engine_flag is False:
            err_map['table']['database_engine_err'] = u'数据字典：' + str(_doc_table_info['database_engine_ori']) + u'  数据库：' + str(_database_table_info['database_engine'])
        if union_index_flag is False:
            err_map['table']['union_index_err'] = u'数据字典：' + str(_doc_table_info['union_index_ori']) + u'  数据库：' + str(_database_table_info['union_index_ori'])
        if default_charset_flag is False:
            err_map['table']['default_charset_err'] = u'数据字典：' + str(_doc_table_info['default_charset']) + u'  数据库：' + str(_database_table_info['default_charset'])
    return err_map


def union_index_check(_database_table_info, _doc_table_info):
    if len(_database_table_info['union_index'].keys()) != len(_doc_table_info['union_index'].keys()):
        return False
    else:
        for key_name in _database_table_info['union_index']:
            if key_name not in _doc_table_info['union_index']:
                return False
            if len(_database_table_info['union_index'][key_name]) != len(_doc_table_info['union_index'][key_name]):
                return False
            for param in _database_table_info['union_index'][key_name]:
                if param not in _doc_table_info['union_index'][key_name]:
                    return False
        return True


def default_charset_check(_database_table_info, _doc_table_info):
    if _database_table_info['default_charset'] == _doc_table_info['default_charset']:
        return True
    return False


def database_engine_check(_database_table_info, _doc_table_info):
    if _database_table_info['database_engine'] == _doc_table_info['database_engine']:
        return True
    return False


def check_only(_database_param_info, _doc_param_info):
    if _database_param_info['is_only'] == _doc_param_info['is_only']:
        return True
    return False


def check_null(_database_param_info, _doc_param_info):
    if _database_param_info['is_null'] == _doc_param_info['is_null']:
        return True
    return False


def check_index(_database_param_info, _doc_param_info):
    if _database_param_info['is_index'] == _doc_param_info['is_index']:
        return True
    elif _database_param_info['is_index'] == 'PRI' or _database_param_info['is_index'] == 'MUL' or _database_param_info['is_index'] == 'UNI':
        if _doc_param_info['is_index'] == 'y':
            return True
        else:
            return False
    else:
        return False


def check_default(_database_param_info, _doc_param_info):
    if _database_param_info['default'] == '' and _doc_param_info['default'] == 'EMPTY STRING':
        return True
    # if _database_param_info['default'] == 'NULL' and _doc_param_info['default'] == '':
    #     return True
    if _database_param_info['default'] == _doc_param_info['default']:
        return True
    return False


def check_comment(_database_param_info, _doc_param_info):
    if _database_param_info['comment'] == _doc_param_info['comment']:
        return True
    # print(_doc_param_info['comment'])
    # print(_database_param_info['comment'])
    return False


def check_run(_database, _doc):
    # print(_database.get_table_list())
    # print(_doc.table_info_list)
    filename = round(time.time())
    excel = myExcel.MyExcel('./' + str(filename) + '.xlsx')
    table_info_list = _doc.table_info_list
    # print(table_info_list)
    for doc_table_info in table_info_list:
        if doc_table_info is None:
            continue
        table_name = doc_table_info['table_name']
        try:
            table_info = _database.get_table_info(table_name=table_name)

        except pymysql.err.Error as err:
            print(err)
            continue
        check_err = check(_doc_table_info=doc_table_info, _database_table_info=table_info)
        # print(check_err)
        excel.col_write(check_err, table_name)
        excel.save()


if __name__ == '__main__':
    mysql_info = MysqlInfo(host='172.20.4.235', user='root', password='test', db='addatasys')
    # docx_info = DocxInfo('C:/Users/测试/Desktop/广告业务/广告业务后台/document/3.0/概要设计/广告业务后台-数据字典.docx')
    docx_info = DocxInfo('./addatasys.docx')
    # for aa in docx_info.table_info_list:
    #     print(aa)
    # print(docx_info)
    check_run(_database=mysql_info, _doc=docx_info)
