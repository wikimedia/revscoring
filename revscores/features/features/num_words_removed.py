import re

from ..datasources import contiguous_segments_removed
from ..dependencies import depends_on

WORD_RE = re.compile('\w+')

@depends_on(contiguous_segments_removed)
def num_words_removed(contiguous_segments_removed):
    
    return sum(len(WORD_RE.findall(segment))
               for segment in contiguous_segments_removed)
