import logging
from functools import wraps

logger = logging.getLogger("revscoring.dependent")


class DependencyLoop(RuntimeError):
    pass


class DependencyError(RuntimeError):
    def __init__(self, message, exception):
        super().__init__(message)
        self.exception = exception


class Dependent:

    def __init__(self, name, process, dependencies=None):
        self.name = name
        self.process = process
        self.dependencies = dependencies if dependencies is not None else []
        self.calls = 0

    def __call__(self, *args, **kwargs):
        logger.debug("Executing {0}.".format(self))
        self.calls += 1
        return self.process(*args, **kwargs)

    def __hash__(self):
        return hash((self.__class__.__name__, self.name))

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return "<" + self.name + ">"


def solve_many(dependents, cache=None):
    cache = cache or {}

    for dependent in dependents:
        value, cache, history = _solve(dependent, cache)
        yield value


def solve(dependent, cache=None):
    cache = cache or {}

    value, cache, history = _solve(dependent, cache)
    return value


def _solve(dependent, cache, history=None):
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
    history = history or set()

    # Check if we've already got this dependency
    if dependent in cache:
        return cache[dependent], cache, history
    else:

        # Check if the dependency is callable.  If not, we're SOL
        if not callable(dependent):
            raise RuntimeError("Can't solve dependency " + repr(dependent) +
                               ".  " + type(dependent).__name__ +
                               " is not callable.")

        # Check if we're in a loop.
        elif dependent in history:
            raise DependencyLoop("Dependency loop detected at " +
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

            # Generate args for process function from dependencies (if any)
            args = []
            for dependency in dependencies:
                value, cache, history = _solve(dependency, cache, history)

                args.append(value)

            # Generate value
            try:
                value = dependent(*args)
            except Exception as e:
                raise DependencyError("Failed to process {0}: {1}"
                                      .format(dependent, e), e)

            # Add value to cache
            cache[dependent] = value
            return cache[dependent], cache, history


def draw(dependent, cache=None, depth=0):
    print("\t" * depth + " - " + str(dependent))

    cache = cache or {}

    # Check if we're a dependent with explicit dependencies
    if hasattr(dependent, "dependencies"):
        for dependency in dependent.dependencies:
            if dependency not in cache:
                draw(dependency, cache=cache, depth=depth+1)
            else:
                draw("CACHED", cache=cache, depth=depth+1)
    else:
        # No dependencies?  OK.  Let's try that.
        dependencies = []
