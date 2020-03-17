from multiprocessing import Pool
import log_parser
import os

# совмещение двух группировок запросов; корректность аргументов не проверяется
def merge_groups(first, second):
    for validness in second:
        for timestamp in second[validness]:
            if timestamp not in first[validness]:
                first[validness][timestamp] = second[validness][timestamp]
            else:
                for event_type, num in second[validness][timestamp].items():
                    first[validness][timestamp][event_type] += num


# число файлов значительно превышает число CPU, так что процессу можно отдать файл целиком;
def read_dir(path, proc_n):
    pool = Pool(processes=proc_n)
    log_files = []
    for file_name in os.listdir(path):           # listdir успешно справляется с 10^6 файлов, на которых виснет ls
        log_files.append( path + file_name )     # ToDo - use pathlib
    results = pool.map(log_parser.read_file, log_files)    # ToDo - мержить нужно на лету
    for i in range(1, len(results)):
        merge_groups(results[0], results[i])
    return results[0]
