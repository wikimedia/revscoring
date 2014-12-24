from itertools import groupby

from ..datasources import contiguous_segments_added
from .feature import Feature


def process(contiguous_segments_added):
    
    longest = 0
    
    for segment in contiguous_segments_added:
        
        for letter, group in groupby(segment.lower(), lambda c:c):
            
            longest = max(longest, len(list(group)))
        
    
    return longest

longest_repeated_char_added = Feature("longest_repeated_char_added", process,
                                      returns=int,
                                      depends_on=[contiguous_segments_added])
