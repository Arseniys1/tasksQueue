from concurrent.futures import ProcessPoolExecutor
from time import sleep

from decorators import provide_entity, provide
from provide_constants import TASK_ID, TASK, TASKS_QUEUE
from tasks_queue import TaskData, generate_task_id, Task, TasksQueue


@provide_entity
def thread(entity, test):
    print("exit")


def main():
    queue = TasksQueue(max_workers=50)
    queue.run_worker()
    task_id = queue.add_task(thread, True)
    task = queue.get_task_by_id(task_id)
    print(task, task_id)
    sleep(1)
    queue.set_work(False)


if __name__ == "__main__":
    main()


