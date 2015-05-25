import logging
from functools import wraps

logger = logging.getLogger("revscoring.dependent")


class DependencyLoop(RuntimeError):
    pass


class DependencyError(RuntimeError):
    def __init__(self, message, exception):
        super().__init__(message)
        self.exception = exception

def not_implemented():
    raise NotImplementedError("Not implemented.")

class Dependent:

    def __init__(self, name, process=not_implemented, depends_on=None,
                             dependencies=None):
        self.name = name
        self.process = process
        self.dependencies = dependencies or depends_on or []
        self.calls = 0

    def __call__(self, *args, **kwargs):
        logger.debug("Executing {0}.".format(self))
        self.calls += 1
        return self.process(*args, **kwargs)

    def __hash__(self):
        return hash(('dependent', self.name))

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __ne__(self, other):
        return not self == other

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return "<" + self.name + ">"


def solve_many(dependents, context=None, cache=None):

    for dependent in dependents:
        value, cache, history = _solve(dependent, context=context, cache=cache)
        yield value


def solve(dependent, context=None, cache=None):

    value, cache, history = _solve(dependent, context=context, cache=cache)
    return value

def expand(dependent, cache=None):
    cache = cache or set()

    cache.add(dependent)

    if hasattr(dependent, "dependencies"):

        for dependency in dependent.dependencies:
            if dependency not in cache:
                cache = expand(dependency, cache)

    return cache

def expand_many(dependents, cache=None):
    cache = cache or set()

    for dependent in dependents:
        cache = expand(dependent, cache)

    return cache


def _solve(dependent, context=None, cache=None, history=None):
    """
    Calculates a dependent's value by solving dependencies.

    :Parameters:
        dependent : `Dependent` | `function`
            A dependent function to solve for.
        inject : `dict` | `set`
            A mapping of injected dependency processers.  Can be specified as a
            set of new `Dependent` or a map of `Dependent`:func() pairs.
        cache : `dict`
            A memoized cache of previously solved dependencies.
        history : `set`
            Used to detect loops in dependencies.

    :Returns:
        The result of executing the dependent with all dependencies resolved
    """
    if context is None:
        context = {}
    elif not isinstance(context, dict):
        context = {d:d for d in context}
    # else leave context alone

    cache = cache or {}
    history = history or set()

    # Check if we've already got a value for this dependency
    if dependent in cache:
        return cache[dependent], cache, history

    # Check if a corresponding dependent was injected into the context
    else:

        # If a dependent is in context here, replace it.
        if dependent in context:
            dependent = context[dependent]

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
                value, cache, history = _solve(dependency, context=context,
                                               cache=cache, history=history)

                args.append(value)

            # Generate value
            try:
                value = dependent(*args)
            except Exception as e:
                raise DependencyError("Failed to process {0}: {1}"
                                      .format(dependent, e), str(e))

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
