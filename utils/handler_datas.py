# 第一种:
# 将[{'check': 'status_code', 'expected':200, 'comparator': 'equals'}]
# 转化为 [{key: 'status_code', value: 200, comparator: 'equals', param_type: 'string'}],

# 第二种:
# 将[{'age': 18}, {'name': '马仔'}]
# 转化为 [{key: 'age', value: 18, param_type: 'int'}]

# 第三种:
# 将 [{'token': 'content.token'}]
# 转化为 [{key: 'token', value: 'content.token'}]

# 第四种:
# 将 {'User-Agent': 'Mozilla/5.0 KeYou'}
# 转化为 [{key: 'User-Agent', value: 'cMozilla/5.0 KeYou'}, {...}]

# 第五种:
# 将 ['${setup_hook_prepare_kwargs($request)}', '${setup_hook_httpntlmauth($request)}']
# 转化为 [{key: '${setup_hook_prepare_kwargs($request)}'}, {key: '${setup_hook_httpntlmauth($request)}'}]

# 第六种:
# 将 {'username': 'keyou', 'age': 18, 'gender': True}
# 转化为 [{key: 'username', value: 'keyou', param_type: 'string'}, {key: 'age', value: 18, param_type: 'int'}]
def handle_param_type(value):
    param_type = 'str'
    if isinstance(value, int):
        param_type = "int"
    elif isinstance(value, str):
        param_type = "str"
    elif isinstance(value, float):
        param_type = "float"
    elif isinstance(value, list):
        param_type = "list"
    elif isinstance(value, tuple):
        param_type = "tuple"
    elif isinstance(value, dict):
        param_type = "dict"
    elif isinstance(value, set):
        param_type = "set"
    return param_type


def handle_data1(datas):
    """
    [{'check': 'status_code', 'expected':200, 'comparator': 'equals'}]
    [{key: 'status_code', value: 200, comparator: 'equals', param_type: 'string'}]
    """
    data_list = []
    if datas is not None:
        for item in datas:
            key = item.get('check')
            value = item.get('expected')
            comparator = item.get('comparator')
            data_list.append({
                "key": key,
                "value": value,
                "comparator": comparator,
                "param_type": handle_param_type(value)
            })
    return data_list


def handle_data2(datas):
    """
    [{'age': 18}, {'name': '马仔'}]
    [{key: 'age', value: 18, param_type: 'int'}]
    """
    data_list = []
    if datas is not None:
        for item in datas:
            key = list(item)[0]
            value = item.get(key)
            data_list.append({
                "key": key,
                "value": value,
                "param_type": handle_param_type(value)
            })
    return data_list


def handle_data3(datas):
    """
    [{'token': 'content.token'}, {'Content-Type': 'application/json;charset=UTF-8'}]
    [{key: 'token', value: 'content.token'}]
    """
    data_list = []
    if datas is not None:
        for item in datas:
            key = list(item)[0]
            value = item.get(key)
            if isinstance(value, list):
                value = str(value)
            data_list.append({
                "key": key,
                "value": value,
            })
    return data_list


def handle_data4(datas):
    """
    {'User-Agent': 'Mozilla/5.0 KeYou'}
    [{key: 'User-Agent', value: 'cMozilla/5.0 KeYou'}, {...}]
    """
    data_list = []
    if datas is not None:
        for key, value in datas.items():
            data_list.append({
                "key": key,
                "value": value
            })
    return data_list


def handle_data5(datas):
    """
    ['${setup_hook_prepare_kwargs($request)}', '${setup_hook_httpntlmauth($request)}']
    [{key: '${setup_hook_prepare_kwargs($request)}'}, {key: '${setup_hook_httpntlmauth($request)}'}]
    """
    data_list = []
    if datas is not None:
        for item in datas:
            data_list.append({
                "key": item
            })
    return data_list


def handle_data6(datas):
    """
    {'username': 'keyou', 'age': 18, 'gender': True}
    [{key: 'username', value: 'keyou', param_type: 'string'}, {key: 'age', value: 18, param_type: 'int'}]
    """
    data_list = []
    if datas is not None:
        for key, value in datas.items():
            data_list.append({
                "key": key,
                "value": value,
                "param_type": handle_param_type(value)
            })
    return data_list


if __name__ == '__main__':
    data = [{'User-Agent': 'Mozilla/5.0 KeYou'}, {'Content-Type': 'application/json;charset=UTF-8'}]
    print(handle_data3(data))
