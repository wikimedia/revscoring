from ..datasources import contiguous_segments_added
from .feature import Feature


def process(contiguous_segments_added):
    return len(contiguous_segments_added)

segments_added = Feature("segments_added", process,
                         returns=int, depends_on=[contiguous_segments_added])
