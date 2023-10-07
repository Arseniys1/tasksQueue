import uuid
from concurrent.futures import ThreadPoolExecutor


def generate_task_id():
    return str(uuid.uuid4())


def function_wrapper(fn):
    def function_output(*args, **kwargs):
        fn(*args, **kwargs)
    return function_output


class TaskData:
    def __init__(self, task_id, *args, **kwargs) -> None:
        super().__init__()
        self.task_id = task_id
        self.args = args
        self.kwargs = kwargs

    def get_success_url(self):
        if "success_url" in self.kwargs:
            return self.kwargs["success_url"]

    def get_error_url(self):
        if "error_url" in self.kwargs:
            return self.kwargs["error_url"]

    def __getattr__(self, name):
        if name in self.kwargs:
            return self.kwargs[name]

    def __getitem__(self, key):
        if key in self.args:
            return self.args[key]


class Task:
    def __init__(self, task_id, future, fn, *args, **kwargs) -> None:
        super().__init__()
        self.task_id = task_id
        self.future = future
        self.fn = fn
        self.task_data = TaskData(self.task_id, *args, **kwargs)


class TasksQueue:
    def __init__(self, executor=ThreadPoolExecutor, *args, **kwargs) -> None:
        super().__init__()
        self.tasks = []
        self.task_ids = []
        self.executor = executor(*args, **kwargs)

    def generate_unique_task_id(self) -> str:
        while True:
            task_id = generate_task_id()
            if task_id in self.task_ids:
                continue
            else:
                return task_id

    def add_task(self, fn, *args, **kwargs) -> str:
        task_id = self.generate_unique_task_id()
        self.task_ids.append(task_id)
        future = self.executor.submit(function_wrapper(fn), *args, **kwargs)
        task = Task(task_id, future, fn, *args, **kwargs)
        self.tasks.append(task)
        return task_id








