"""
.. autoclass:: revscoring.datasources.datasource.Datasource
    :member-order:
    :inherited-members:
"""
from ..dependencies import Dependent


class Datasource(Dependent):
    """
    Represents a data source for generating features.  Unlike features,
    datasources do not necessarily generate simple scalar values.

    :Parameters:
        name : str
            The name of the feature
        process : `func`
            A function that will generate a data value
        depends_on : `list`(`hashable`)
            An ordered list of dependencies that correspond
            to the `*args` of `process`
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __hash__(self):
        return hash(('datasource', self.name))
