from tasks_entry import entry


def get_provide_wrapper(fn):
    def provide_wrapper():
        return fn
    return provide_wrapper


def provide_entity(fn):
    entry.add_provide_names(fn, ["entity"])
    return get_provide_wrapper(fn)


def provide(names):
    def _provide(fn):
        entry.add_provide_names(fn, names)

        return get_provide_wrapper(fn)
    return _provide



