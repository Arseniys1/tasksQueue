import uuid
from concurrent.futures import ThreadPoolExecutor

from helpers import get_original_function_from_provide_wrappers
from tasks_entry import entry


def generate_task_id():
    return str(uuid.uuid4())


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
    def __init__(self, task_id, fn, *args, **kwargs) -> None:
        super().__init__()
        self.task_id = task_id
        self.future = None
        self.fn = fn
        self.task_data = TaskData(self.task_id, *args, **kwargs)

    def set_future(self, future):
        self.future = future


class Entity:
    def __init__(self, tasks_queue, task) -> None:
        super().__init__()
        self.tasks_queue = tasks_queue
        self.task = task
        self.task_data = task.task_data


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

    def provide_to_function(self, fn, task, *args):
        function_element = entry.get_function_element(fn)
        args = list(args)
        provide_elements = []
        names_reverse = function_element.names.copy()
        names_reverse.reverse()
        for name in names_reverse:
            if name == "entity":
                entity = Entity(self, task)
                provide_elements.append(entity)
            elif name == "task_id":
                provide_elements.append(task.task_id)
            elif name == "task":
                provide_elements.append(task)
        return tuple(provide_elements + args)

    def add_task(self, fn, *args, **kwargs) -> str:
        fn = get_original_function_from_provide_wrappers(fn)
        task_id = self.generate_unique_task_id()
        task = Task(task_id, fn, *args, **kwargs)
        self.task_ids.append(task_id)
        self.tasks.append(task)
        provided_args = self.provide_to_function(fn, task, *args)
        future = self.executor.submit(fn, *provided_args, **kwargs)
        task.set_future(future)
        return task_id

    def get_task_by_id(self, task_id):
        for task in self.tasks:
            if task.task_id == task_id:
                return task



