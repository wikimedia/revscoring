import re

from ..datasources import contiguous_segments_removed
from ..util.dependencies import depends
from ..util.returns import returns

WORD_RE = re.compile('\w+')

@depends(on=[contiguous_segments_removed])
@returns(int)
def num_words_removed(contiguous_segments_removed):
    
    return sum(len(WORD_RE.findall(segment))
               for segment in contiguous_segments_removed)
