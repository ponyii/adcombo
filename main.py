import json

def read_file(path):
    result = {"valid": {}, "non_valid": {}}

    f = open(path, 'r')
    while True:
        line = f.readline()
        if len(line) == 0:
            break

        is_valid, timestamp, event_type = parse_token( json.loads(line) ) # ToDo - process json.decoder.JSONDecodeError
        validness = "valid" if is_valid else "non_valid"
        if timestamp not in result[validness]:
            result[validness][timestamp] = {"create": 0, "update": 0, "delete": 0}
        result[validness][timestamp][event_type] += 1

    f.close()
    return result

# returns (is_valid, timestamp, event_type)
def parse_token(token):
    if not isinstance(token, dict):   # ToDo - check keys and types of values
        raise Exception("Invalid token")

    ids = set()
    for el in token["query_string"].split("&"):
        if len(el) > 0:
            pair = el.split("=")
            if (len(pair) != 2):
                raise Exception("Invalid query_string")
            if pair[0] == "id":
                ids.add( int(pair[1]) )       # ToDo - process ValueError
    return ids == set(token["ids"]), token["timestamp"], token["event_type"]

print(json.dumps( read_file("./test_files/0.log"), sort_keys=True, indent=4 ))
