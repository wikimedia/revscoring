import pickle

from revscores.dependent import Dependent, depends


def foo_func():
    return 5

foo = Dependent("foo", foo_func)

print(pickle.dumps(foo))

@depends()
def foo2():
    return 5
    
print(pickle.dumps(foo2))
