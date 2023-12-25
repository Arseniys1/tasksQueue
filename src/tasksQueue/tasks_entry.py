import inspect

from .helpers import get_original_function_from_provide_wrappers


class FunctionElement:
    def __init__(self, fn, names) -> None:
        super().__init__()
        self.fn = fn
        self.names = names
        self.fn_arguments = inspect.getfullargspec(fn)


class TasksEntry:
    def __init__(self) -> None:
        super().__init__()
        self.function_elements = []

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(TasksEntry, cls).__new__(cls)
        return cls.instance

    def get_function_element(self, fn):
        for function_element in self.function_elements:
            if function_element.fn == fn:
                return function_element

    def add_provide_names(self, fn, names):
        fn = get_original_function_from_provide_wrappers(fn)
        if type(names) == str:
            names = [names]
        function_element = self.get_function_element(fn)
        if not function_element:
            function_element = FunctionElement(fn, names)
            self.function_elements.append(function_element)
        else:
            [function_element.names.append(name) for name in names if name not in function_element.names]


entry = TasksEntry()


