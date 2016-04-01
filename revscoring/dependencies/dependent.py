"""

.. autoclass:: revscoring.Dependent
    :members:

.. autoclass:: revscoring.DependentSet
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
            A collection of :class:`revscoring.Dependent` whose values are
            required by `process`
    """
    def __init__(self, name, process=None, depends_on=None,
                 dependencies=None):
        if not isinstance(name, str):
            raise TypeError("Name {0} is not a str.".format(name))
        self.name = name
        self.process = process or not_implemented
        self.dependencies = dependencies or depends_on or []
        self.calls = 0

    def _format_name(self, name, args):
        if name is None:
            name = "{0}({1})" \
                   .format(self.__class__.__name__,
                           ", ".join(repr(arg) for arg in args))

        return name

    def __call__(self, *args, **kwargs):
        logger.debug("Executing {0} ({1} calls so far)."
                     .format(self, self.calls))
        self.calls += 1
        return self.process(*args, **kwargs)

    def __hash__(self):
        return hash('dependent.' + self.name)

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __ne__(self, other):
        return not self == other

    def __str__(self):
        return "dependent." + self.name

    def __repr__(self):
        return "<" + self.__str__() + ">"


class DependentSet:
    """
    Represents a set of :class:`~revscoring.Dependent`.  This class behaves
    like a :class:`set`.

    :Parameters:
        name : `str`
            A base name for the items in the set
    """
    def __init__(self, name, _dependents=None, _dependent_sets=None):
        self._dependents = _dependents or set()
        self._dependent_sets = _dependent_sets or set()
        self._name = name

    def __setattr__(self, attr, value):
        super().__setattr__(attr, value)

        if isinstance(value, Dependent):
            logger.log(logging.NOTSET,
                       "Registering {0} to {1}".format(value, self._name))
            if value in self._dependents:
                logger.warn("{0} has already been added to {1}.  Could be "
                            .format(value, self) + "overwritten?")
            self._dependents.add(value)
        elif isinstance(value, DependentSet):
            self._dependent_sets.add(value)

    # String methods
    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return "{" + self._name + "}"

    def __hash__(self):
        return hash('dependent_set.' + self._name)

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __ne__(self, other):
        return not self == other

    # Set methods
    def __len__(self):
        return len(self._dependents.union(*self._dependent_sets))

    def __contains__(self, item):
        return item in self._dependents.union(*self._dependent_sets)

    def __iter__(self):
        return iter(self._dependents.union(*self._dependent_sets))

    def __sub__(self, other):
        return self._dependents.union(*self._dependent_sets) - other

    def __and__(self, other):
        return self._dependents.union(*self._dependent_sets) & other

    def __or__(self, other):
        return self._dependents.union(*self._dependent_sets) | other
