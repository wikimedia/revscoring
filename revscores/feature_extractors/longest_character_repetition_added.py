from itertools import groupby

from ..datasources import contiguous_segments_added
from ..util.dependencies import depends
from ..util.returns import returns


@depends(on=[contiguous_segments_added])
@returns(int)
def longest_character_repetition_added(contiguous_segments_added):
    
    longest = 0
    
    for segment in contiguous_segments_added:
        
        for letter, group in groupby(segment.lower(), lambda c:c):
            
            longest = max(longest, len(list(group)))
        
    
    return longest
