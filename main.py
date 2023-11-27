from time import sleep

from src.tasksQueue.decorators import provide_entity
from src.tasksQueue.tasks_queue import TasksQueue


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


