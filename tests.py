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
        print(message, " - ", int( (time.process_time() - process_time) ))
        return time.process_time()

# проверка корректности функции read_file на автоматически сгенерированных логах
def read_file_1():
    for name in ["small", "medium", "big"]:       # ToDo - all the log files in the folder
        path = "./test_files_generated/" + name
        f = open(path + ".groups", "r")
        expected_result = json.loads( f.readline() )
        f.close()
        pt = _time(name + " - start")
        result = log_parser.read_file(path + ".log")
        assert( result == expected_result, result, expected_result )
        _time(name + " - ok", pt)

read_file_1()     # в "настоящем" коде этой строки бы не было, но был бы специальный запускатель тестов
