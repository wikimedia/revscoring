import re

from ..datasources import contiguous_segments_added
from ..util.dependencies import depends

WORD_RE = re.compile('\w+')

@depends(on=[contiguous_segments_added])
def num_words_added(contiguous_segments_added):
    
    return sum(len(WORD_RE.findall(segment))
               for segment in contiguous_segments_added)
