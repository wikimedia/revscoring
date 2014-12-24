from itertools import groupby

from ..datasources import contiguous_segments_added
from .feature import feature_processor


@feature_processor(returns=int, depends_on=[contiguous_segments_added])
def longest_repeated_char_added(contiguous_segments_added):
    
    longest = 0
    
    for segment in contiguous_segments_added:
        
        for letter, group in groupby(segment.lower(), lambda c:c):
            
            longest = max(longest, len(list(group)))
        
    
    return longest
