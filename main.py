from decorators import provide_entity, provide
from tasks_queue import TaskData, generate_task_id, Task, TasksQueue


@provide_entity
@provide("task_id")
def thread(task_id, entity, test):
    print(task_id, entity, test)
    while True:
        pass


def main():
    queue = TasksQueue(max_workers=50)
    queue.add_task(thread, True)


if __name__ == "__main__":
    main()


