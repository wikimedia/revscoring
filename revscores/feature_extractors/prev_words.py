import re

from ..datasources import revision_text
from ..util.dependencies import depends
from ..util.returns import returns

WORD_RE = re.compile('\w+')

@depends(on=["language", revision_text])
@returns(int)
def prev_words(revision_text):
    
    misspellings = 0
    
    for m in in WORD_RE.finditer(revision_text):
        misspellings += 1
        
    return misspellings
