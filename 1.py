from concurrent.futures import ProcessPoolExecutor
from io import StringIO

import jsonpickle

from tasks_queue import TasksQueue


def test(buff):
    print(id(buff))
    while True:
        print(1)


def main():
    queue = TasksQueue()
    executor = ProcessPoolExecutor()
    buff = StringIO()
    print(id(buff))
    future = executor.submit(test, (buff,))
    executor.shutdown(wait=False)


if __name__ == "__main__":
    buff = StringIO()
    print(jsonpickle.encode(buff))
    main()


