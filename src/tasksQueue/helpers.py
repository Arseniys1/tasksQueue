

def get_original_function_from_provide_wrappers(fn):
    while True:
        if fn.__qualname__ == "get_provide_wrapper.<locals>.provide_wrapper":
            fn = fn()
            continue
        else:
            return fn


