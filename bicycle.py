'''
Рукописный парсер запросов; немного быстрее, чем json.loads, способен давать такой же результат.
Его главное достоинство - возможность не конвертировать ids в числа, что ускоряет парсинг и log_parser.is_valid; это ускореят код раза в полтора.

Я написал его в (тщетной) надежде опередить json.loads;
он быстрее лишь немного, но требует куда больших гарантий от файла логов (порядок ключей, пробелы, ...).
Правильным способом оптимизации кажется использование pickle и для записи, и для чтения логов;
при сильном желании можно также модифицировать записыватель логов или же код pickle, чтобы избавить от конвертации ids в числа.
'''

def loads(line):
    result = {}

    left = line.find("\"timestamp\":") + len("\"timestamp\":")
    right = line.find(",", left)
    result["timestamp"] = int( line[left : right] )

    left = line.find("\"event_type\":\"", left) + len("\"event_type\":\"")
    right = line.find("\",", left)
    result["event_type"] = line[left : right]

    left = line.find("\"ids\":[", left) + len("\"ids\":[")
    right = line.find("],", left)
    result["ids"] = line[left : right].split(",")   # нет необходимости переводить их в int

    left = line.find("\"query_string\":\"", left) + len("\"query_string\":\"")
    right = line.find("\"}", left)
    result["query_string"] = line[left : right]

    return result
