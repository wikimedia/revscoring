import logging

import decorator

logger = logging.getLogger("revscores.feature_extraction.dependencies")

class depends_on:
    
    def __init__(self, *dependencies):
        self.dependencies = dependencies
    
    def __call__(self, f):
        
        def wrapped_f(*args, **kwargs):
            logger.debug("Executing {0}.".format(f))
            return f(*args, **kwargs)
            
        
        wrapped_f.dependencies = self.dependencies
        
        return wrapped_f
    

def solve(dependent, cache):
    if dependent in cache:
        return cache[dependent]
    else:
        
        if not callable(dependent):
            raise Exception("Can't solve dependency " + repr(dependent) + \
                            ".  " + type(dependent).__name__ + \
                            " is not callable.")
        else:
            
            if hasattr(dependent, "dependencies"):
                dependencies = dependent.dependencies
            else:
                dependencies = []
            
            args = [solve(dependency, cache)
                    for dependency in dependencies]
        
            value = dependent(*args)
            cache[dependent] = value
            return cache[dependent]
