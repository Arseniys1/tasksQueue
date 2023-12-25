import inspect
import uuid
from concurrent.futures import ThreadPoolExecutor

from .helpers import get_original_function_from_provide_wrappers
from .provide_constants import ENTITY, TASK_ID, TASK, TASKS_QUEUE
from .tasks_entry import entry
from .tasks_worker import worker


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

    def get_callback_success_url(self):
        if "callback_success_url" in self.kwargs:
            return self.kwargs["callback_success_url"]

    def get_callback_error_url(self):
        if "callback_error_url" in self.kwargs:
            return self.kwargs["callback_error_url"]

    def get_result_callback(self):
        if "result_callback" in self.kwargs:
            return self.kwargs["result_callback"]

    def get_exception_callback(self):
        if "exception_callback" in self.kwargs:
            return self.kwargs["exception_callback"]

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
        self.fn_name = str(fn)
        self.task_data = TaskData(self.task_id, *args, **kwargs)
        self.work = True
        self.future_result = None
        self.exception = None
        self.serialize_hide = ["future", "fn", "work", "serialize_hide"]

    def set_future(self, future):
        self.future = future

    def set_future_result(self, future_result):
        self.future_result = future_result

    def set_exception(self, exception: Exception):
        self.exception = exception

    def __getstate__(self):
        result = self.__dict__
        for hide_item in self.serialize_hide:
            result.pop(hide_item)
        return result


class Entity:
    def __init__(self, tasks_queue, task) -> None:
        super().__init__()
        self.tasks_queue = tasks_queue
        self.task = task
        self.task_data = task.task_data


class TasksQueue:
    def __init__(self, prefix=None, *args, **kwargs) -> None:
        super().__init__()
        self.tasks = []
        self.task_ids = []
        self.executor = ThreadPoolExecutor(*args, **kwargs)
        self.work = True
        self.worker_task = None
        self.prefix = prefix

    def generate_unique_task_id(self) -> str:
        while True:
            task_id = generate_task_id()
            if self.prefix:
                task_id = f"{self.prefix}.{task_id}"
            if task_id in self.task_ids:
                continue
            else:
                return task_id

    @staticmethod
    def remove_unused_kwargs(fn, **kwargs):
        kwargs_keys = list(kwargs.keys())
        for kwarg_name in kwargs_keys:
            if kwarg_name not in inspect.getfullargspec(fn).args:
                kwargs.pop(kwarg_name)
        return kwargs

    def provide_to_function(self, fn, task, *args, **kwargs):
        function_element = entry.get_function_element(fn)
        if not function_element:
            return args, self.remove_unused_kwargs(fn, **kwargs)
        args = list(args)
        provide_elements = []
        names_reverse = function_element.names.copy()
        names_reverse.reverse()
        for name in names_reverse:
            if name == ENTITY:
                entity = Entity(self, task)
                provide_elements.append(entity)
            elif name == TASK_ID:
                provide_elements.append(task.task_id)
            elif name == TASK:
                provide_elements.append(task)
            elif name == TASKS_QUEUE:
                provide_elements.append(self)
        kwargs_keys = list(kwargs.keys())
        for kwarg_name in kwargs_keys:
            if kwarg_name not in function_element.fn_arguments.args:
                kwargs.pop(kwarg_name)
        return tuple(provide_elements + args), self.remove_unused_kwargs(fn, **kwargs)

    def add_task(self, fn, *args, **kwargs) -> str:
        fn = get_original_function_from_provide_wrappers(fn)
        task_id = self.generate_unique_task_id()
        task = Task(task_id, fn, *args, **kwargs)
        self.task_ids.append(task_id)
        self.tasks.append(task)
        provided_args, provided_kwargs = self.provide_to_function(fn, task, *args, **kwargs)
        future = self.executor.submit(fn, *provided_args, **provided_kwargs)
        task.set_future(future)
        return task_id

    def get_task_by_id(self, task_id):
        for task in self.tasks:
            if task.task_id == task_id:
                return task

    def set_work(self, work):
        if not work:
            for task in self.tasks:
                task.work = False
        self.work = work

    def get_futures_list(self):
        futures = []
        for task in self.tasks:
            futures.append(task.future)
        return futures

    def get_task_by_future(self, future):
        for task in self.tasks:
            if task.future == future:
                return task

    def run_worker(self):
        if self.worker_task:
            return self.worker_task
        task_id = self.add_task(worker)
        task = self.get_task_by_id(task_id)
        self.worker_task = task
        return task






