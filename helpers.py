import time

# возвращает текущее time.perf_counter() и выводит в консоль message;
# если второй аргумент положительный, также выводит в консоль разницу во времени;
def _time(message, t = -1):
    if t == -1:
        print(message)
        return time.perf_counter()
    else:
        print(message, " - ", time.perf_counter() - t)
        return time.perf_counter()
