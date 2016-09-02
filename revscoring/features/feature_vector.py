from . import Feature


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
