import re

from ..datasources import revision_text
from ..util.dependencies import depends
from ..util.returns import returns

WORD_RE = re.compile('[a-zA-Z]+', re.UNICODE)

@depends(on=[revision_text])
@returns(int)
def prev_words(revision_text):
    
    words = 0
    
    for m in WORD_RE.finditer(revision_text):
        
        words += 1
        
    return words
