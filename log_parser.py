import json

def read_file(path):
    result = {"valid": {}, "non_valid": {}}

    # ToDo - посмотреть на альтернативные способы чтения файлов
    f = open(path, 'r')        # предполагаю, что число файлов значительно превышает число доступных потоков, так что потоку можно отдать файл целиком
    while True:
        line = f.readline()    # ToDo - стоит считывать пачками
        if len(line) == 0:
            break

        is_valid, timestamp, event_type = parse_token( json.loads(line) ) # ToDo - process json.decoder.JSONDecodeError
                                                                          # json.loads, очевидно, совершает избыточное число проверок, и для конкретного вида логов можно написать более быстрый парсер;
                                                                          # но добиться большей скорости (при сохранении хоть какой-то проверки корректности), используя python, мне не удалось.
        validness = "valid" if is_valid else "non_valid"
        timestamp -= timestamp % (3600 * 24)                 # начало дня
        if timestamp not in result[validness]:
            result[validness][timestamp] = {"create": 0, "update": 0, "delete": 0}
        result[validness][timestamp][event_type] += 1

    f.close()
    return result

# @token - запрос (dict), описанный в https://gist.github.com/onyxim/bb2d1828df741499d17ba97ad3319ef1
# @returns (is_valid, timestamp, event_type)
def parse_token(token):
    if not isinstance(token, dict):   # ToDo - check keys and types of values
        raise Exception("Invalid token")

    ids = set( token["ids"] )         # дубликацию чисел в token["ids"] считаем допустимой
    query_ids = set()
    for el in token["query_string"].split("&"):          # я предполагаю, что query_string не очень велики, и обрабатывать их "по частям" не имеет смысла
        if len(el) > 0:
            pair = el.split("=")
            if (len(pair) != 2):                         # я считаю query_string валидной, если она содержит &-separated записи вида "<что угодно>=<что угодно>"
                raise Exception("Invalid query_string")  # скорее всего, ограничение на используемые символы должно быть более жестким
            if pair[0] == "id":
                tmp = int(pair[1])
                if tmp not in ids:                       # ToDo - process ValueError
                    return False, token["timestamp"], token["event_type"]
                query_ids.add(tmp)
    return len(ids) == len(query_ids), token["timestamp"], token["event_type"]
