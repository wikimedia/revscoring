"""

.. autoclass:: revscoring.Dependent
    :members:

.. autoclass:: revscoring.DependentSet
    :members:
"""
import logging
import pickle

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

    def _format_name(self, name, args, func_name=None):
        if name is None:
            name = "{0}({1})" \
                   .format(func_name or self.__class__.__name__,
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

    @classmethod
    def load(cls, f):
        """
        Reads serialized model information from a file.
        """
        if hasattr(f, 'buffer'):
            return pickle.load(f.buffer)
        else:
            return pickle.load(f)

    def dump(self, f):
        """
        Writes serialized model information to a file.
        """

        if hasattr(f, 'buffer'):
            return pickle.dump(self, f.buffer)
        else:
            return pickle.dump(self, f)


class DependentSet:
    """
    Represents a set of :class:`~revscoring.Dependent`.  This class behaves
    like a :class:`set`.

    :Parameters:
        name : `str`
            A base name for the items in the set
    """

    def __init__(self, name, dependents=None, dependent_sets=None):
        self.dependents = dependents or {}
        self.dependent_sets = dependent_sets or {}
        self.name = name

    def __setattr__(self, attr, value):
        super().__setattr__(attr, value)

        if isinstance(value, Dependent):
            logger.log(logging.NOTSET,
                       "Registering {0} to {1}".format(value, self.name))
            if value in self.dependents:
                logger.warn("{0} has already been added to {1}.  Could be "
                            .format(value, self) + "overwritten?")
            self.dependents[attr] = value
        elif isinstance(value, DependentSet):
            self.dependent_sets[attr] = value
        else:
            pass  # Just set it like a regular attribute

    # String methods
    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return "{" + self.name + "}"

    def __hash__(self):
        return hash('dependent_set.' + self.name)

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __ne__(self, other):
        return not self == other

    def all_dependencies(self):
        return set(self.dependents.values()).union(*self.dependent_sets.values())

    # Set methods
    def __len__(self):
        return len(self.all_dependencies())

    def __contains__(self, item):
        return item in self.all_dependencies()

    def __iter__(self):
        return iter(self.all_dependencies())

    def __sub__(self, other):
        return self.all_dependencies() - other

    def __and__(self, other):
        return self.all_dependencies() & other

    def __or__(self, other):
        return self.all_dependencies() | other
