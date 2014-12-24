import functools
import pickle


class Dependee:
    
    def __init__(self, func, depends_on=None):
        self.func = func
        self.depends_on = depends_on or []
        functools.update_wrapper(self, func)
    
    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)
    
    def __getstate__(self):
        return (self.func, self.depends_on)
    
    def __setstate__(self, state):
        self.func, self.depends_on = state
    
class depends:
    
    def __init__(self, on=None):
        self.depends_on = on or []
    
    def __call__(self, func):
        return Dependee(func, self.depends_on)
        

@depends(on=["foo", "bar"])
def sum(x, y):
    """
    I am the docstring
    """
    return x+y

print(sum)
print(sum.depends_on)
print(sum(1,2))
print(pickle.dumps(sum))
