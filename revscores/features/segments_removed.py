from ..datasources import contiguous_segments_removed
from .feature import feature_processor


@feature_processor(returns=int, depends_on=[contiguous_segments_removed])
def segments_removed(contiguous_segments_removed):
    return len(contiguous_segments_removed)
