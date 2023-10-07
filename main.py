from tasks_queue import TaskData, generate_task_id, Task, TasksQueue


def thread(test):
    while True:
        pass


def main():
    queue = TasksQueue(max_workers=50)
    queue.add_task(thread, (True,))


if __name__ == '__main__':
    main()


