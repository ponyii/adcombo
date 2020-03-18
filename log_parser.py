import json
# import bicycle
# from helpers import _time

# Чтение файла лога, группировка запросов;
# ОСТРОЖНО, корректность лога не проверяется.
# узкие места - json.loads и is_valid.
def read_file(path):
    result = {"valid": {}, "non_valid": {}}
    with open(path, 'r') as f:
        for line in f:
            request = json.loads(line)        # может быть оптимизировано;
            # request = bicycle.loads(line)   # см. комментарий в bicycle.py
            validness = "valid" if is_valid(request) else "non_valid"
            timestamp = request["timestamp"] - request["timestamp"] % (3600 * 24)                 # начало дня
            if timestamp not in result[validness]:
                result[validness][timestamp] = {"create": 0, "update": 0, "delete": 0}
            result[validness][timestamp][ request["event_type"] ] += 1

    return result

# Определяет валидность запроса (переданного как dict);
# ОСТРОЖНО, корректность аргумента не проверяется.
def is_valid(request):
    expected_ids = set( request["ids"] )
    query_ids = set()
    q = request["query_string"]
    prefix = "id="

    left = 0
    while True:
        left = q.find(prefix, left)
        if left == -1:      # no more ids
            break
        elif left == 0 or q[left - 1] == "&":
            right = q.find("&", left)
            if right == -1:
                right = len(q)
            id = int(q[left + len(prefix) : right])       # от конвертации можно избавиться, если читать ids запроса как массив строк
            # id = q[left + len(prefix) : right]          # см. комментарий в bicycle.py

            if id not in expected_ids:         # обработка найденного id
                return False
            query_ids.add(id)

            left = right + 1
        else:      # another key ends with `id`
            left += 1
    return len(expected_ids) == len(query_ids)
