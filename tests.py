import generator
import log_parser
import json
import time

# возвращает текущее time.process_time() и выводит в консоль @message;
# если второй аргумент положительный, также выводит в консоль разницу во времени;
def _time(message, process_time = -1):
    if process_time == -1:
        print(message)
        return time.process_time()
    else:
        print(message, " - ", time.process_time() - process_time)
        return time.process_time()

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

read_file_1()     # в "настоящем" коде этой строки бы не было, но был бы специальный запускатель тестов
