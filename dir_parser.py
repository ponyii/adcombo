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

# ToDO - а если в директории много файлов? если они появляются?
# можно еще использовать `with os.scandir(path) as it` или `pathlib.Path.cwd().iterdir()`
def read_dir(path, proc_n):
    pool = Pool(processes=proc_n)
    log_files = []
    for file_name in os.listdir(path):
        log_files.append( path + file_name )     # ToDo - use pathlib
    results = pool.map(log_parser.read_file, log_files)
    for i in range(1, len(results)):
        merge_groups(results[0], results[i])
    return results[0]

if __name__ == "__main__":
    import json
    print(json.dumps( read_dir("./test_files/", 2), sort_keys=True, indent=4 ))
