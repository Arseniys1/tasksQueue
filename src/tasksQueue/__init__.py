

__name__ = "TasksQueue"
__version__ = version = "1.0.0"
__fullname__ = "%s %s" % (__name__, __version__)


from .tasks_queue import Task, Entity, TaskData, TasksQueue
from .tasks_worker import worker
from .thread_sleep import thread_sleep
from .decorators import provide, provide_entity
from .provide_constants import ENTITY, TASK_ID, TASK, TASKS_QUEUE




