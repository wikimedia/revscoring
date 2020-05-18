"""
.. autoclass:: revscoring.Feature
    :members:

.. autoclass:: revscoring.features.Modifier
    :members:

.. autoclass:: revscoring.features.Constant
    :members:
"""
from math import log as math_log

from revscoring.dependencies import Dependent

# Sets up refences to overloaded function names
math_max = max
math_min = min


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
        if returns is None:
            raise TypeError(
                "__init__() missing required named argument 'returns'")
        self.returns = returns

    def __call__(self, *args, **kwargs):
        value = super().__call__(*args, **kwargs)

        if __debug__:
            return self.validate(value)
        else:
            return value

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
            try:
                return self.returns(value)
            except ValueError:
                raise ValueError("Expected {0}, but got {1} instead."
                                    .format(self.returns, type(value)))

    @classmethod
    def or_constant(self, val):
        if isinstance(val, Feature):
            return val
        else:
            return Constant(val)


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


class Modifier(Feature):
    """
    Represents a modification of one or more predictive feature.

    :Parameters:
        name : str
            The name of the feature
        process : `func`
            A function that will generate a feature value
        return_type : `type`
            A type to compare the return of this function to.
        dependencies : `list`(`hashable`)
                An ordered list of dependencies that correspond
                to the `*args` of `process`
    """
    pass


class BinaryOperator(Modifier):

    CHAR = "?"

    def __init__(self, left, right, returns=None, name=None):
        left = Feature.or_constant(left)
        right = Feature.or_constant(right)

        if name is None:
            name = "({0} {1} {2})".format(left.name, self.CHAR, right.name)

        if returns is None:
            returns = type(self.operate(left.returns(), right.returns()))

        super().__init__(name, self.operate, returns=returns,
                         depends_on=[left, right])

    def operate(self, left, right):
        raise NotImplementedError()


class add(BinaryOperator):
    """
    Generates a feature that represents the addition of
    two :class:`revscoring.Feature` or constant values.
    """

    CHAR = "+"

    def operate(self, left, right):
        return left + right


class sub(BinaryOperator):
    """
    Generates a feature that represents the subtraction of
    two :class:`revscoring.Feature` or constant values.
    """

    CHAR = "-"

    def operate(self, left, right):
        return left - right


class mul(BinaryOperator):
    """
    Generates a feature that represents the multiplacation of
    two :class:`revscoring.Feature` or constant values.
    """

    CHAR = "*"

    def operate(self, left, right):
        return left * right


class div(BinaryOperator):
    """
    Generates a feature that represents the division of
    two :class:`revscoring.Feature` or constant values.
    """

    CHAR = "/"

    def __init__(self, left, right, name=None):
        # Explicitly setting return type to float.
        super().__init__(left, right, returns=float, name=name)

    def operate(self, left, right):
        return left / right


class Comparison(BinaryOperator):

    def __init__(self, left, right, name=None):
        # Explicitly setting return type to boolean.
        super().__init__(left, right, returns=bool, name=name)


class gt(Comparison):
    """
    Generates a feature that represents the greater-than relationship of
    two :class:`revscoring.Feature` or constant values.
    """

    CHAR = ">"

    def operate(self, left, right):
        return left > right


class lt(Comparison):
    """
    Generates a feature that represents the less-than relationship of
    two :class:`revscoring.Feature` or constant values.
    """

    CHAR = "<"

    def operate(self, left, right):
        return left < right


class ge(Comparison):
    """
    Generates a feature that represents the greater-than-or-equal relationship
    of two :class:`revscoring.Feature` or constant values.
    """

    CHAR = ">="

    def operate(self, left, right):
        return left >= right


class le(Comparison):
    """
    Generates a feature that represents the less-than-or-equal relationship of
    two :class:`revscoring.Feature` or constant values.
    """

    CHAR = "<="

    def operate(self, left, right):
        return left <= right


class eq(Comparison):
    """
    Generates a feature that represents the equality of two
    :class:`revscoring.Feature` or constant values.
    """

    CHAR = "=="

    def operate(self, left, right):
        return left == right


class ne(Comparison):
    """
    Generates a feature that represents the inequality of two
    :class:`revscoring.Feature` or constant values.
    """

    CHAR = "!="

    def operate(self, left, right):
        return left != right


class and_(Comparison):
    """
    Generates a feature that represents the conjunction of two
    :class:`revscoring.Feature` or constant values.
    """

    CHAR = "and"

    def operate(self, left, right):
        return left and right


class or_(Comparison):
    """
    Generates a feature that represents the disjunction of two
    :class:`revscoring.Feature` or constant values.
    """

    CHAR = "or"

    def operate(self, left, right):
        return left or right


class max(Modifier):
    """
    Generates a feature that represents the maximum of a set of
    :class:`revscoring.Feature` or constant values.
    """

    def __init__(self, *args, name=None):
        dependencies = [Feature.or_constant(arg) for arg in args]
        returns = float
        # Hardcoded even though max can return strings, it
        # shouldn't ever do that

        if name is None:
            name = "max({0})".format(", ".join(f.name for f in dependencies))
        super().__init__(name, self._process, returns=returns,
                         depends_on=dependencies)

    def _process(self, *feature_values):
        return float(math_max(*feature_values))


class min(Modifier):
    """
    Generates a feature that represents the minimum of a set of
    :class:`revscoring.Feature` or constant values.
    """

    def __init__(self, *args, name=None):
        dependencies = [Feature.or_constant(arg) for arg in args]
        returns = float
        # Hardcoded even though max can return strings, it
        # shouldn't ever do that

        if name is None:
            name = "min({0})".format(", ".join(f.name for f in dependencies))
        super().__init__(name, self._process, returns=returns,
                         depends_on=dependencies)

    def _process(self, *feature_values):
        return float(math_min(*feature_values))


class log(Modifier):
    """
    Generates a feature that represents the log of a
    :class:`revscoring.Feature`'s value.
    """

    def __init__(self, feature, name=None):
        feature = Feature.or_constant(feature)
        if name is None:
            name = "log({0})".format(feature.name)
        super().__init__(name, self._process,
                         returns=float, depends_on=[feature])

    def _process(self, feature_value):
        return math_log(feature_value)


class not_(Modifier):
    """
    Generates a feature that represents the negation of a
    :class:`revscoring.Feature`'s value.
    """

    def __init__(self, feature, name=None):
        feature = Feature.or_constant(feature)
        if name is None:
            name = "not {0}".format(feature.name)
        super().__init__(name, self._process,
                         returns=bool, depends_on=[feature])

    def _process(self, feature_value):
        return not feature_value
