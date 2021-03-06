import random
import json

'''
При генерации используется какое-то количество hardcoded значений;
с одной стороны, от них хотелось бы избавиться, с другой - это усложнит чтение кода.
Я счел, что это неоднозначный вопрос, решающийся прочтением code policy компании, и (за отсутствием оного) оставил все как есть.
'''

def _coin():
    return random.randint(1,2) == 1

# генерирует логи за [days_num, days_num * 2] дней, с [lines_num, lines_num * 2] записями в каждом;
# возвращает словарь, содержащий ожидаемую группировку записей.
def generate_log(path, days_num, lines_num):
    groups = {"valid": {}, "non_valid": {}}
    with open(path + ".log", "w") as f:
        last = 10          # число, взятое с потолка; номер дня, для timestamp;
        for i in range( random.randint(days_num, days_num * 2) ):
            last = random.randint(last + 1, last * 2)       # генерация уникальных номеров дней
            timestamp = last * 3600 * 24
            groups["valid"]    [timestamp] = {"create": 0, "update": 0, "delete": 0}
            groups["non_valid"][timestamp] = {"create": 0, "update": 0, "delete": 0}
            is_zero = {"valid": True, "non_valid": True}    # нет представителей
            for i in range( random.randint(lines_num, lines_num * 2) ):
                event_type = random.sample( ["create", "update", "delete"], 1 )[0]
                is_valid = _coin()                          # валидная и невалидная строка равновероятны
                validness = "valid" if is_valid else "non_valid"
                is_zero[validness] = False
                groups[validness][timestamp][event_type] += 1
                f.write( generate_line(is_valid, event_type, timestamp) + "\n" )
            for validness, value in is_zero.items():
                if value:         # маловероятно при значительных lines_num
                    groups.remove(validness)

    with open(path + ".groups", "w") as f:
        f.write(json.dumps(groups, sort_keys=True))

# генерация запроса, подобного описанному в https://gist.github.com/onyxim/bb2d1828df741499d17ba97ad3319ef1
# запрос может быть невалидным, но число полей, типы значений и т.д. будут корректными
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
        ids_in_query = result["ids"].copy() + result["ids"][2:10].copy()        # все id, некоторые дважды
    else:
        if _coin():   # невалидный запрос - недостаток id
            ids_in_query = result["ids"][2:10].copy()
        else:         # невалидный запрос - избыток id
            ids_in_query = result["ids"].copy() + result["ids"][2:10].copy()    # все id, некоторые дважды
            ids_in_query.append( random.randint(result["ids"][-1] + 1,     result["ids"][-1] * 2) )
            ids_in_query.append( random.randint(result["ids"][-1] * 2 + 1, result["ids"][-1] * 4) )
        # бывают, конечно, и дургие невалидные запросы, но кажется достаточным проверить эти два вида
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

'''
if __name__ == "__main__":
    generate_log("./test_files_generated/small", 2, 5)
    generate_log("./test_files_generated/medium", 10, 200)
    generate_log("./test_files_generated/big", 50, 1000)
'''
