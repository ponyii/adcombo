import log_parser
import dir_parser
import json
import os
from helpers import _time
from multiprocessing import cpu_count

# Проверка корректности функции log_parser.read_file на автоматически сгенерированных логах;
# фактически именно здесь проверяется log_parser.is_valid - писать отдельный тест для функции, возвращающей бинарное значение, не кажется осмысленным.
def read_file_gen(dir):
    for file_name in os.listdir(dir):
        if not file_name.endswith(".log"):
            continue
        path = os.path.join(dir, file_name[:-4])

        t = _time(file_name + " - start")
        result = log_parser.read_file(path + ".log")
        _time(file_name + " - parsed", t)

        with open(path + ".groups", "r") as f:
            expected_result = f.readline()
            assert json.dumps(result, sort_keys=True) == expected_result, \
                "DIFFERNT GROUPS:\n" + json.dumps(result, sort_keys=True) + "\n" + expected_result
            # используется сравнение результатов как строк (а не как словарей),
            # поскольку если а - dict с ключами-int'ами, то json.loads( json.dumps(a) ) - dict с ключами-строками;
            # можно было бы использовать pickle; с другой стороны, приятно обойтись одним парсером,
            # а json.dumps хочется использовать для красивой печати группировки в случае ошибки.

# log_parser.read_file не падает при чтении образцов логов
def read_file_real(dir):
    t = _time("read_file - real - start")
    for file_name in os.listdir(dir):
        log_parser.read_file( os.path.join(dir, file_name) )
    t = _time("read_file - real - parsed", t)

# log_parser.read_dir не падает при чтении образцов логов
def read_dir_real(dir):
    t = _time("read_dir - real - start")
    dir_parser.read_dir( dir, cpu_count() )
    t = _time("read_dir - real - parsed", t)


def _merge_groups_internal(groups, expected_result):
    for i in range(1, len(groups)):
        dir_parser.merge_groups( groups[0], groups[i] )
    assert groups[0] == expected_result, \
        "DIFFERNT GROUPS:\n" + json.dumps(groups[0], sort_keys=True, indent=4) + "\n" + json.dumps(expected_result, sort_keys=True, indent=4)

# проверка корректности dir_parser.merge_groups на маленьких рукпосиных примерах
def merge_groups_small():
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

# проверка корректности dir_parser.merge_groups на большом автогенеренном примере
def merge_groups_big():
    n = 1000

    groups = []
    for i in range(1, n):
        groups.append( {"valid": {i : {"a" : i}}} )
        groups[-1]["valid"][i + 1] = {"a": i}

    expected_result = {"valid": {1 : {"a" : 1}, n : {"a" : n - 1}}}
    for i in range(2, n):
        expected_result["valid"][i] = {"a" : 2 * i - 1}
        
    _merge_groups_internal(groups, expected_result)


# в "настоящем" коде этих строк бы не было, но был бы специальный запускатель тестов
if __name__ == "__main__":
    read_file_gen("./test_files_generated")
    read_file_real("./test_files")
    read_dir_real("./test_files/")
    merge_groups_small()
    merge_groups_big()
