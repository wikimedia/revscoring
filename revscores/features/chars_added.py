from ..datasources import contiguous_segments_added
from .feature import feature_processor


@feature_processor(returns=int, depends_on=[contiguous_segments_added])
def chars_added(contiguous_segments_added):
    return len("".join(contiguous_segments_added))
