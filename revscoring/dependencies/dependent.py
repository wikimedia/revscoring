"""
.. autoclass:: revscoring.dependencies.dependent.Dependent
    :members:
"""
import logging

logger = logging.getLogger(__name__)


def not_implemented(*args, **kwargs):
    raise NotImplementedError("Not implemented.")


class Dependent:
    """
    Constructs a dependency-handling processor function.

    :Parameters:
        name : str
            A name to identify this dependency
        process : func
            A function to run when solving this dependency
        depends_on : `iterable`
            A collection of
    """
    def __init__(self, name, process=None, depends_on=None,
                 dependencies=None):
        self.name = name
        self.process = process or not_implemented
        self.dependencies = dependencies or depends_on or []
        self.calls = 0

    def __call__(self, *args, **kwargs):
        logger.debug("Executing {0} ({1} calls so far)."
                     .format(self, self.calls))
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
