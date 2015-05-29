from ..dependent import dig as dependent_dig
from ..dependent import dig_many as dependent_dig_many
from .datasource import Datasource


def dig(dependent):
    return (d for d in dependent_dig(dependent) if isinstance(d, Datasource))

def dig_many(dependents):
    return (d for d in dependent_dig_many(dependents)
            if isinstance(d, Datasource))
