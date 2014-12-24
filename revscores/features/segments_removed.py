from ..datasources import contiguous_segments_removed
from .feature import Feature


def process(contiguous_segments_removed):
    return len(contiguous_segments_removed)

segments_removed = Feature("segments_removed", process,
                           returns=int,
                           depends_on=[contiguous_segments_removed])
