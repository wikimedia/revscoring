"""
.. autoclass:: revscoring.Feature
    :members:

.. autoclass:: revscoring.features.Modifier
    :members:

.. autoclass:: revscoring.features.Constant
    :members:
"""
import operator
from itertools import repeat

from revscoring.dependencies import Dependent


class Feature(Dependent):
    """
    Represents a predictive feature.

    :Parameters:
        name : str
            The name of the feature
        process : `func`
            A function that will generate a feature value
        returns : `type`
            A type to compare the return of this function to.
        dependencies : `list`(`hashable`)
            An ordered list of dependencies that correspond
            to the `*args` of `process`
    """

    def __init__(self, name, process=None, *, returns=None, depends_on=None):
        super().__init__(name, process, depends_on)
        self.returns = returns

    def __call__(self, *args, **kwargs):
        value = super().__call__(*args, **kwargs)

        if __debug__:
            return self.validate(value)
        else:
            return value

    def _format_name(self, name, args, func_name=None):
        arg_names = []
        for arg in args:
            if isinstance(arg, Constant) or isinstance(arg, ConstantVector):
                arg_names.append(repr(arg.value))
            elif isinstance(arg, Feature):
                arg_names.append(arg.name)
            else:
                arg_names.append(repr(arg))

        if name is None:
            name = "{0}({1})" \
                   .format(func_name or self.__class__.__name__,
                           ", ".join(arg_names))

        return name

    def __hash__(self):
        return hash('feature.' + self.name)

    def __str__(self):
        return "feature." + self.name

    # Binary math
    def __add__(self, summand):
        return add(self, summand)

    def __sub__(self, subband):
        return sub(self, subband)

    def __truediv__(self, divisor):
        return div(self, divisor)

    def __mul__(self, multiplier):
        return mul(self, multiplier)

    # Comparison
    def __lt__(self, other):
        return lt(self, other)

    def __le__(self, other):
        return le(self, other)

    def __eq__(self, other):
        return eq(self, other)

    def __ne__(self, other):
        return ne(self, other)

    def __gt__(self, other):
        return gt(self, other)

    def __ge__(self, other):
        return ge(self, other)

    # Boolean operators
    def and_(self, other):
        return and_(self, other)

    def or_(self, other):
        return or_(self, other)

    def not_(self):
        return not_(self)

    def validate(self, value):
        if isinstance(value, self.returns):
            return value
        else:
            raise ValueError("Expected {0}, but got {1} instead."
                             .format(self.returns, type(value)))

    @classmethod
    def or_constant(self, val):
        if isinstance(val, Feature):
            return val
        elif isinstance(val, list):
            return ConstantVector(val)
        else:
            return Constant(val)


class FeatureVector(Feature):

    def validate(self, vector):
        for i, value in enumerate(vector):
            if not isinstance(value, self.returns):
                raise ValueError(
                    "Expected {0}, but got {1} instead at position {2}."
                    .format(self.returns, type(value), i))

        return vector

    def __hash__(self):
        return hash('feature_vector.' + self.name)

    def __str__(self):
        return "feature_vector." + self.name


class Constant(Feature):
    """
    A special sub-type of `revscoring.Feature` that returns a constant value.

    :Parameters:
        value : `mixed`
            Any type of potential feature value
        name : `str`
            A name to give the feature
    """

    def __init__(self, value, name=None):
        self.value = value
        if name is None:
            name = str(value)
        super().__init__(name, self._process,
                         returns=type(value), depends_on=[])

    def _process(self):
        return self.value


class ConstantVector(FeatureVector):
    """
    A special sub-type of `revscoring.Feature` that returns a constant value.

    :Parameters:
        value : `mixed`
            Any type of potential feature value
        name : `str`
            A name to give the feature
    """

    def __init__(self, values, name=None):
        self.value = values
        if name is None:
            name = str(values)
        super().__init__(name, self._process,
                         returns=type(values[0]), depends_on=[])

    def _process(self):
        return self.value


class Modifier:
    pass


class FunctionApplier(Modifier):
    def __init__(self, *arguments, func, name=None, returns=float):
        if name is None:
            name = self._format_name(
                name, list(arguments), func_name=func.__name__)
        super().__init__(name, self.process, depends_on=arguments,
                         returns=returns)
        self.func = func


class SingletonFunctionApplier(FunctionApplier, Feature):

    def process(self, *arg_vals):
        return self.returns(self.func(*arg_vals))


