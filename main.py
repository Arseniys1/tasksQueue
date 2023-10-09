

from decorators import provide_entity, provide
from tasks_queue import TaskData, generate_task_id, Task, TasksQueue


@provide_entity
@provide("task_id")
@provide("task")
def thread(entity, task_id, task, test):
    future = task.future
    while True:
        pass


def main():
    queue = TasksQueue(max_workers=50)
    task_id = queue.add_task(thread, True)
    task = queue.get_task_by_id(task_id)
    print(task, task_id)


if __name__ == "__main__":
    main()


