import json
import re
# from helpers import _time

# узкие места - json.loads и is_valid
def read_file(path):
    result = {"valid": {}, "non_valid": {}}
    with open(path, 'r') as f:
        for line in f:
            request = json.loads(line)   # json.loads, очевидно, совершает избыточное число проверок, и для запросов можно написать более быстрый парсер;
                                         # но добиться существенно большей скорости, используя python, мне не удалось.
                                         # ToDO - поищи другие готовые парсеры
            validness = "valid" if is_valid(request) else "non_valid"
            timestamp = request["timestamp"] - request["timestamp"] % (3600 * 24)                 # начало дня
            if timestamp not in result[validness]:
                result[validness][timestamp] = {"create": 0, "update": 0, "delete": 0}
            result[validness][timestamp][ request["event_type"] ] += 1

    return result

# @request - запрос (dict), описанный в https://gist.github.com/onyxim/bb2d1828df741499d17ba97ad3319ef1
# @returns (is_valid, timestamp, event_type)
# корректность аргумента не проверяется
# узкие места - findall и обработка substr
def is_valid(request):
    expected_ids = set( request["ids"] )
    query_ids = set()
    for substr in re.findall(r'&id=\d*|^id=\d*', request["query_string"]):    # естественно использовать finditer, чтобы не рассматривать часть строк до конца, но findall быстрее;
        id = int(substr[ substr.find("id=") + len("id=") : ])
        if id not in expected_ids:
            return False
        query_ids.add(id)
    return len(expected_ids) == len(query_ids)
