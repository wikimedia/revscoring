from . import datasources
from ....meta import aggregators
from .util import prefix

segments_added = aggregators.len(
    datasources.segments_added,
    name=prefix + ".segments_added"
)
"""
A count of the number of segments added in this edit.
"""

segments_removed = aggregators.len(
    datasources.segments_removed,
    name=prefix + ".segments_removed"
)
"""
A count of the number of segments removed in this edit.
"""
