import time


def get_seconds():
    return round(time.time(), 2)


def thread_sleep(seconds, task):
    end_seconds = get_seconds() + seconds
    while get_seconds() < end_seconds:
        time.sleep(0.1)
        if not task.work:
            break


