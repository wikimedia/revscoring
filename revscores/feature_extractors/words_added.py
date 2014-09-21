import re

from ..datasources import contiguous_segments_added
from ..util.dependencies import depends
from ..util.returns import returns

WORD_RE = re.compile('\w+')

@depends(on=[contiguous_segments_added])
@returns(int)
def words_added(contiguous_segments_added):
    
    return sum(len(WORD_RE.findall(segment))
               for segment in contiguous_segments_added)
