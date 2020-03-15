import random
import json

def _coin():
    return random.randint(1,2) == 1

# генерирует логи за [days_num, days_num * 2] дней, с [lines_num, lines_num * 2] записями в каждый;
# возвращает словарь, содержащий корректную группировку записей.
def generate_log(path, days_num, lines_num):
    f = open(path, "w")

    groups = {"valid": {}, "non_valid": {}}
    last = 10
    for i in range( random.randint(days_num, days_num * 2) ):
        last = random.randint(last + 1, last * 2)       # генерация уникальных номеров дней
        timestamp = last * 3600 * 24
        groups["valid"]    [timestamp] = {"create": 0, "update": 0, "delete": 0}
        groups["non_valid"][timestamp] = {"create": 0, "update": 0, "delete": 0}
        for i in range( random.randint(lines_num, lines_num * 2) ):
            event_type = random.sample( ["create", "update", "delete"], 1 )[0]
            is_valid = _coin()                # валидная и невалидная строка равновероятны
            validness = "valid" if is_valid else "non_valid"
            groups[validness][timestamp][event_type] += 1
            f.write( generate_line(is_valid, event_type, timestamp) )
        # ToDo - check if groups[validness][timestemp] is empty

    f.close()
    return groups

def generate_line(is_valid, event_type, timestamp):
    result = {}
    result["event_type"] = event_type
    result["timestamp"] = timestamp + random.randint(0, 3600 * 24 - 1)

    # генерация 10-20 различных id
    result["ids"] = []
    last = 1
    for i in range( random.randint(10, 20) ):
        result["ids"].append( random.randint(last, last*2) )
        last = result["ids"][-1] + 1

    # составление списка id для query_string
    ids_in_query = []
    if is_valid:
        ids_in_query = result["ids"].copy() + result["ids"][2:10].copy()
    else:
        if _coin():   # нехватка id
            ids_in_query = result["ids"][2:10].copy()
        else:         # избыток id
            ids_in_query = result["ids"].copy() + result["ids"][2:10].copy()
            ids_in_query.append( random.randint(result["ids"][-1] + 1,     result["ids"][-1] * 2) )
            ids_in_query.append( random.randint(result["ids"][-1] * 2 + 1, result["ids"][-1] * 4) )
    random.shuffle( ids_in_query )

    # составление query_string
    result["query_string"] = ""
    i = 0
    while i < len(ids_in_query):
        if _coin():
            result["query_string"] += "fake=fake_value&"
        else:
            result["query_string"] += "id=" + str( ids_in_query[i] ) + "&"
            i += 1

    return json.dumps(result)


# print( json.dumps( generate_line(True, "delete", 0), sort_keys=True, indent=4 ) )
# print( json.dumps( generate_line(False, "delete", 3600 * 24),  sort_keys=True, indent=4 ) )
# print( json.dumps( generate_log("./test_files_generated/0.log", 10, 10), sort_keys=True, indent=4  ) )
