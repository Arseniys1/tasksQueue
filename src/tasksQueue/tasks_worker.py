import logging
from concurrent.futures import as_completed

from .decorators import provide
from .provide_constants import TASKS_QUEUE
from .tasks_requests import success_request, error_request

logger = logging.getLogger(__name__)


@provide(TASKS_QUEUE)
def worker(tasks_queue):
    while tasks_queue.work:
        for future in as_completed(tasks_queue.get_futures_list()):
            task = tasks_queue.get_task_by_future(future)
            try:
                future_result = future.result()
                task.set_future_result(future_result)
                result_callback = task.task_data.get_result_callback()
                if result_callback:
                    try:
                        result_callback(task, future_result)
                    except Exception as e:
                        logger.error(e)
                success_url = task.task_data.get_success_url()
                if success_url:
                    success_request(success_url, task)
            except Exception as future_exception:
                logger.error(future_exception)
                task.set_exception(future_exception)
                exception_callback = task.task_data.get_exception_callback()
                if exception_callback:
                    try:
                        exception_callback(task, future_exception)
                    except Exception as ee:
                        logger.error(ee)
                try:
                    error_url = task.task_data.get_error_url()
                    if error_url:
                        error_request(error_url, task)
                except Exception as ee:
                    logger.error(ee)
            tasks_queue.task_ids.remove(task.task_id)
            tasks_queue.tasks.remove(task)




