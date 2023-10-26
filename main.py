from time import sleep

from decorators import provide_entity, provide
from provide_constants import TASK_ID, TASK, TASKS_QUEUE
from tasks_queue import TaskData, generate_task_id, Task, TasksQueue


@provide_entity
@provide(TASK_ID)
@provide(TASK)
@provide(TASKS_QUEUE)
def thread(entity, task_id, task, tasks_queue, test, success_url, callback_success_url, callback_error_url):
    future = task.future
    while task.work:
        pass
    print("exit")


def main():
    queue = TasksQueue(max_workers=50)
    queue.run_worker()
    task_id = queue.add_task(thread, True, success_url="https://google.com/", callback_success_url="https://google.com/", callback_error_url="https://google.com/")
    task = queue.get_task_by_id(task_id)
    print(task, task_id)
    sleep(1)
    queue.set_work(False)


if __name__ == "__main__":
    main()


