import inspect


def find_f_local_in_stack(local_name):
    stack = inspect.stack()

    for frame_info in stack:
        code_ctx = frame_info.code_context
        if len(code_ctx) == 0:
            continue

        f_locals = frame_info.frame.f_locals
        if local_name not in f_locals:
            continue

        return f_locals[local_name]
