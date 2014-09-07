

class depends_on:
    
    def __init__(self, *dependencies):
        self.dependencies = dependencies
    
    def __call__(self, f):
        f.dependencies = self.dependencies
        
        return f
    

def solve(dependent, cache):
    if dependent in cache:
        return cache[dependent]
    else:
        args = [solve(dependency, cache)
                for dependency in dependent.dependencies]
        
        value = dependent(*args)
        cache[dependent] = value
