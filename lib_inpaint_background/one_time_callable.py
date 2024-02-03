def one_time_callable(func):
    def wrapper(*args, **kwargs):
        if not wrapper.called:
            wrapper.called = True
            return func(*args, **kwargs)

    wrapper.called = False
    return wrapper
