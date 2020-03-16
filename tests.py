import generator
import log_parser
import dir_parser
import json
import os
from helpers import _time

# проверка корректности функции read_file на автоматически сгенерированных логах
def read_file_gen():
    for name in ["small", "medium", "big"]:       # ToDo - all the log files in the folder
        path = "./test_files_generated/" + name

        t = _time(name + " - start")
        result = log_parser.read_file(path + ".log")
        _time(name + " - parsed", t)

        with open(path + ".groups", "r") as f:
            expected_result = f.readline()
            assert json.dumps(result, sort_keys=True) == expected_result, \
                "DIFFERNT GROUPS:\n" + json.dumps(result, sort_keys=True) + "\n" + expected_result
            # используется сравнение результатов как строк (а не как словарей),
            # поскольку если а - dict с ключами-int'ами, то json.loads( json.dumps(a) ) - dict с ключами-строками;
            # ToDO - use pickle

# read_file не падает при чтении образцов логов
def read_file_real():
    t = _time("real - start")
    for file_name in os.listdir("./test_files"):
        log_parser.read_file("./test_files/" + file_name)    # ToDo - use pathlib
    t = _time("real - parsed", t)

# read_dir не падает при чтении образцов логов
def read_dir_real():
    dir_parser.read_dir("./test_files/", 2)

def _merge_groups_internal(groups, expected_result):
    for i in range(1, len(groups)):
        dir_parser.merge_groups( groups[0], groups[i] )
    assert groups[0] == expected_result, \
        "DIFFERNT GROUPS:\n" + groups[0] + "\n" + expected_result

def merge_groups():
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
        _merge_groups_internal(groups, expected_result)

# в "настоящем" коде этих строк бы не было, но был бы специальный запускатель тестов
if __name__ == "__main__":
    read_file_gen()
    read_file_real()
    read_dir_real()
    merge_groups()
