from multiprocessing import Pool
import log_parser
import os

# Совмещение двух группировок запросов (@first изменяется, @second - нет);
# ОСТОРОЖНО, корректность аргументов не проверяется.
def merge_groups(first, second):
    for validness in second:
        for timestamp in second[validness]:
            if timestamp not in first[validness]:
                first[validness][timestamp] = second[validness][timestamp]
            else:
                for event_type, num in second[validness][timestamp].items():
                    first[validness][timestamp][event_type] += num


# Чтение (мультипроцессорное) папки с логами; возвращает группировку запросов;
# ОСТОРОЖНО, корректность файлов логов, наличие инородных файлов и т.п. не проверяется.
# число файлов значительно превышает число CPU, так что процесс получает файл целиком.
def read_dir(path, proc_n):
    pool = Pool(processes=proc_n)
    log_files = []
    for file_name in os.listdir(path):           # listdir успешно справляется с 10^6 файлов, на которых виснет ls
        log_files.append( os.path.join(path, file_name) )

    result = {"valid": {}, "non_valid": {}}

    files_num = 1000                       # обрабатываются chunk'и по files_num файлов, после чего результаты на всех обработанных логах merge'атся;
    chunks = len(log_files) // files_num   # единственная причина такого разделения - хочется использовать pool.map, но не писать велосипед;
    if len(log_files) % files_num != 0:    # и также хочется избежать хранения массива из миллиона группировок;
        chunks += 1                        # таким образом files_num - большое число (чем больше - тем лучше), являющееся приемлемой длиной массива группировок.

    for i in range(chunks):
        tmp = log_files[ i : min(i + files_num, len(log_files)) ]
        for group in pool.map(log_parser.read_file, tmp):    # были бы примеры настоящих больших данных - можно было бы подумать про оптимальный chunksize
            merge_groups(result, group)
    return result

'''
Написанная здесь функция предназначена для разового прочтения всех файлов в директории.
Я не нашел никакого хорошего способа обрабатывать добавляющиеся раз в час файлы логов на питоне;
кажется удобным использовать один из следующих вариантов (в порядке уменьшения привлекательности):
- часовую порцию логов класть в отдельную папку и запускать (записывателем логов) в ней парсер;
- move'ать обработанные логи в отдельную папку; после завершения read_dir заново запускаться в той же директории время от времени
    или ждать отмашки от записывателя логов или скрипта на bash'е о появлении новых файлов;
- как в последнем варианте, но ожидать появления логов в питоне, с помощью watchdog.
Последний вариант более всего соответсвтует заданию, но кажется наименее удобным (чем меньше используется редких библиотек - тем лучше); вопрос - к какому из вариантов стоит готовиться?
'''