class VectorFunctionApplier(FunctionApplier, FeatureVector):
    def process(self, *arg_vectors):
        arg_vectors = self.normalize_vectors(arg_vectors)
        return [self.returns(self.func(*arg_vals))
                for arg_vals in zip(*arg_vectors)]

    def normalize_vectors(self, arg_vectors):
        """
        Checks whether all vectors are the same length and repeats singleton
        values so that they can be repeatedly applied against vectors.
        """
        vector_length = max(len(av) for av in arg_vectors
                            if isinstance(av, list))
        normalized_vectors = []

        for dependency, arg_vector in zip(self.dependencies, arg_vectors):
            if isinstance(dependency, FeatureVector):
                if vector_length != len(arg_vector):
                    raise ValueError(
                        ("Length of value for {0} ({1}) does not " +
                         "match the length of other vectors ({2})")
                        .format(dependency, len(arg_vector), vector_length))
                else:
                    normalized_vectors.append(arg_vector)
            else:
                normalized_vectors.append(repeat(arg_vector, vector_length))

        return normalized_vectors


def function_applier(func):
    def wrapper(*arguments, name=None, returns=None):
        arguments = [Feature.or_constant(a) for a in arguments]
        func_tocall, name, returns = func(*arguments, name, returns)
        if returns is None:
            returns = type(func_tocall(*(a.returns() for a in arguments)))
        if any(isinstance(a, FeatureVector) for a in arguments):
            return VectorFunctionApplier(
                *arguments, func=func_tocall, name=name, returns=returns)
        else:
            return SingletonFunctionApplier(
                *arguments, func=func_tocall, name=name, returns=returns)
    return wrapper


def binary_operator(func):
    def wrapper(left, right, name=None, returns=None):
        left = Feature.or_constant(left)
        right = Feature.or_constant(right)
        func_tocall, operator, returns = func(left, right, returns)
        if returns is None:
            returns = type(func_tocall(left.returns(), right.returns()))
        if name is None:
            name = "({0} {1} {2})".format(left.name, operator, right.name)
        if isinstance(left, FeatureVector) or isinstance(right, FeatureVector):
            return VectorFunctionApplier(
                left, right, func=func_tocall, name=name, returns=returns)
        else:
            return SingletonFunctionApplier(
                left, right, func=func_tocall, name=name, returns=returns)
    return wrapper


@binary_operator
def add(left, right, returns):
    return operator.add, "+", returns
add.__doc__ = """
Generates a feature that represents the addition of
two :class:`revscoring.Feature` or constant values.
"""


@binary_operator
def sub(left, right, returns):
    return operator.sub, "-", returns
sub.__doc__ = """
Generates a feature that represents the subtraction of
two :class:`revscoring.Feature` or constant values.
"""


@binary_operator
def mul(left, right, returns):
    return operator.mul, "*", returns
mul.__doc__ = """
Generates a feature that represents the multiplacation of
two :class:`revscoring.Feature` or constant values.
"""


@binary_operator
def div(left, right, returns):
    return operator.truediv, "/", returns if returns is not None else float
div.__doc__ = """
Generates a feature that represents the division of
two :class:`revscoring.Feature` or constant values.
"""


@binary_operator
def lt(left, right, returns):
    return operator.lt, "<", bool
lt.__doc__ = """
Generates a feature that represents the less-than relationship of
two :class:`revscoring.Feature` or constant values.
"""


@binary_operator
def le(left, right, returns):
    return operator.le, "<=", bool
le.__doc__ = """
Generates a feature that represents the less-than-or-equal relationship of
two :class:`revscoring.Feature` or constant values.
"""


@binary_operator
def gt(left, right, returns):
    return operator.gt, ">", bool
gt.__doc__ = """
Generates a feature that represents the greater-than relationship of
two :class:`revscoring.Feature` or constant values.
"""


@binary_operator
def ge(left, right, returns):
    return operator.ge, ">=", bool
ge.__doc__ = """
Generates a feature that represents the greater-than-or-equal relationship
of two :class:`revscoring.Feature` or constant values.
"""


@binary_operator
def eq(left, right, returns):
    return operator.eq, "==", bool
eq.__doc__ = """
Generates a feature that represents the equality of two
:class:`revscoring.Feature` or constant values.
"""


@binary_operator
def ne(left, right, returns):
    return operator.ne, "!=", bool
ne.__doc__ = """
Generates a feature that represents the inequality of two
:class:`revscoring.Feature` or constant values.
"""


@binary_operator
def or_(left, right, returns):
    return operator.or_, "or", bool
or_.__doc__ = """
Generates a feature that represents the disjunction of two
:class:`revscoring.Feature` or constant values.
"""


@binary_operator
def and_(left, right, returns):
    return operator.and_, "and", bool
and_.__doc__ = """
Generates a feature that represents the conjunction of two
:class:`revscoring.Feature` or constant values.
"""


@function_applier
def not_(dependency, name, returns):
    if name is None:
        name = "(not {0})".format(dependency.name)
    return operator.not_, name, bool
not_.__doc__ = """
Generates a feature that represents the negation of one
:class:`revscoring.Feature` or constant value.
"""
