import json
import re



def find_key_in_json(key_to_find, json_obj, path=None):
    """
    Ищет ключ в JSON и сохраняет иерархию путей до него.

    :param key_to_find: Ключ, который нужно найти.
    :param json_obj: JSON объект для поиска.
    :param path: Текущий путь к ключу в JSON.
    :return: Список путей к найденным ключам.
    """
    paths = []
    if path is None:
        path = []

    if isinstance(json_obj, dict):
        for k, v in json_obj.items():
            new_path = path + [k]
            if k == key_to_find:
                paths.append(new_path)
            elif isinstance(v, (dict, list)):
                paths.extend(find_key_in_json(key_to_find, v, new_path))

    elif isinstance(json_obj, list):
        for i, item in enumerate(json_obj):
            new_path = path + [str(i)]
            if isinstance(item, (dict, list)) and key_to_find in item:
                paths.append(new_path + [key_to_find])

    return paths



def get_nested_value(data_dict, keys):
    current_level = data_dict

    for key in keys:
        if isinstance(current_level, dict):
            if key in current_level:
                current_level = current_level[key]

        elif isinstance(current_level, list):
            if int(key) in range(len(current_level)):
                current_level = current_level[int(key)]
        else:
            return None 
        
    return current_level



def custom_filter(item, key, values):
    paths = find_key_in_json(key, item)
    if paths:
        for path in paths:
            if any(re.search(value, get_nested_value(item, path), re.IGNORECASE) for value in values):
                return True
    return False


def complex_filter(filename, first_param, second_param):
    param_1, target_1 = first_param
    param_2, target_2 = second_param

    try:
        with open(filename, encoding='utf-8') as f:
            data = json.load(f)
    except json.decoder.JSONDecodeError:
            data = {}
    filtered_by_first_param  = list(filter(lambda item: custom_filter(item, param_1, target_1 ), data))
    filtered_by_second_param = list(filter(lambda item: custom_filter(item, param_2, target_2 ), filtered_by_first_param ))
    return filtered_by_second_param



if __name__ == "__main__":
    res = complex_filter('00499.json', ('КодОКВЭД', ['62.']), ("НаимРегион", ['Калуж']))


