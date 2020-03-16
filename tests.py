import generator
import log_parser
import dir_parser
import json
from helpers import _time


# проверка корректности функции read_file на автоматически сгенерированных логах
def read_file_1():
    for name in ["small", "medium", "big"]:       # ToDo - all the log files in the folder
        path = "./test_files_generated/" + name

        pt = _time(name + " - start")
        result = log_parser.read_file(path + ".log")
        _time(name + " - parsed", pt)

        with open(path + ".groups", "r") as f:
            expected_result = f.readline()
            assert( json.dumps(result, sort_keys=True) == expected_result )
            # используется сравнение результатов как строк, поскольку если а - dict с ключами-int'ами,
            # то json.loads( json.dumps(a) ) - dict с ключами-строками;
            # ToDO - может, использовать вместо json что-то python-ориентированное?

def merge_groups_internal(groups, expected_result):
    for i in range(1, len(groups)):
        dir_parser.merge_groups( groups[0], groups[i] )
    assert( groups[0] == expected_result )

def merge_groups_1():
     # tuple of pairs (groups, expected_result)
    cases = (
        # 2 groups, no common keys
        ([ {"valid": {1: {"a":1, "b":2, "c":3}}},
           {"valid": {                          2: {"a":2, "b":4, "c":6}}} ],
           {"valid": {1: {"a":1, "b":2, "c":3}, 2: {"a":2, "b":4, "c":6}}} ),
        # 2 groups with a common key
        ([ {"valid": {1: {"a":1, "b":2, "c":3}}},
           {"valid": {1: {"a":2, "b":4, "c":6}}} ],
           {"valid": {1: {"a":3, "b":6, "c":9}}} ),
        # 3 groups
        ([ {"valid": {1: {"a":1, "b":2, "c":3}, 2: {"a":2, "b":4,  "c":6},  3: {"a":3,  "b":6,  "c":9 }}},
           {"valid": {                          2: {"a":4, "b":8,  "c":12}, 3: {"a":5,  "b":10, "c":15}}},
           {"valid": {                                                      3: {"a":6,  "b":12, "c":18}, 4: {"a":7, "b":14, "c":21}}} ],
           {"valid": {1: {"a":1, "b":2, "c":3}, 2: {"a":6, "b":12, "c":18}, 3: {"a":14, "b":28, "c":42}, 4: {"a":7, "b":14, "c":21}}} ),
    )
    for groups, expected_result in cases:
        merge_groups_internal(groups, expected_result)

# в "настоящем" коде этих строк бы не было, но был бы специальный запускатель тестов
if __name__ == "__main__":
    read_file_1()
    merge_groups_1()
