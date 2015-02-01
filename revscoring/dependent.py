import logging
from functools import wraps

logger = logging.getLogger("revscoring.dependent")

class DependencyLoop(RuntimeError):
    pass

class Dependent:
    
    def __init__(self, name, process, dependencies=None):
        self.name = name
        self.process = process
        self.dependencies = dependencies if dependencies is not None else []
    
    def __call__(self, *args, **kwargs):
        logger.debug("Executing {0}.".format(self))
        return self.process(*args, **kwargs)
    
    def __str__(self): return self.__repr__()
    
    def __repr__(self):
        return "<" + self.name + ">"

def solve(dependent, cache=None, history=None):
    """
    Calculates a dependent's value by solving dependencies.
    
    :Parameters:
        dependent : `Dependent` | `function`
            A dependent function to solve for.
        cache : `dict`
            A memoized cache of previously solved dependencies.
        history : `set`
            Used to detect loops in dependencies.
    
    :Returns:
        The result of executing the dependent with all dependencies resolved
    """
    cache = cache or {}
    history = history or set()
    
    # Check if we've already got this dependency
    if dependent in cache:
        return cache[dependent]
    else:
        
        # Check if the dependency is callable.  If not, we're SOL
        if not callable(dependent):
            raise RuntimeError("Can't solve dependency " + repr(dependent) + \
                               ".  " + type(dependent).__name__ + \
                               " is not callable.")
                
        # Check if we're in a loop.
        elif dependent in history:
            raise DependencyLoop("Dependency loop detected at " + \
                                 repr(dependent))
        
        # All is good.  Time to generate a value
        else:
            
            # Add to history so we can detect any loops on the way down.
            history.add(dependent)
            
            # Check if we're a dependent with explicit dependencies
            if hasattr(dependent, "dependencies"):
                dependencies = dependent.dependencies
            else:
                # No dependencies?  OK.  Let's try that.
                dependencies = []
            
            # Generate args from dependencies
            args = [solve(dependency, cache, history=history)
                    for dependency in dependencies]
            
            
            # Generate value
            value = dependent(*args)
            
            # Add value to cache
            cache[dependent] = value
            return cache[dependent]
