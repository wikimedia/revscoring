"""
These Meta-Features expand a single feature into multiple deatures.

.. autoclass revscoring.features.meta.expanders.list_of
"""
from ..feature import FeatureVector


class list_of(FeatureVector):

    def __init__(self, feature, depends_on=None, name=None):
        name = self._format_name(name, [feature])
        super().__init__(
            name, self.process, depends_on=depends_on,
            returns=feature.returns)
        self.feature = feature

    def process(self, *lists_of_values):
        return [self.feature(*values) for values in zip(*lists_of_values)]
