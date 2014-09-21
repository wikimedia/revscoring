import re

from ..datasources import contiguous_segments_added
from ..util.dependencies import depends
from ..util.returns import returns

WORD_RE = re.compile('\w+')

@depends(on=["language", contiguous_segments_added])
@returns(int)
def badwords_added(language, contiguous_segments_added):
    
    badwords = 0
    
    for segment in contiguous_segments_added:
        words = (m.group(0) for m in WORD_RE.finditer(segment))
        for badword in language.badwords(words):
            badwords += 1
        
    
    return badwords
