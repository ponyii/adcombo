import json

def read_file(path):
    result = {"valid": {}, "non_valid": {}}

    f = open(path, 'r')        # предполагаю, что число файлов значительно превышает число доступных потоков, так что потоку можно отдать файл целиком
    while True:
        line = f.readline()    # ToDo - стоит считывать пачками
        if len(line) == 0:
            break

        is_valid, timestamp, event_type = parse_token( json.loads(line) ) # ToDo - process json.decoder.JSONDecodeError
                                                                          # ToDo - json.loads стоит заменить на велосипед, заточенный под конкретные сообщения и более быстрый
        validness = "valid" if is_valid else "non_valid"
        timestamp -= timestamp % (3600 * 24)                 # начало дня
        if timestamp not in result[validness]:
            result[validness][timestamp] = {"create": 0, "update": 0, "delete": 0}
        result[validness][timestamp][event_type] += 1

    f.close()
    return result

# returns (is_valid, timestamp, event_type)
def parse_token(token):
    if not isinstance(token, dict):   # ToDo - check keys and types of values
        raise Exception("Invalid token")

    ids = set( token["ids"] )   # дубликацию чисел в token["ids"] считаем допустимой
    ids_num = 0
    for el in token["query_string"].split("&"):    # я предполагаю, что query_string не очень велики, и обрабатывать их "по частям" не имеет смысла
        if len(el) > 0:
            pair = el.split("=")
            if (len(pair) != 2):                         # я считаю query_string валидной, если она содержит &-separated записи вида "<что угодно>=<что угодно>"
                raise Exception("Invalid query_string")  # скорее всего, ограничение на используемые символы должно быть более жестким
            if pair[0] == "id":
                ids_num += 1
                if int(pair[1]) not in ids or len(ids) < ids_num:  # ToDo - process ValueError
                    return False, token["timestamp"], token["event_type"]
    return len(ids) == ids_num, token["timestamp"], token["event_type"]


print(json.dumps( read_file("./test_files/0.log"), sort_keys=True, indent=4 ))
