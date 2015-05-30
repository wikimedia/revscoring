import logging
from functools import wraps

logger = logging.getLogger("revscoring.dependent")

def not_implemented(*args, **kwargs):
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
