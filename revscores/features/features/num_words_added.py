import re

from ..datasources import contiguous_segments_added
from ..dependencies import depends_on

WORD_RE = re.compile('\w+')

@depends_on(contiguous_segments_added)
def num_words_added(contiguous_segments_added):
    
    return sum(len(WORD_RE.findall(segment))
               for segment in contiguous_segments_added)
