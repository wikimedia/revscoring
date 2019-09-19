"""
.. autoclass:: revscoring.FeatureVector
    :members:
"""
from revscoring.features import Feature


class FeatureVector(Feature):
    """
    Represents a vector of predictive features.

    :Parameters:
        name : str
            The name of the feature
        process : `func`
            A function that will generate a feature value
        returns : `type`
            A type to compare the return vector of this function to.
        dependencies : `list`(`hashable`)
            An ordered list of dependencies that correspond
            to the `*args` of `process`
    """

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
