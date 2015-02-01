from ..datasources import contiguous_segments_added
from .feature import Feature


def process(contiguous_segments_added):
    return len("".join(contiguous_segments_added))

chars_added = Feature("chars_added", process, returns=int,
                      depends_on=[contiguous_segments_added])
