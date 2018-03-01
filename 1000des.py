import threading as th
from random import randint

counter = 0
list = []
lock = th.Lock()
result = 0


def compute(n):
    global counter
    global result
    for i in range(0, n):
        with lock:
            counter = (randint(1, 6))
            list.append(counter)
    result += sum(list) / len(list)


threads = [th.Thread(target=compute, args=(1000,))]
for thread in threads:
    thread.start()
for thread in threads:
    thread.join()
print(result)
