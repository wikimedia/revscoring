import re

from ..datasources import contiguous_segments_removed
from .feature import feature_processor

WORD_RE = re.compile('\w+', re.UNICODE)

@feature_processor(returns=int, depends_on=[contiguous_segments_removed])
def words_removed(contiguous_segments_removed):
    
    return sum(len(WORD_RE.findall(segment))
               for segment in contiguous_segments_removed)
