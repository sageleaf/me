from functools import wraps

def validate_user(f):
    @wraps(f)
    def func_wrapper(*args, **kwargs): 
        pass
        return f(*args, **kwargs)
    return func_wrapper
