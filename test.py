from src.tasksQueue import TasksQueue, worker

queue = TasksQueue()


def test(n, test1=None, result_callback=None, exception_callback=None):
    raise Exception("123")
    return n, test1


def res(task, future_result):
    print(task, future_result)


def exc(task, exception):
    print(task, exception)


queue.add_task(test, 1, test1=123, result_callback=res, exception_callback=exc)

queue.run_worker()

