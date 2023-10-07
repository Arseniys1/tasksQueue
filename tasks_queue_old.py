import logging
import random
import string
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests

logger = logging.getLogger("django")


class TasksQueue:
    def __init__(self, max_workers=1000):
        self.tasks = []
        self.tasks_data = []
        self.executor = ThreadPoolExecutor(max_workers=max_workers)

    def add_task(self, fn, *args, **kwargs):
        task = self.executor.submit(fn, *args, **kwargs)
        if "task_data" in kwargs:
            self.tasks_data.append([task, kwargs["task_data"]])
        self.tasks.append(task)

    def get_task_by_id(self, task_id):
        for task_data in self.tasks_data:
            if task_data[1]["task_id"] == task_id:
                return task_data

    def generate_task_id(self):
        size = 10
        chars = string.ascii_letters + string.digits
        return ''.join(random.choice(chars) for _ in range(size))

    def worker(self):
        for task in as_completed(self.tasks):
            self.tasks.remove(task)

            task_data = None
            for task_data_item in self.tasks_data:
                if task_data_item[0] == task:
                    task_data = task_data_item[1]
                    self.tasks_data.remove(task_data_item)

            try:
                task_result = task.result()
                try:
                    if task_data and "task_id" in task_data and "back_url" in task_data:
                        requests.post(task_data["back_url"], json={
                            "success": task_result[0],
                            "task_id": task_data["task_id"],
                            "task_result": task_result[1],
                        }, timeout=5)
                except Exception:
                    pass
            except Exception as e:
                try:
                    if task_data and "task_id" in task_data and "back_url" in task_data:
                        requests.post(task_data["back_url"], json={
                            "success": False,
                            "task_id": task_data["task_id"],
                            "task_result": "Произошла ошибка, попробуйте позже",
                        }, timeout=5)
                except Exception:
                    pass
                logger.error(e)


